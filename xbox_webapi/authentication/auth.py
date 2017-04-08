import json
import requests
import re
import demjson
import logging
import io

import xml.dom.minidom as minidom

try:
    # Python 3
    from urllib.parse import urlparse, parse_qs
except ImportError:
    # Python 2
    from urlparse import urlparse, parse_qs

from xbox_webapi.authentication.two_factor import TwoFactorAuthentication
from xbox_webapi.authentication.token import Token, Tokenstore
from xbox_webapi.authentication.token import AccessToken, RefreshToken, UserToken, DeviceToken, TitleToken, XSTSToken
from xbox_webapi.common.exceptions import AuthenticationException
from xbox_webapi.common.userinfo import XboxLiveUserInfo

log = logging.getLogger('authentication')

class AuthenticationManager(object):
    def __init__(self, token_filepath=None):
        """
        Authenticate with Windows Live Server and Xbox Live.

        Args:
            token_filepath (str): path to json tokenfile

        In case Two-Factor authentication is requested from provided account, the user is asked for input via
        standard-input.
        """
        self.session = requests.session()
        self.authenticated = False
        self.token_filepath = token_filepath

    def load_token_files(self, ts):
        """
        Load Tokens from self.token_filepath IF NEEDED (e.g. passed tokens are invalid)

        Tokens passed to 'authenticate' as argument are always prioritized over tokens loaded from file

        Args:
            ts (object): Instance of :class:`Tokenstore`

        Returns:
            object: return instance of :class:`Tokenstore`
        """
        if not self.token_filepath:
            log.error("Called load_token_files without a supplied token_filepath to class-constructor")
            return ts

        try:
            with io.open(self.token_filepath, 'r') as f:
                json_file = json.load(f, encoding='utf-8')
        except Exception as e:
            log.error('Loading tokens from file failed! Msg: %s' % e)
            return ts

        def should_replace(token_arg, token_file):
            """Check if token from file is newer than from tokenstore"""
            if (not token_arg or not token_arg.is_valid) and \
                    token_file and token_file.is_valid:
                return True

        file_tokens = json_file.get('tokens')
        for token in file_tokens:
            t = Token.from_dict(token)
            log.info('Loaded token %s from file' % type(t))
            if isinstance(t, AccessToken) and should_replace(ts.access_token, t):
                ts.access_token = t
            elif isinstance(t, RefreshToken) and should_replace(ts.refresh_token, t):
                ts.refresh_token = t
            elif isinstance(t, UserToken) and should_replace(ts.user_token, t):
                ts.user_token = t
            elif isinstance(t, DeviceToken) and should_replace(ts.device_token, t):
                ts.device_token = t
            elif isinstance(t, TitleToken) and should_replace(ts.title_token, t):
                ts.title_token = t
            elif isinstance(t, XSTSToken) and should_replace(ts.xsts_token, t):
                ts.xsts_token = t

        file_userinfo = json_file.get('userinfo')
        if not ts.userinfo and file_userinfo:
            ts.userinfo = XboxLiveUserInfo.from_dict(file_userinfo)

        return ts

    def save_token_files(self, ts):
        """
        Save Tokens into self.token_filepath

        Args:
            ts (object): Instance of :class:`Tokenstore`

        Returns:
            None
        """
        if not self.token_filepath:
            log.error("Called save_token_files without a supplied token_filepath to class-constructor")
            return

        json_file = {
            'tokens': list(),
            'userinfo': None
        }

        tokens = [ts.access_token, ts.refresh_token, ts.user_token, ts.xsts_token]
        for token in tokens:
            json_file['tokens'].append(token.to_dict())

        json_file['userinfo'] = ts.userinfo.to_dict()

        with io.open(self.token_filepath, 'w') as f:
            json.dump(json_file, f, indent=2)

    def authenticate(self, email_address=None, password=None, ts=None, do_refresh=True):
        """
        Authenticate with Xbox Live using either tokens or user credentials.

        After being called, its property `authenticated` should be checked for success.

        Raises:
            AuthenticationException: When neither token and credential authentication is successful

        Args:
            email_address (str): Microsoft Account Email address
            password (str): Microsoft Account password
            ts (object): Instance of :class:`Tokenstore`
            do_refresh (bool): Refresh Access- and Refresh Token even if still valid, default: True

        Returns:
            object: On success return instance of :class:`Tokenstore`
        """

        full_authentication_required = False

        if not ts:
            log.debug('Creating new tokenstore')
            ts = Tokenstore()

        if self.token_filepath:
            ts = self.load_token_files(ts)

        try:
            # Refresh and Access Token
            if not do_refresh and ts.access_token and ts.refresh_token and \
                    ts.access_token.is_valid and ts.refresh_token.is_valid:
                pass
            else:
                ts.access_token, ts.refresh_token = self._windows_live_token_refresh(ts.refresh_token)

            # User Token
            if ts.user_token and ts.user_token.is_valid:
                pass
            else:
                ts.user_token = self._xbox_live_authenticate(ts.access_token)

            '''
            TODO: Fix
            # Device Token
            if ts.device_token and ts.device_token.is_valid:
                pass
            else:
                ts.device_token = self._xbox_live_device_auth(ts.access_token)

            # Title Token
            if ts.title_token and ts.title_token.is_valid:
                pass
            else:
                ts.title_token = self._xbox_live_title_auth(ts.device_token, ts.access_token)
            '''

            # XSTS Token
            if ts.xsts_token and ts.xsts_token.is_valid and ts.userinfo:
                self.authenticated = True
            else:
                ts.xsts_token, ts.userinfo = self._xbox_live_authorize(ts.user_token)
                self.authenticated = True
        except AuthenticationException:
            full_authentication_required = True

        # Authentication via credentials
        if full_authentication_required and email_address and password:
            ts.access_token, ts.refresh_token = self._windows_live_authenticate(email_address, password)
            ts.user_token = self._xbox_live_authenticate(ts.access_token)
            '''
            TODO: Fix
            ts.device_token = self._xbox_live_device_auth(ts.access_token)
            ts.title_token = self._xbox_live_title_auth(ts.device_token, ts.access_token)
            '''
            ts.xsts_token, ts.userinfo = self._xbox_live_authorize(ts.user_token)
            self.authenticated = True

        if not self.authenticated:
            raise AuthenticationException("AuthenticationManager was not able to authenticate "
                                          "with provided tokens or user credentials!")

        self.save_token_files(ts)
        return ts

    def _extract_js_object(self, body, obj_name):
        """
        Find a javascript object inside a html-page via regex.

        When it is found, convert it to a python-compatible dict.

        Args:
            body (str): The raw HTTP body to parse
            obj_name (str): The name of the javascript-object to find

        Returns:
            dict: Parsed javascript-object on success, otherwise `None`
        """
        server_data_re = r"%s(?:.*?)=(?:.*?)({(?:.*?)});" % (obj_name)
        matches = re.findall(server_data_re, body, re.MULTILINE | re.IGNORECASE | re.DOTALL)
        if len(matches):
            return demjson.decode(matches[0])

    def _windows_live_authenticate(self, email_address, password):
        """
        Internal method to authenticate with Windows Live, called by `self.authenticate`

        In case of required two-factor-authentication the respective routine is initialized and user gets asked for
        input of verification details.

        Args:
            email_address (str): Microsoft Account Email address
            password (str):  Microsoft Account password

        Raises:
            AuthenticationException: When two-factor-authentication fails or returned headers do not contain
            Access-/Refresh-Tokens.

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        response = self.__window_live_authenticate_request(email_address, password)

        proof_type = self._extract_js_object(response.content.decode("utf-8"), "PROOF.Type")
        if proof_type:
            log.info("Two Factor Authentication required!")
            twofactor = TwoFactorAuthentication(self.session)
            server_data = self._extract_js_object(response.content.decode("utf-8"), "ServerData")
            response = twofactor.authenticate(email_address, server_data)
            if not response:
                raise AuthenticationException("Two Factor Authentication failed!")

        if 'Location' not in response.headers:
            # we can only assume the login failed
            raise AuthenticationException("Could not log in with supplied credentials")

        # the access token is included in fragment of the location header
        location = urlparse(response.headers['Location'])
        fragment = parse_qs(location.fragment)

        access_token = AccessToken(fragment['access_token'][0], fragment['expires_in'][0])
        refresh_token = RefreshToken(fragment['refresh_token'][0])
        return access_token, refresh_token

    def _windows_live_token_refresh(self, refresh_token):
        """
        Internal method to refresh Windows Live Token, called by `self.authenticate`

        Raises:
            AuthenticationException: When provided Refresh-Token is invalid.

        Args:
            refresh_token (object): Instance of :class:`RefreshToken`

        Returns:
            tuple: If authentication succeeds, `tuple` of (AccessToken, RefreshToken) is returned
        """
        if refresh_token and refresh_token.is_valid:
            resp = self.__window_live_token_refresh_request(refresh_token)
            response = json.loads(resp.content.decode('utf-8'))

            if 'access_token' not in response:
                raise AuthenticationException("Could not refresh token via RefreshToken")

            access_token = AccessToken(response['access_token'], response['expires_in'])
            refresh_token = RefreshToken(response['refresh_token'])
            return access_token, refresh_token
        else:
            raise AuthenticationException("No valid RefreshToken")

    def _xbox_live_authenticate(self, access_token):
        """
        Internal method to authenticate with Xbox Live, called by `self.authenticate`

        Args:
            access_token (object): Instance of :class:`AccessToken`

        Raises:
            AuthenticationException: When provided Access-Token is invalid

        Returns:
            object: If authentication succeeds, returns :class:`UserToken`
        """
        if access_token and access_token.is_valid:
            json_data = self.__xbox_live_authenticate_request(access_token).json()
            return UserToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken")

    def _xbox_live_device_auth(self, access_token):
        """
         Internal method to authenticate Device with Xbox Live, called by `self.authenticate`

         Args:
             access_token (object): Instance of :class:`AccessToken`

         Raises:
             AuthenticationException: When provided Access-Token is invalid

         Returns:
             object: If authentication succeeds, returns :class:`DeviceToken`
         """
        if access_token and access_token.is_valid:
            json_data = self.__device_authenticate_request(access_token)
            print(json_data.status_code)
            print(json_data.headers)
            print(json_data.content)
            json_data = json_data.json()
            return DeviceToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken")

    def _xbox_live_title_auth(self, device_token, access_token):
        """
         Internal method to authenticate Device with Xbox Live, called by `self.authenticate`

         Args:
             device_token (object): Instance of :class:`DeviceToken`
             access_token (object): Instance of :class:`AccessToken`

         Raises:
             AuthenticationException: When provided Access-Token is invalid

         Returns:
             object: If authentication succeeds, returns :class:`TitleToken`
         """
        if access_token and access_token.is_valid and device_token and device_token.is_valid:
            json_data = self.__title_authenticate_request(device_token, access_token).json()
            return TitleToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
        else:
            raise AuthenticationException("No valid AccessToken/DeviceToken")

    def _xbox_live_authorize(self, user_token, device_token=None, title_token=None):
        """
        Internal method to authorize with Xbox Live, called by `self.authenticate`

        Args:
            user_token (object): Instance of :class:`UserToken`
            device_token (object): Instance of :class:`DeviceToken`
            title_token (object): Instance of :class:`TitleToken`

        Returns:
            tuple: If authentication succeeds, returns tuple of (:class:`XSTSToken`, :class:`XboxLiveUserInfo`)
        """
        if user_token and user_token.is_valid:
            json_data = self.__xbox_live_authorize_request(user_token, device_token, title_token).json()
            userinfo = json_data['DisplayClaims']['xui'][0]
            userinfo = XboxLiveUserInfo.from_dict(userinfo)

            xsts_token = XSTSToken(json_data['Token'], json_data['IssueInstant'], json_data['NotAfter'])
            return xsts_token, userinfo

    def __window_live_authenticate_request(self, email, password):
        """
        Authenticate with Windows Live Server.

        First, the Base-URL gets queried by HTTP-GET from a static URL. The resulting response holds a javascript-object
        containing Post-URL and PPFT parameter - both get used by the following HTTP-POST to attempt authentication by
        sending user-credentials in the POST-data.

        If the final POST-Response holds a 'Location' field in it's headers, the authentication can be considered
        successful and Access-/Refresh-Token are available.

        Args:
            email (str): Microsoft account email-address
            password (str): Corresponding password

        Returns:
            requests.Response: Response of the final POST-Request
        """

        base_url = 'https://login.live.com/oauth20_authorize.srf?'

        params = {
            'client_id': '0000000048093EE3',
            'redirect_uri': 'https://login.live.com/oauth20_desktop.srf',
            'response_type': 'token',
            'display': 'touch',
            'scope': 'service::user.auth.xboxlive.com::MBI_SSL',
            'locale': 'en',
        }
        resp = self.session.get(base_url, params=params)

        # Extract ServerData javascript-object via regex, convert it to proper JSON
        server_data = self._extract_js_object(resp.content.decode("utf-8"), "ServerData")
        # Extract PPFT value
        ppft = server_data.get('sFTTag')
        ppft = minidom.parseString(ppft).getElementsByTagName("input")[0].getAttribute("value")

        post_data = {
            'login': email,
            'passwd': password,
            'PPFT': ppft,
            'PPSX': 'Passpor',
            'SI': 'Sign in',
            'type': '11',
            'NewUser': '1',
            'LoginOptions': '1'
        }

        return self.session.post(server_data.get('urlPost'), data=post_data, allow_redirects=False)

    def __window_live_token_refresh_request(self, refresh_token):
        """
        Refresh the Windows Live Token by sending HTTP-GET Request containing Refresh-token in query to a static URL.

        Args:
            refresh_token (RefreshToken): :class:`RefreshToken from a previous Windows Live Authentication

        Returns:
            requests.Response: Response of HTTP-GET
        """
        base_url = 'https://login.live.com/oauth20_token.srf?'
        params = {
            'grant_type': 'refresh_token',
            'client_id': '0000000048093EE3',
            'scope': 'service::user.auth.xboxlive.com::MBI_SSL',
            'refresh_token': refresh_token.token,
        }

        return self.session.get(base_url, params=params)

    def __xbox_live_authenticate_request(self, access_token):
        """
        Authenticate with Xbox Live by sending HTTP-POST containing Windows-Live Access-Token to User-Auth endpoint.

        Args:
            access_token (AccessToken): :class:`AccessToken` from the Windows-Live-Authentication

        Returns:
           requests.Response: Response of HTTP-POST
        """
        url = 'https://user.auth.xboxlive.com/user/authenticate'
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.token,
            }
        }

        return self.session.post(url, json=data, headers=headers)

    def __xbox_live_authorize_request(self, user_token, device_token=None, title_token=None):
        """
        Authorize with Xbox Live by sending Xbox-Live User-Token via HTTP Post to the XSTS-Authorize endpoint.

        Args:
            user_token (UserToken): :class:`UserToken` from the Xbox-Live Authentication
            device_token (DeviceToken): :class:`DeviceToken` from Xbox-Live Device Authentication
            title_token (TitleToken): :class:`TitleToken` from Xbox-Live Title Authentication

        Returns:
            requests.Response: Response of HTTP-POST
        """
        url = 'https://xsts.auth.xboxlive.com/xsts/authorize'
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [user_token.token],
                "SandboxId": "RETAIL",
            }
        }

        if device_token:
            data["Properties"].update({"DeviceToken": device_token.token})
        if title_token:
            data["Properties"].update({"TitleToken": title_token.token})

        return self.session.post(url, json=data, headers=headers)

    def __title_authenticate_request(self, device_token, access_token):
        """
        Authenticate Title / App with Xbox Live.

        On successful authentication it might show as "Currently playing" to friends or followers.

        Args:
            device_token (Token): Device :class:`Token obtained by Device Authentication.
            access_token (Token): :class:`Token`

        Returns:
            requests.Response: Response of HTTP-POST
        """
        url = "https://title.auth.xboxlive.com"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "DeviceToken": device_token.token,
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.token
            }
        }

        return self.session.post(url, json=data, headers=headers)

    def __device_authenticate_request(self, access_token):
        """
        Authenticate your current device with Xbox Live.

        Args:
            access_token (Token): Access :class:`Token

        Returns:
            requests.Response: Response of HTTP-POST`
        """
        url = "https://device.auth.xboxlive.com/device/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": "http://auth.xboxlive.com",
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": access_token.token,
            }
        }

        return self.session.post(url, json=data, headers=headers)