def lambda_handler(event, context):
    return {
        'response':{
        'outputSpeech': {
            'type': 'PlainText',
            'text': 'hello there, how are you ?'
        },
        'shouldEndSession': True
    }
}
