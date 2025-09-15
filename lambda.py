import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))
    
    try:
        # Get bridge URL from environment variable
        BRIDGE_SERVER_URL = os.environ['BRIDGE_SERVER_URL']
        print(f"Using bridge URL: {BRIDGE_SERVER_URL}")
        
        # Handle different types of Alexa requests
        request_type = event['request']['type']
        
        if request_type == 'LaunchRequest':
            # User said "open incident commander" - give a welcome message
            user_query = "Welcome to Incident Commander. What would you like to know about your incidents?"
            should_end_session = False  # Keep session open for follow-up questions
        elif request_type == 'IntentRequest':
            # User asked a specific question - extract their query
            user_query = event['request']['intent']['slots']['Query']['value']
            should_end_session = True  # End session after answering
        else:
            # Other request types (SessionEndedRequest, etc.)
            user_query = "What is the status of active incidents?"
            should_end_session = True
        
        print(f"Processing query: '{user_query}'")
        print(f"Request type: {request_type}")
        print(f"Should end session: {should_end_session}")

        # Prepare the request data
        data = json.dumps({'query': user_query}).encode('utf-8')
        print(f"Request data: {data.decode('utf-8')}")
        
        # Make the request
        socket.setdefaulttimeout(10)
        
        request = Request(
            BRIDGE_SERVER_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        print("Making request to bridge server...")
        
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            speech_text = result['response']
            print(f"SUCCESS! Bridge response: {speech_text}")
        
    except KeyError as e:
        print(f"Key error: {e}")
        speech_text = "I didn't understand your request. Please try again."
        should_end_session = True
    except HTTPError as e:
        print(f"HTTP error from bridge server: {e}")
        print(f"HTTP status: {e.code}")
        print(f"HTTP reason: {e.reason}")
        # Read the response body for more details
        try:
            error_body = e.read().decode('utf-8')
            print(f"Error response body: {error_body}")
        except:
            pass
        speech_text = "The incident service returned an error. Please try again later."
        should_end_session = True
    except URLError as e:
        print(f"Network error: {e}")
        print(f"Error reason: {e.reason}")
        speech_text = "I can't connect to the incident service right now."
        should_end_session = True
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        speech_text = f"Sorry, I encountered an error: {str(e)}"
        should_end_session = True

    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {'type': 'PlainText', 'text': speech_text},
            'shouldEndSession': should_end_session
        }
    }