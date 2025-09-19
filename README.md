# alexa-incident-commander
Incident Managment Alexa powered voice assistant backed up by incident.io 

A powerful Alexa skill that provides real-time incident status updates through natural voice commands. Built for the incident.io competition.

# Overview

Sometimes I just want a voice assistant to tell me about what's going on instead of looking at my computer screen and a thousand pages and dashboards , what if I want to know about incidents as if I am talking to colleague , with this Alexa skill backed by incident.io MCP server , it can now be a reality !

## 🎥 Demo Video
[![Demo Video]()

## ✨ Features

- **Voice-Activated Incident Updates**: Get real-time incident status through Alexa
- **Natural Language Processing**: Claude AI-powered response generation
- **Real-time Data**: Live integration with incident.io MCP server
- **Hands-Free Operation**: Perfect for incident war rooms and on-call engineers

## 🛠️ Technical Implementation

1. **Alexa Skill**: Voice interface with natural language understanding
2. **AWS Lambda**: Cloud-based request orchestration
3. **Local Bridge Server**: Flask app connecting Lambda to local services
4. **Claude AI**: Natural language response generation
5. **incident.io MCP Server**: Real-time incident data access

### Architecture

```mermaid
graph TB
    A[Alexa Device] -->|Voice Request| B[AWS Lambda Function]
    B -->|HTTP Request| C[Local Bridge Server]
    C -->|stdin/stdout MCP Protocol| D[incident.io MCP Server]
    
    D -->|MCP Response| C
    C -->|Enhanced Response with Claude AI Formatting| B
    B -->|Formatted Voice Response| A
    
    subgraph "AWS Cloud"
        B
    end
    
    subgraph "Local Environment"
        C
        D
    end
    
    classDef alexa fill:#00d4ff,stroke:#0099cc,stroke-width:2px,color:#fff
    classDef aws fill:#ff9900,stroke:#cc7700,stroke-width:2px,color:#fff
    classDef local fill:#4caf50,stroke:#388e3c,stroke-width:2px,color:#fff
    
    class A alexa
    class B aws
    class C,D local
```

# Limitations

- This is a POC , the local bridge server should ideally be another AWS lambda function
- The code can be improved for portability , it does not allow setting of custom ports , bridge url for the local bridge server at the moment
- More rigorous Alexa testing is required

# Setup
Read more about how to set this up yourself [here](setup.md)


