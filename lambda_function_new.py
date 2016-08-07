from __future__ import print_function

import requests

BASE_URL = 'http://162.243.165.89:5000'

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

   session_attributes = {}
    card_title = "Git open"
    speech_output = "Shell activated" \
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I couldn't understand you. " \
                    "Could you repeat yourself?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "list":
        return listdir(intent, session)
    elif intent_name == "Change directory":
        return chandir(intent, session)
    elif intent_name == "Current directory":
        return workdir(intent, session)
    elif intent_name == "Git add":
        return gadd(intent, session)
    elif intent_name == "Git status":
        return gstatus(intent, session)
    elif intent_name == "Git Push":
        return gpush(intent, session)
    elif intent_name == "Git Pull":
        return gpull(intent, session)
    elif intent_name == "Git Commit":
        return gcommit(intent, session)
    else:
        return donothelp(intent, session)

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please tell me your favorite color by saying, " \
                    "my favorite color is red"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your favorite color by saying, " \
                    "my favorite color is red."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def set_nodejs_in_session(intent, session):
    """ Sets the node.js to be the only real dev language in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'Nodejs' in intent['slots']:
        real_dev_language = intent['slots']['Nodejs']['value']
        session_attributes = create_real_dev_language_attributes(real_dev_language)
        speech_output = "I now know that only real dev language is " + \
                        real_dev_language + \
                        ". You can ask me the only real dev language by saying, " \
                        "what's the only real dev language?"
        reprompt_text = "You can ask me your favorite color by saying, " \
                        "what's my favorite color?"
    else:
        speech_output = "I'm not sure what the only real dev language is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your favorite color is. " \
                        "You can tell me your favorite color by saying, " \
                        "my favorite color is red."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_real_dev_language_attributes(real_dev_language):
    return {"realDevLanguage": real_dev_language}


def get_dev_lang_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "realDevLanguage" in session.get('attributes', {}):
        real_dev_language = session['attributes']['realDevLanguage']
        speech_output = "The only real dev language is " + real_Dev_Language + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what the only real dev language is. " \
                        "You can say, the only real dev language is Nodejs."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
        
def donothelp(intent, session):
    card_title = "No"
    speech_output = "I couldn't understand you." 
    session_attributes = {}
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Response-Builders --------------------------------------------

def genericResponse(resp):
    speech_output = resp.text
    return build_response({}, build_speechlet_response("list", speech_output, "", False))

def forwardGetRequest(subpath):
    return genericResponse(requests.get(BASE_URL+subpath))

def forwardPostRequest(subpath, data=None):
    return genericResponse(requests.put(BASE_URL+subpath, data=data))

# --------------- Responses ----------------------------------------------------

def listdir(intent,session):
    return forwardGetRequest("/ls")

def chandir(intent,session):
    return forwardPostRequest("/cd",data={"dir":intent["directory"]})

def workdir(intent,session):
    return forwardGetRequest("/pwd")

def gadd(intent, session):
    return forwardPostRequest("/git/add", data={"filename":intent["filename"]})

def gstatus(intent, session):
    return forwardGetRequest("/git/status")

def gpush(intent, session):
    return forwardPostRequest("/git/push")

def gpull(intent, session):
    return forwardPostRequest("/git/pull")

def gcommit(intent, session):
    return forwardPostRequest("/git/commit", data={"message":intent["message"]})

# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
