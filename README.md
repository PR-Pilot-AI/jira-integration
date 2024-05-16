# JIRA Integration Project

## Overview
This project integrates with JIRA to handle webhooks and perform specific actions based on the JIRA events. It uses FastAPI to create a web server that listens for incoming webhook requests.

## Environment Variables
- `JIRA_API_TOKEN`: The API token used to authenticate requests to the JIRA API. This is necessary for the application to interact with JIRA.

## Setup
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set the necessary environment variables.
4. Run the application using `uvicorn main:app --reload` to start the FastAPI server.

## Usage
The application is set up to receive webhook events at the root URL (`/`). It processes the incoming JSON payload to extract relevant JIRA issue details and performs actions based on the specified conditions.