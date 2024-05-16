from fastapi import FastAPI, Request
from pr_pilot import PRPilot

app = FastAPI()
pr_pilot = PRPilot(api_key="your_api_key")  # Replace with your actual API key

@app.post("/webhook/jira")
async def jira_webhook(request: Request):
    payload = await request.json()
    # Parse the JIRA webhook payload into variables
    issue_key = payload.get('issue', {}).get('key', 'Unknown')
    issue_summary = payload.get('issue', {}).get('fields', {}).get('summary', 'No summary provided')
    issue_status = payload.get('issue', {}).get('fields', {}).get('status', {}).get('name', 'No status available')
    # Add more variables as needed

    # Use PR Pilot SDK to read the ticket content and find relevant information in the code
    findings = pr_pilot.analyze_code(issue_key, issue_summary)

    # Add a comment to the ticket with the findings
    pr_pilot.comment_on_ticket(issue_key, findings)

    # For now, just return the parsed information
    return {
        "issue_key": issue_key,
        "issue_summary": issue_summary,
        "issue_status": issue_status
    }