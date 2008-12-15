import smugcmd_shared


(access_token_key,access_token_secret) = smugcmd_shared.access_token_load()

m = smugcmd_shared.pysmug.SmugMug(
    oauth_consumer_key = smugcmd_shared.CONSUMER_KEY,
    oauth_consumer_secret = smugcmd_shared.CONSUMER_SECRET,
    oauth_access_token_key = access_token_key,
    oauth_access_token_secret = access_token_secret,
)


print "oauth access token key   :", access_token_key
print "oauth access token secret:", access_token_secret

print "checking oauth token access..."
resp = m.auth_checkAccessToken()


if resp[u'stat'] == u'ok':
    print "oauth successful."
    print
    print "Token Information:"
    for e, k in resp[u'Auth'][u'Token'].iteritems():
        print "    %s=%s" % (e, k)
    
    print "User Information:"
    for e, k in resp[u'Auth'][u'User'].iteritems():
        print "    %s=%s" % (e, k)
