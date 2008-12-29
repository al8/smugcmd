import smugcmd_shared
from resp_print import resp_print

(access_token_key,access_token_secret) = smugcmd_shared.access_token_load()

m = smugcmd_shared.pysmug.SmugMug(
    oauth_consumer_key = smugcmd_shared.CONSUMER_KEY,
    oauth_consumer_secret = smugcmd_shared.CONSUMER_SECRET,
    oauth_access_token_key = access_token_key,
    oauth_access_token_secret = access_token_secret,
)


resp = m.albums_get()


if resp[u'stat'] == u'ok':
    resp_print(resp)
else:
    print "fail"
