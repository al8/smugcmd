'''
get access token
'''
import httplib
import oauth.oauth as oauth
import os
import sys

import smugcmd_shared


def run():
    is_debug_print = False

    # setup
    client = smugcmd_shared.SimpleOAuthClient(smugcmd_shared.SERVER, smugcmd_shared.PORT, smugcmd_shared.REQUEST_TOKEN_URL, smugcmd_shared.ACCESS_TOKEN_URL, smugcmd_shared.AUTHORIZATION_URL)
    consumer = oauth.OAuthConsumer(smugcmd_shared.CONSUMER_KEY, smugcmd_shared.CONSUMER_SECRET)
    signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
#    signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()

    
    (key,secret) = smugcmd_shared.request_token_load()

    request_token = oauth.OAuthToken(key=key, secret=secret)

    # get access token
    print '* Obtain an access token ...'
    oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=request_token, http_url=client.access_token_url)
    oauth_request.sign_request(signature_method, consumer, request_token)
    if (is_debug_print):
        print 'REQUEST (via headers)'
        print 'parameters: %s' % str(oauth_request.parameters)
    access_token = client.fetch_access_token(oauth_request)
    
    if (access_token is None):
        print "no access token received."
        sys.exit(-1)
    
    if (is_debug_print):
        print 'GOT access token'
        print 'key: %s' % str(access_token.key)
        print 'secret: %s' % str(access_token.secret)

    print smugcmd_shared.filename_request_token
    try:
        os.remove(smugcmd_shared.filename_request_token)
    except:
        print "unable to remove file '%s'" % smugcmd_shared.filename_request_token


    smugcmd_shared.access_token_save(access_token.key, access_token.secret)
    print "Access token written to file. smugcmd setup completed. (access_token_file:'%s')" % (smugcmd_shared.filename_access_token)




if __name__ == '__main__':
    run()
