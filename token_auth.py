import requests, json
import subprocess
import sys
import certifi
import urllib3

http = urllib3.PoolManager(
    cert_reqs="CERT_REQUIRED",
    ca_certs=certifi.where()
)

authorize_url = "https://auth.reefkinetics.com/identity/connect/authorize"
token_url = "https://auth.reefkinetics.com/identity/connect/token"

#callback url specified when the application was defined
callback_uri = "https://example.com/rb_user_authenticate_success/"

test_api_url = "https://webapi.reefkinetics.com/"

#client (application) credentials
client_id = 'dd'
client_secret = 'secret!!!'

#step A - simulate a request from a browser on the authorize_url - will return an authorization code after the user is
# prompted for credentials.

authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + '&redirect_uri=' + callback_uri + '&scope=READ'


print ("go to the following url on the browser and enter the code from the returned url: ")
print ("---  " + authorization_redirect_url + "  ---")
authorization_code = input('code: ')

# step I, J - turn the authorization code into a access token, etc
data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': callback_uri}
print ("requesting access token")
access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))

print ("response")
print (access_token_response.headers)
print ('body: ' + access_token_response.text)

# we can now use the access_token as much as we want to access protected resources.
tokens = json.loads(access_token_response.text)
access_token = tokens['access_token']
print ("access token: " + access_token)

api_call_headers = {'Authorization': 'Bearer ' + access_token}
api_call_response = requests.get(test_api_url, headers=api_call_headers, verify=False)

print (api_call_response.text)
