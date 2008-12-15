import sys
import os
import tempfile
import pickle
import pysmug


########################################################################################################################


#application directories
def get_appdir():
    return os.path.dirname(sys.argv[0])
def getfile_appdir(filename):
    return os.path.join(get_appdir(), filename)
def get_tempdir():
    return tempfile.gettempdir()

########################################################################################################################

#smugcmd api key and secret
#set consumer key and secret here (strings), otherwise, will load from file 'apikey.txt'.
CONSUMER_KEY = None
CONSUMER_SECRET = None


filename_apikey = getfile_appdir("apikey.txt")

def load_apikeyfile():
    global CONSUMER_KEY, CONSUMER_SECRET
    #file is in the form of:
    #---------------------------- SOF
    #apikey
    #apisecret
    #---------------------------- EOF
    try:
        f = open(filename_apikey)
        CONSUMER_KEY = f.readline().strip()
        CONSUMER_SECRET = f.readline().strip()
        f.close()
        return True
    except IOError:
        return False

if CONSUMER_KEY is None or CONSUMER_SECRET is None or CONSUMER_KEY == '' or CONSUMER_SECRET == '':
    rc = load_apikeyfile()
    if not rc:
        print "Error loading API key file '%s'" % filename_apikey
        sys.exit(-1)

########################################################################################################################


#oauth urls
SERVER = 'api.smugmug.com'
PORT = 80

REQUEST_TOKEN_URL = 'http://api.smugmug.com/services/oauth/getRequestToken.mg'
ACCESS_TOKEN_URL = 'http://api.smugmug.com/services/oauth/getAccessToken.mg'
AUTHORIZATION_URL = 'http://api.smugmug.com/services/oauth/authorize.mg'



filename_request_token = getfile_appdir("smugcmd_request_token.pkl")
filename_access_token = getfile_appdir("smugcmd_access_token.pkl")




def _token_save(filename, key, secret, errmsg = "unable to write token to file. (%s)"):
    try:
        f = open(filename, "w")
        pickle.dump((key, secret,), f)
        f.close()
    except IOError:
        print errmsg % filename
        sys.exit(-1)
        return None
    return (key, secret)
    
def _token_load(filename, errmsg = "unable to read token from file. (%s)"):
    try:
        f = open(filename, "r")
        (key, secret,) = pickle.load(f)
        f.close()
    except IOError:
        print errmsg % filename
        sys.exit(-1)
        return None
    return (key, secret)



def request_token_save(key, secret):
    return _token_save(filename_request_token, key, secret)
    
def request_token_load():
    return _token_load(filename_request_token)

def access_token_save(key, secret):
    return _token_save(filename_access_token, key, secret)
    
def access_token_load():
    return _token_load(filename_access_token)


########################################################################################################################

import httplib
import oauth.oauth as oauth

# client using httplib with headers
class SimpleOAuthClient(oauth.OAuthClient):

    def __init__(self, server, port=httplib.HTTP_PORT, request_token_url='', access_token_url='', authorization_url=''):
        self.server = server
        self.port = port
        self.request_token_url = request_token_url
        self.access_token_url = access_token_url
        self.authorization_url = authorization_url
        self.connection = httplib.HTTPConnection("%s:%d" % (self.server, self.port))

    def fetch_request_token(self, oauth_request):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        x = response.read()
        return oauth.OAuthToken.from_string(x)

    def fetch_access_token(self, oauth_request, is_debug_print=False):
        # via headers
        # -> OAuthToken
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        respstr = response.read()
        if (is_debug_print): print "access token response:", respstr
        try:
            return oauth.OAuthToken.from_string(respstr)
        except KeyError:
            print "Unable to get access token: '%s'" % respstr
            print "Possible reasons:"
            print "  Access token already retreived."
            print "  This step was not completed within 20 minutes."
            return None

    def get_authorize_token_url(self, oauth_request):
        return oauth_request.to_url()


########################################################################################################################


if __name__ == "__main__":
    print "get_appdir():", get_appdir()
    print "get_tempdir():", get_tempdir()
    
    print "filename_request_token:", filename_request_token
    


