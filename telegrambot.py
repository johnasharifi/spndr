''' This is a simple wrapper class that implements a low level abstraction on the calling of the 
    telegram API. 
    
    This class has been configured by default to receive the oldest received message using Telegram's
    bot API. It keeps a connection on for a maximum of 100 seconds (long polling), if it doesn't
    receive an update, it returns None to the calling program. 

    Please go to https://core.telegram.org/bots/api to look at the API's documentation and to gain a 
    better understanding of how this wrapper works.

    FUNCTIONS IN THIS MODULE

    1. receive() - receive() implements the /getUpdates method of the API, all the parameters for this call 
                   have been taken as attributes of the calling object.
    2. send() - send() implements the /sendMessage method of the API, the necessary parameters for this
                call are the chat id which is unique for each chat/user and the text message to send.

'''

import requests, json, os

class communicate:

    service_url_prefix = 'https://api.telegram.org/bot'

    def __init__(self, offset=0, limit=100, timeout=100, allowed_updates=[], init=0):
        self.token = open(os.getcwd()+'//bot_token.txt').read()
        self.offset = offset
        self.limit = limit
        self.timeout = timeout
        self.allowed_updates = allowed_updates
        self.data = None
        self.init = init

    def receive(self):
        #print('in receive')
        api_params = {"offset":self.offset, "limit":self.limit,
                      "timeout":self.timeout, "allowed_updates":self.allowed_updates}
        #print("waiting for input")
        req_obj = requests.post(self.service_url_prefix+self.token+'/getUpdates', 
                               data=api_params)
        self.data = req_obj.json()
        #print(json.dumps(self.data, indent=4))
        if len(self.data['result'])==0:
            return None
        if self.init == 0:
            self.offset = self.data['result'][-1]['update_id']
            self.init+=1
        self.offset+=1
        #print('returning to getMsg')
        return self.data

    def send(self, chat_id, text):
        api_params = {"chat_id":chat_id, "text":text}

        req_obj = requests.post(self.service_url_prefix+self.token+'/sendMessage',
                               data=api_params)

        json_resp = req_obj.json()
        #print(json.dumps(json_resp, indent=4))


    






    








