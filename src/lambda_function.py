import json
import os
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import socket

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event))

    try:
        request_type = event['request']['type']
        BRIDGE_SERVER_URL = os.environ['BRIDGE_SERVER_URL']
        print(f"Using bridge URL: {BRIDGE_SERVER_URL}")

        # === LaunchRequest ===
        if request_type == 'LaunchRequest':
            speech_text = "Welcome to Incident Commander. What would you like to do?"
            should_end_session = False
            return build_response(speech_text, should_end_session)

        # === SessionEndedRequest ===
        elif request_type == 'SessionEndedRequest':
            reason = event['request'].get('reason', 'Unknown')
            print(f"Session ended. Reason: {reason}")
            return build_response("Goodbye.", should_end_session=True)

        # === IntentRequest ===
        elif request_type == 'IntentRequest':
            intent = event['request']['intent']
            intent_name = intent['name']
            print(f"Intent received: {intent_name}")

            # Handle exit/stop/cancel intents directly
            if intent_name in ['AMAZON.StopIntent', 'AMAZON.CancelIntent', 'AMAZON.NavigateHomeIntent']:
                return build_response("Exiting Incident Commander. Goodbye.", should_end_session=True)

            # Freeform query intent
            elif intent_name == 'FreeformQueryIntent':
                try:
                    user_query = intent['slots']['Query']['value']
                except KeyError:
                    user_query = ""
                print(f"User query: {user_query}")
            
            # CloseIntent , when you want to close the session
            elif intent_name == 'CloseIntent':
                return build_response("Incident Commander is now closing. Tata amigo ! ", should_end_session=True)
            else:
                # Handle unknown intents gracefully
                user_query = "What is the status of current incidents?"

            # Forward query to bridge server
            data = json.dumps({'query': user_query}).encode('utf-8')
            print(f"Sending to bridge: {data.decode('utf-8')}")

            socket.setdefaulttimeout(10)
            request = Request(
                BRIDGE_SERVER_URL,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            print("Sending request to bridge server...")
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                speech_text = result.get('response', "Sorry, I didn't understand that.")
                print(f"Bridge response: {speech_text}")

            should_end_session = False  # Keep session open
            return build_response(speech_text, should_end_session)

        else:
            print("Unhandled request type.")
            return build_response("I'm not sure how to handle that request.", should_end_session=True)

    except KeyError as e:
        print(f"Key error: {e}")
        return build_response("I didn't understand your request. Please try again.", should_end_session=True)

    except HTTPError as e:
        print(f"HTTPError: {e.code}, reason: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Bridge error body: {error_body}")
        except:
            pass
        return build_response("The incident service returned an error. Please try again later.", should_end_session=True)

    except URLError as e:
        print(f"URLError: {e.reason}")
        return build_response("I can't connect to the incident service right now.", should_end_session=True)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return build_response(f"Sorry, I encountered an error: {str(e)}", should_end_session=True)


# === Helper: Build Alexa JSON response ===
def build_response(text, should_end_session):
    return {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': text
            },
            'shouldEndSession': should_end_session
        }
    }
