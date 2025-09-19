# Detailed Setup Guide

# Prequisites

- AWS account
- Claude API key
- Incident.io API key

# Overview

We can divide the architecture into three main components

- [Local bridge server](#setting-up-local-bridge-server) : Translates HTTP requests from AWS Lambda into stdin/stdout MCP protocol communications with your local incident.io MCP server, then enhances responses with Claude AI formatting for natural voice output

- [AWS Lambda function](#setting-up-aws-lambda) : Receives Alexa voice requests, forwards them to the local bridge server via HTTP, and returns Claude-formatted incident responses as spoken Alexa responses

- [Alexa configuration](#setting-up-alexa)

## Setting up Local bridge server

- Clone incident.io mcp server git repository and build the binary

```bash
git clone https://github.com/incident-io/incidentio-mcp-golang.git
go build -o bin/mcp-server ./cmd/mcp-server
```

- Navigate to the [local_server](../src/local_server/) directory in the current repository,
create a `.env` file to store the below environment variables

```bash
INCIDENT_IO_API_KEY=<value>
ANTHROPIC_API_KEY=<value>
MCP_SCRIPT_PATH=<path to start-mcp-server.sh>
```

- Setup a python venv and install required packages

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Run the code and forward the port via [ngrok](https://ngrok.com/docs)/[localxpose](https://localxpose.io/dashboard/access) in another terminal , I am using localxpose in the example , take note of the ephimeral domain , alternatively use their pro subscription for a persistent domain ( Being used for the current POC )

```bash
python3 local_bridge.py # in terminal 1
loclx tunnel http --to localhost:5000 # in terminal 2
```

- Test locally by a simple curl request like below

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "talk to me about incident inc-1"}'
```

Congratulations ! You now have your local bridge server set !

## Setting up AWS Lambda

- Head on to [AWS console](https://console.aws.amazon.com/)
- Navigate to `AWS Lambda`
- Create new Lambda function with Python 3.12
- Copy-paste the lambda function code from [here](../src/aws-lamda-script/lambda_function.py)
- Add layer: `arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p312-requests:3`
- Create a new Environment variable `BRIDGE_SERVER_URL` and store the ephimeral domain created by localxpose or ngrok followed by the `/ask` endpoint

## Setting up Alexa

- Go to the Alexa Developer Console: https://developer.amazon.com/alexa/console/ask
- Create a New Skill: Incident Commander
- Default language: Choose your language , ensure to choose a language that co-relates to
your alexa's location
- Choose a model to add to your skill: Click Custom.
- Choose a method to host your skill's backend resources: Click Provision your own (because we already built the backend in Lambda).
- Click Create skill.
- Choose a Template: On the next screen, choose Start from scratch and click Continue.
- Build the Interaction Model using the [Alexa json config](../src/alexa-config/)
 click Invocation under "Interaction Model" and set the Invocation Name: This is what users to incident commander.
- Link the Skill to Lambda: In the left sidebar, click Endpoint under "Interaction Model".
Select AWS Lambda ARN, Copy your Lambda function's ARN from the top right of its page in the AWS Console,Paste the ARN into the Default Region field,Click Save Endpoints.
- Test in the Developer Console,Go to the Test tab in the Alexa Developer Console,At the top, change the dropdown from "Off" to Development, type the below for starters
```bash
alexa open incident commander
tell me about the last incident
```
- Login to alexa app with the same email used in the developer console and enable the skill

C O N G R A T U L A T I O N S ! 
Now you have a personal voice incident management assistant !









