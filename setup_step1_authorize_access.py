'''
authorize access (through url)

oauth flow:
    step 1:
        obtain a request token
        authorize the request token (via URL login)
    
    step 2:
        use request token to get access token
        save access token to be used for subsequent accesses
'''

import httplib
import oauth.oauth as oauth
import webbrowser

import smugcmd_shared



def run():
    is_debug_print = False

    # setup
    client = smugcmd_shared.SimpleOAuthClient(smugcmd_shared.SERVER, smugcmd_shared.PORT, smugcmd_shared.REQUEST_TOKEN_URL, smugcmd_shared.ACCESS_TOKEN_URL, smugcmd_shared.AUTHORIZATION_URL)
    consumer = oauth.OAuthConsumer(smugcmd_shared.CONSUMER_KEY, smugcmd_shared.CONSUMER_SECRET)
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
#    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

    # get request token
    print '* Obtaining a request token ...'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, http_url=client.request_token_url)
    oauth_request.sign_request(signature_method, consumer, None)
    if (is_debug_print):
        print 'REQUEST (via headers)'
        print 'parameters: %s' % str(oauth_request.parameters)
    request_token = client.fetch_request_token(oauth_request)
    print 'GOT request token'
    if (is_debug_print):
        print '  key: %s' % str(request_token.key)
        print '  secret: %s' % str(request_token.secret)
    

    smugcmd_shared.request_token_save(request_token.key, request_token.secret)

#    print '* Authorizing the request token ...'
    oauth_request = oauth.OAuthRequest.from_token_and_callback(token=request_token, http_url=client.authorization_url)
    authorize_token_url = client.get_authorize_token_url(oauth_request)
    
    print "If a web browser did not automatically open, go to this URL to authorize the token:\n%s\n" % authorize_token_url
    print "   You must authorize the token and obtain an access token within 20 minutes."
    webbrowser.open(authorize_token_url)



if __name__ == '__main__':
    run()
