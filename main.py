import logging
import os

from fastapi import FastAPI, Request
from jira import JIRA
from pr_pilot.util import create_task, wait_for_result

app = FastAPI()
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

logger = logging.getLogger(__name__)


@app.post("/")
async def jira_webhook(request: Request):
    payload = await request.json()
    # Parse the JIRA webhook payload into variables
    issue_key = payload.get('issue', {}).get('key', 'Unknown')
    if issue_key == 'KAN-1':
        return {}
    issue_description = payload.get('issue', {}).get('fields', {}).get('description', 'No description provided')
    added_label = payload.get('changelog', {}).get('items', [{}])[0].get('toString', 'No label added')
    if added_label == 'needs-refinement':
        logger.info(f"Received JIRA webhook for issue {issue_key} with added label {added_label}")
        prompt = (f"I have a JIRA ticket with the following description:\n---\n{issue_description}\n---\n"
                  f"The issue needs to be refined with technical context. Pretend like you are the technical lead of the project and do the refinement:\n"
                  f"1. If the ticket mentions file paths, read the files\n"
                  f"2. If the ticket contains references to functions/classes/etc, search with ripgrep and read the relevant files\n"
                  f"3. Respond with your comment.\n\n"
                  f"Your comment should:\n"
                  f"- Be short and concise\n"
                  f"- Contain functional and non-functional requirements\n"
                  f"- Include links (complete Github URLs) to the relevant files in the codebase\n\n"
                  f"Return your plain comment in JIRA Text Formatting Notation:\n\n"
                  f"- To create a header, place `hn. ` at the start of the line (where n can be a number from 1-6).\n"
                  f"- To create a link, use `[text|URL]`.\n"
                  "- To create a code block, use {code}...{code}.\n"
                  "- For monospaced inline text, use {{monospaced}}.\n")
        task = create_task("PR-Pilot-AI/pr-pilot", prompt)
        new_issue_description = wait_for_result(task)


        jira = JIRA('https://mlamina.atlassian.net', basic_auth=('mlamina09@gmail.com', JIRA_API_TOKEN))
        # Add the technical context as a comment to the issue
        jira.add_comment(issue_key, new_issue_description)

    # For now, just return the parsed information
    return {}
