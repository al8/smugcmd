This app is in development for now, so you'll need an api key to use this interface.
get one here: http://www.smugmug.com/hack/apikeys

When you have your api key + secret, you use it one of two ways,
  method A) put it in 'apikey.txt' using 'apikey_example.txt' as a reference.
  method B) within 'smugcmd_shared.py', modify values of CONSUMER_KEY and CONSUMER_SECRET in the designated location.

Then you need to authenticate using the enclosed oauth.


oauth works like this:
	obtain a request token
	authorize the request token (via URL login)
	use request token to get access token
	save access token to be used for subsequent accesses

the enclosed scripts handle this.
setup_step1_authorize_access.py:
	run this to authorize access to your account. It will open a URL to smugmug where you will login and allow this application to access your account. (If a webpage does not automatically open, a url is also printed to the console.)
setup_step2_get_access_token.py:
	after allowing access, use this script to obtain an access token. A file will be created in the appdir and this token will be used to access your smugmug account.
	keep this file safe; it contains information to access your smugmug account.

setup_step3_check_access.py:
	after step 1 and 2 are finished, use this script to check your access.


.... more later