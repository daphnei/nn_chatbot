"""
In this file we specify default event handlers which are then populated into the handler map using metaprogramming
Copyright Anjishnu Kumar 2015
Happy Hacking!
"""
import random
from ask import alexa
import alexa_client
CONV_START = "0"
CONV_CONT = "1"
CONV_ACCEPT = "2"
CONV_REJECT = "3"
CONV_END = "4"


def lambda_handler(request_obj, context=None):
    '''
    This is the main function to enter to enter into this code.
    If you are hosting this code on AWS Lambda, this should be the entry point.
    Otherwise your server can hit this code as long as you remember that the
    input 'request_obj' is JSON request converted into a nested python object.
    '''

    metadata = {'h' : 'SomeRandomDude'} # add your own metadata to the request using key value pairs
    
    ''' inject user relevant metadata into the request if you want to, here.    
    e.g. Something like : 
    ... metadata = {'user_name' : some_database.query_user_name(request.get_user_id())}

    Then in the handler function you can do something like -
    ... return alexa.create_response('Hello there {}!'.format(request.metadata['user_name']))
    '''
    return alexa.route_request(request_obj, metadata)


@alexa.default_handler()
def default_handler(request):
    user_utterance = request.get_slot_map()["Text"]

    if user_utterance.lower() == "yes":
        alexa_client.talk_to_server(CONV_ACCEPT)
        if random.random():
        	alexa_reply = "Great! What's the next sentence?"
        else:
            alexa_reply = "I'll add it to the story. What's next?"
    elif user_utterance.lower() == "no":
        alexa_client.talk_to_server(CONV_REJECT)
        if random.random():
        	alexa_reply = "Bummer! Let's try again."
        else:
            alexa_reply = "Ok, why don't you suggest a next sentence."
    elif user_utterance.lower() == "end" or user_utterence.lower().contains("what is the story so far"):
        alexa_reply = alexa_client.talk_to_server(CONV_END)
        alexa_reply = "Here is the story: " + alexa_reply
    else:
        alexa_reply = "The next line will be, " + alexa_client.talk_to_server(CONV_START + user_utterance)
         if random.random():
             alexa_reply += " Is that good?"
         else:
             alexa_reply += " Do you want to add it to the story?"

            
    """ The default handler gets invoked if no handler is set for a request """
    return alexa.create_response(message=alexa_reply)


@alexa.request_handler("LaunchRequest")
def launch_request_handler(request):
    return alexa.create_response(message="Welcome to the story generator. What should the first sentence be?")


@alexa.request_handler("SessionEndedRequest")
def session_ended_request_handler(request):
    return alexa.create_response(message="Goodbye!")
