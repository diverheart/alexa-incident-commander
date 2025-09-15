# alexa-incident-commander
Incident Managment Alexa powered voice assistant backed up by incident.io 

A powerful Alexa skill that provides real-time incident status updates through natural voice commands. Built for the incident.io competition.

[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange?logo=amazon-aws)](https://aws.amazon.com/lambda/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask)](https://flask.palletsprojects.com/)
[![Claude AI](https://img.shields.io/badge/Powered%20by-Claude-ff69b4)](https://claude.ai)

## 🎥 Demo Video
[![Demo Video]()

## ✨ Features

- **Voice-Activated Incident Updates**: Get real-time incident status through Alexa
- **Natural Language Processing**: Claude AI-powered response generation
- **Real-time Data**: Live integration with incident.io MCP server
- **Hands-Free Operation**: Perfect for incident war rooms and on-call engineers

## 🛠️ Technical Implementation

### Components

1. **Alexa Skill**: Voice interface with natural language understanding
2. **AWS Lambda**: Cloud-based request orchestration
3. **Local Bridge Server**: Flask app connecting Lambda to local services
4. **Claude AI**: Natural language response generation
5. **incident.io MCP Server**: Real-time incident data access

### Key Technologies

- **AWS Lambda** + **API Gateway** - Cloud infrastructure
- **Python 3.12** - Backend logic
- **Flask** - Local bridge server
- **Anthropic Claude API** - AI-powered responses
- **incident.io MCP Server** - Incident data access
- **LocalXpose** - Secure tunneling for local development

## 🚀 Quick Start

### Prerequisites

- AWS Account with Lambda access
- Amazon Developer Account for Alexa Skills
- incident.io account with API access
- Anthropic Claude API key
- Python 3.12+

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/incident-commander-alexa-skill.git
   cd incident-commander-alexa-skill

2. Run the following commands
   ```bash
   pip install -r requirements.txt
   export INCIDENT_IO_API_KEY=your_key
   export ANTHROPIC_API_KEY=your_key
   python src/local_bridge.py
   
3. Deploy Lambda function

  - Upload src/lambda_function.py to AWS Lambda

  - Set environment variable BRIDGE_SERVER_URL

  - Add AWS Secrets Manager permissions

  - Configure Alexa Skill

  - Create skill in Alexa Developer Console

  - Set invocation name: "incident commander"

  - Configure QueryIntent with sample utterances

  - Connect to Lambda ARN
