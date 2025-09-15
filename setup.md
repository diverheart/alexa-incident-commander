# Detailed Setup Guide

## 1. AWS Lambda Setup
- Create Lambda function with Python 3.12
- Add layer: `arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p312-requests:3`
- Set environment variable: `BRIDGE_SERVER_URL`

## 2. Local Bridge Setup
- Install dependencies: `pip install -r requirements.txt`
- Set API keys as environment variables
- Run: `python src/local_bridge.py`

## 3. Alexa Skill Configuration
- Invocation name: "incident commander"
- Intent: `QueryIntent` with sample utterances
- Slot: `Query` with type `AMAZON.SearchQuery`
- Endpoint: Lambda ARN

## 4. Tunnel Setup
- Install LocalXpose: `brew install localxpose`
- Run tunnel: `lpx tunnel http 5000`
- Update Lambda with tunnel URL