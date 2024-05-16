import logging
import os

from fastapi import FastAPI, Request
from jira import JIRA
from pr_pilot.util import create_task, wait_for_result


JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
JIRA_API_USER = os.getenv('JIRA_API_USER')
JIRA_API_ENDPOINT = os.getenv('JIRA_API_ENDPOINT')

GITHUB_REPO = os.getenv('GITHUB_REPO', 'PR-Pilot-AI/pr-pilot')

app = FastAPI()
logger = logging.getLogger(__name__)


PROMPT = """
I have a JIRA ticket with the following description:
---
{issue_description}
---
The issue needs to be refined with technical context. Pretend like you are the technical lead of the project and do the refinement:
1. If the ticket mentions file paths, read the files
2. If the ticket contains references to functions/classes/etc, search with ripgrep and read the relevant files
3. Respond with your comment.

Your comment should:
- Be short and concise
- Contain functional and non-functional requirements
- Include links (complete Github URLs) to the relevant files in the codebase

Return your plain comment in JIRA Text Formatting Notation:
- To create a header, place `hn. ` at the start of the line (where n can be a number from 1-6).
- To create a link, use `[text|URL]`.
- To create a code block, use {{code}}...{{code}}.
- For monospaced inline text, use {{{{monospaced}}}}.
"""


@app.post("/")
async def jira_webhook(request: Request):
    payload = await request.json()

    # Parse the JIRA webhook payload into variables
    issue_key = payload.get('issue', {}).get('key', 'Unknown')
    issue_description = payload.get('issue', {}).get('fields', {}).get('description', 'No description provided')
    added_label = payload.get('changelog', {}).get('items', [{}])[0].get('toString', 'No label added')

    # React if the label "needs-refinement" was added to the ticket
    if added_label == 'needs-refinement':
        logger.info(f"Received JIRA webhook for issue {issue_key} with added label {added_label}")

        # Ask PR Pilot to do technical refinement for the ticket
        task = create_task(GITHUB_REPO, PROMPT.format(issue_description=issue_description))
        technical_refinement = wait_for_result(task)

        # Add the technical context as a comment to the issue
        jira = JIRA(JIRA_API_ENDPOINT, basic_auth=(JIRA_API_USER, JIRA_API_TOKEN))
        jira.add_comment(issue_key, technical_refinement)

    return {}
