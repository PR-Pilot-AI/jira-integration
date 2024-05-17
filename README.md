# PR Pilot Demo: LLM-Based Technical Refinement for JIRA Tickets

## Demo Video

[![Watch the video](https://img.youtube.com/vi/3F_MID7CiXg/maxresdefault.jpg)](https://youtu.be/3F_MID7CiXg)

## Use Case
This project demonstrates how [PR Pilot](https://www.pr-pilot.ai) can be used to easily automate some of your workflows in JIRA.

The demo uses FastAPI to create a web server that listens for incoming webhook requests.
The webhook handler reacts if a new label `needs-refinement` is added to a JIRA issue. It then instructs PR Pilot to
act as a technical lead for the issue.

PR Pilot will **autonomously**:

1. Read the JIRA ticket and find code references
2. Find the relevant code and understand it in the context of the ticket
3. Add a comment to the ticket with a technical refinement


## Environment Variables
- `JIRA_API_TOKEN`: The API token used to authenticate requests to the JIRA API. This is necessary for the application to interact with JIRA.
- `JIRA_API_USER`: The email address associated with the JIRA account. This is used to authenticate requests to the JIRA API.
- `JIRA_API_ENDPOINT`: The base URL of the JIRA instance. This is used to construct the URLs for the JIRA API requests.
- `PR_PILOT_API_TOKEN`: The API token used to authenticate requests to the PR Pilot API. This is necessary for the application to interact with PR Pilot.
- `GITHUB_REPO`: The name of the GitHub repository.

## Setup
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set the necessary environment variables.
4. Run the application using `fastapi dev main.py` to start the FastAPI server.

## Usage
The application is set up to receive webhook events at the root URL (`/`).
To trigger the webhook handler, add the label `needs-refinement` to a JIRA issue.