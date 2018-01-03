

from __future__ import print_function
import random

question=0

questions= ["Who's the author of Sherlock Holmes Series?", "What's the national bird of USA?" , "what's the capital of the United States?",
            "What's the capital of China? " , "what's the capital of India?"]

answers= [["Arthur Conan Doyle","Charles Dickens","F.Scott Fitzerald"],["Bald Eagle","Vulture","Sparrow"],["Washington DC", "Seattle", "New York"] ,["Beijing", "Shanghai", "Tibet"],["New Delhi", "Mumbai", "Banglore"]]

choiceLetter=['A','B','C']

afterShuffleChoice=""

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
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


# --------------- Functions that control the skill's behavior ------------------

def get_question(num):

    return(questions[num])

def get_answers(num):

    shuffleAns= list(answers[num])
    random.shuffle(shuffleAns)

    all_answers=""

    choiceIndex=0

    for answer in shuffleAns:
        print (answer)
        all_answers+= ("{}, {} , ").format(choiceLetter[choiceIndex],answer)
        if answer==answers[num][0]:

                afterShuffleChoice= choiceLetter[choiceIndex]

                #setAfterShuffleChoice(afterShuffleChoice)
        choiceIndex+=1
    response=[all_answers, afterShuffleChoice]
    return (response)


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Quiz. Say start quiz to start the quiz."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I didn't get that. Would you like to start the quiz? If yes say, start quiz."
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


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def answer_question(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """
    card_title = intent['name']
    session_attributes= session["attributes"]
    should_end_session = False

    choice= intent['slots']['Choices']['value']
    print (choice.lower) # can delete this line

    right_answer=  session_attributes["ShuffledChoice"]
    print (right_answer) # can delete this line
    right_answer.lower()

    ShuffledChoice=""

    if choice.lower()==right_answer.lower() :


        session_attributes['score']+=1

        currentQuestion=session_attributes['currentQuestion']
        session_attributes['currentQuestion'] +=1
        currentQuestion+=1
        if currentQuestion>4:
            response= get_answers(currentQuestion-1)
        else:
            response= get_answers(currentQuestion)
        answer=response[0]
        ShuffledChoice=response[1]


        if currentQuestion<=4:
            speech_output = "Correct! Next question! " + get_question(currentQuestion)+" "+  answer

            reprompt_text = "I dind't understand that. What was your choice?" #delete this ?
        else :
            speech_output = "Correct! You scored:  " + str(session_attributes["score"])+ " out of 5. "
            should_end_session = True




    elif session_attributes["currentQuestion"]<=3:
        currentQuestion=session_attributes['currentQuestion']
        currentQuestion+=1
        response= get_answers(currentQuestion)
        answer=response[0]
        ShuffledChoice=response[1]

        session_attributes['currentQuestion'] =currentQuestion

        speech_output="Wrong! Next question!" + get_question(currentQuestion)+ " "+ answer
    else:
        speech_output="Wrong!. You scored:  " + str(session_attributes["score"])+ " out of 5. "
        should_end_session = True
        ShuffledChoice=""
        #session_attributes["score":session_attributes["score"]]


    reprompt_text="Sorry. I didn't get that! Please choose again."
    session_attributes["ShuffledChoice"] = ShuffledChoice
    #session_attributes = {"ShuffledChoice":ShuffledChoice}
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def start_quiz(intent, session):
#def get_color_from_session(intent, session):

    reprompt_text = None

    response= get_answers(0)
    answer=response[0]
    ShuffledChoice=response[1]
    #session["SessionAttributes"]["afterShuffleChoice"]= afterShuffleChoice

    speech_output="Alright.. First Question, "   + get_question(0)+ "  " +answer

    session_attributes = {"ShuffledChoice":ShuffledChoice ,"currentQuestion":0 ,"score":0}
    should_end_session=False


    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AnswerIntent":
        return answer_question(intent, session)
    elif intent_name == "StartQuizIntent":
        return start_quiz(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

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
