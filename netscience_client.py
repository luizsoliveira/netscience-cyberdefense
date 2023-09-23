import json
import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

class NetScienceClient:

    API_AUTH_ENDPOINT = 'rpc/login'
    API_TASK_ENDPOINT = 'rpc/catch_task'

    def __init__(self,
                 base_url,
                 username,
                 password,
                 logging=False,
                 debug=False
                 ):
        
        self.base_url = base_url
        self.logging = logging
        self.debug = debug
        self.token = False

        self.username = username
        self.password = password
        
        #Checking if logging has a valid value
        if not (self.logging==False or (hasattr(self.logging, 'basicConfig') and hasattr(self.logging.basicConfig, '__call__'))):
            raise Exception('The logging parameters need to be a valid logging object or False')
        
    def do_auth(self):
        data = {
        "email": self.username,
        "pass": self.password
        }

        # sending post request and saving response as response object
        r = requests.post(url=f"{self.base_url}/{self.API_AUTH_ENDPOINT}", data=data)
        response_data = json.loads(r.text)

        if (r.status_code != 200):
            raise Exception(f"Some problem occurred during the authentication. Code: {r.status_code}. Message: {response_data['message']}.")


        if (response_data['token']):
            self.token = response_data['token']
            return response_data['token']
        else:
            raise Exception(f"The expected token was not present in the response. Instead was received: {response_data['message']}")

    def check_authentication(self):
        # Firstly, check if the instance already has a token
        # If not, try to authenticate
        if not (self.token or self.do_auth()):
            raise Exception(f"Was not possible to authenticate. See the logs.")
        
        return True

    def catch_task(self, task_type):

        self.check_authentication()

        data = {
        "tasktype": task_type
        }

        # sending post request and saving response as response object
        r = requests.post(url=f"{self.base_url}/{self.API_TASK_ENDPOINT}", data=data)
        response_data = json.loads(r.text)

        if (r.status_code != 200):
            raise Exception(f"Some problem occurred during the task catching. Code: {r.status_code}. Message: {response_data['message']}.")

        return response_data
        