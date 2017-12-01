# Xbox-WebAPI

Xbox-WebAPI is a python library to authenticate with Xbox Live via your Microsoft Account and provides Xbox related Web-API.

Authentication via credentials or tokens is supported, Two-Factor-Authentication is also possible.

# Dependencies
* Python >= 3.4
* Libraries: requests, python-dateutil, demjson, six

# Installation
To install this library, execute the following via cmdline
```sh
python setup.py install
```

# Authentication
```py
import sys
from xbox_webapi.authentication.auth import AuthenticationManager
from xbox_webapi.common.exceptions import AuthenticationException

# Tokens will be saved on successful login
# That way credentials can be omitted next time
# Usage with valid tokens:
# auth_mgr = AuthenticationManager('tokens.json')
# try:
#     auth_mgr.authenticate()
# except AuthenticationException as e:
#     print('Tokens are expired! Err: %s' % e)
#     sys.exit(-1)

auth_mgr = AuthenticationManager('tokens.json')
try:
    tokenstore = auth_mgr.authenticate(email_address="user@live.com", password="password")
except AuthenticationException as e:
    print('Email/Password authentication failed! Err: %s' % e)
    sys.exit(-1)

# Tokenstore holds tokens and userinfo
print(tokenstore.refresh_token)
print(tokenstore.xsts_token)
print(tokenstore.userinfo)
```

# API usage
```py
import sys, json
from xbox_webapi.api.provider import XboxLiveClient

ts = tokenstore

xbl_client = XboxLiveClient(ts.userinfo.userhash, ts.xsts_token, ts.userinfo.xuid)
# For Xbox One
resp = xbl_client.eds.get_singlemediagroup_search("cuphead", 10, "DGame", domain="Modern")
# For 360
# xbl_client.eds.get_singlemediagroup_search("skate", 10, "Xbox360Game", domain="Xbox360")
if resp.status_code != 200:
    print("Invalid EDS details response")
    sys.exit(-1)

print(json.dumps(resp.json(), indent=2))

```

### Documentation

Soon.. maybe...
