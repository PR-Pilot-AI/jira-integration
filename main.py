from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhook/jira")
async def jira_webhook(request: Request):
    payload = await request.json()
    # Parse the JIRA webhook payload into variables
    issue_key = payload.get('issue', {}).get('key', 'Unknown')
    issue_summary = payload.get('issue', {}).get('fields', {}).get('summary', 'No summary provided')
    issue_status = payload.get('issue', {}).get('fields', {}).get('status', {}).get('name', 'No status available')
    # Add more variables as needed

    # For now, just return the parsed information
    return {
        "issue_key": issue_key,
        "issue_summary": issue_summary,
        "issue_status": issue_status
    }