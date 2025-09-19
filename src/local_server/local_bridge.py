# local_bridge.py
from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
import logging
import subprocess
import json
import time

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
client = Anthropic()

# Path to your MCP server script
env = os.environ.copy()
MCP_SCRIPT_PATH = os.getenv('MCP_SCRIPT_PATH')

# Global process variable
mcp_process = None

# In your local_bridge.py, add this at the top
@app.before_request
def log_request_info():
    print(f"=== INCOMING REQUEST ===")
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Path: {request.path}")
    print(f"Headers:")
    for key, value in request.headers:
        print(f"  {key}: {value}")
    print(f"Data: {request.get_data().decode('utf-8')}")
    print(f"========================")

@app.after_request
def log_response_info(response):
    print(f"=== OUTGOING RESPONSE ===")
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"========================")
    return response

def ensure_mcp_server_running():
    """Ensure the MCP server is running"""
    global mcp_process
    
    if mcp_process and mcp_process.poll() is None:
        return True  # Server is already running
    
    try:
        # Set environment with API key
        env = os.environ.copy()
        api_key = os.getenv('INCIDENT_IO_API_KEY')
        if not api_key:
            logger.error("INCIDENT_IO_API_KEY environment variable is not set")
            return False
            
        env['INCIDENT_IO_API_KEY'] = api_key
        logger.info("api key is",api_key)    
        
        
        # Start the MCP server
        mcp_process = subprocess.Popen(
            [MCP_SCRIPT_PATH],
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        # Wait a moment for server to initialize
        time.sleep(2)
        logger.info("MCP server started successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        return False

def ask_mcp_directly():
    """Get incident data from MCP server"""
    if not ensure_mcp_server_running():
        return None
    
    try:
        # Create a tool call message
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "list_incidents",
                "arguments": {}
            }
        }
        
        # Send to MCP server
        mcp_process.stdin.write(json.dumps(message) + '\n')
        mcp_process.stdin.flush()
        
        # Read response
        response_line = mcp_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            if 'result' in response:
                return response['result']
        
        return None
        
    except Exception as e:
        logger.error(f"Error communicating with MCP server: {e}")
        return None

def format_with_claude(user_query, incident_data):
    """Send the raw incident data to Claude for formatting"""
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0,
            system="""You are an incident management voice assistant. Your responses will be read aloud.
            Format the incident data into a clear, concise, spoken response by Alexa, whatever you respond with will be spoken by Alexa.
            Only speak from the context you are getting from the mcp server.
            Sound friendly and professional, reply in plain text to the point, please be very to the point""",
            messages=[
                {
                    "role": "user", 
                    "content": f"User asked: '{user_query}'. Here is the incident data: {json.dumps(incident_data)}. "
                }
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        logger.error(f"Error formatting with Claude: {e}")
        return "I found some incident information, but had trouble formatting it."

@app.route('/ask', methods=['POST'])
def ask_claude():
    logger.info("Received a new request on /ask endpoint.")
    
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing "query" in request body.'}), 400

    user_query = data.get('query')
    logger.info(f"Processing query: '{user_query}'")

    # 1. Get raw data from MCP server
    incident_data = ask_mcp_directly()
    
    if incident_data is None:
        response_text = "Sorry, I couldn't access the incident data right now."
    else:
        # 2. Send to Claude for nice formatting
        response_text = format_with_claude(user_query, incident_data)
    
    return jsonify({'response': response_text})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Bridge server is running!'})

if __name__ == '__main__':
    logger.info("Starting Flask bridge server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)