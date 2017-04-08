from six import string_types
from dateutil.parser import parse
from dateutil.tz import tzutc
from datetime import datetime, timedelta


class Token(object):
    def __init__(self, token, date_issued, date_valid):
        """
        Container for authentication tokens obtained from Windows Live / Xbox Live Servers, featuring validity checking.

        Args:
            token (str): The JWT Token
            date_issued (str/datetime): The date the token was issued. Just provide the current time if you do not
            have this info.
            date_valid (str/datetime): The date the token expires.

        Returns:
            Token: Instance of :class:`Token
        """
        self.token = token

        if isinstance(date_issued, string_types):
            date_issued = parse(date_issued)
        self.date_issued = date_issued

        if isinstance(date_valid, string_types):
            date_valid = parse(date_valid)
        self.date_valid = date_valid

    @classmethod
    def from_dict(cls, node):
        """
        Assemble a :class:`Token` object from a dict, for example from json config file.

        Args:
            node (dict): Token as `dict` object. Mandatory fields: 'token', 'date_issued', 'date_valid'

        Returns:
            Token: Instance of :class:`Token`

        """
        name = node['name']

        token_classes = {
            'AccessToken': AccessToken,
            'RefreshToken': RefreshToken,
            'UserToken': UserToken,
            'DeviceToken': DeviceToken,
            'TitleToken': TitleToken,
            'XSTSToken': XSTSToken
        }

        if name not in token_classes:
            raise ValueError('Invalid token type')

        token_cls = token_classes[name]
        instance = token_cls.__new__(token_cls)
        super(token_cls, instance).__init__(node['token'], node['date_issued'], node['date_valid'])
        return instance

    def to_dict(self):
        """
        Convert the `Token`-object to a `dict`-object, to use it in json-file for example.
        Returns:
            dict: The token formatted as dict.
        """
        return {
            'name': self.__class__.__name__,
            'token': self.token,
            'date_issued': self.date_issued.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            'date_valid': self.date_valid.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

    @property
    def is_valid(self):
        """
        Check if token is still valid.

        Returns:
            bool: True on success, False otherwise

        """
        return self.date_valid > datetime.now(tzutc())
    
    def __str__(self):
        return self.token


class AccessToken(Token):
    def __init__(self, token, expires_sec):
        """
        Container for storing Windows Live Access Token

        Subclass of :class:`Token`

        WARNING: Only invoke when creating a FRESH token
        Don't use to convert saved token into object
        Args:
            token (str): The JWT Access-Token
            expires_sec (int): The expiry-time in seconds
        """
        date_issued = datetime.now(tzutc())
        date_valid = date_issued + timedelta(seconds=int(expires_sec))
        super(AccessToken, self).__init__(token, date_issued, date_valid)


class RefreshToken(Token):
    def __init__(self, token):
        """
        Container for storing Windows Live Refresh Token.

        Subclass of :class:`Token`

        WARNING: Only invoke when creating a FRESH token!
        Don't use to convert saved token into object
        Refresh Token usually has a lifetime of 14 days

        Args:
            token (str): The JWT Refresh-Token
        """
        date_issued = datetime.now(tzutc())
        date_valid = date_issued + timedelta(days=14)
        super(RefreshToken, self).__init__(token, date_issued, date_valid)


class UserToken(Token):
    """
    Container for storing Xbox Live User Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass

class DeviceToken(Token):
    """
    Container for storing Xbox Live Device Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass

class TitleToken(Token):
    """
    Container for storing Xbox Live Title Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass

class XSTSToken(Token):
    """
    Container for storing Xbox Live XSTS Token.

    Subclass of :class:`Token`

    WARNING: Only invoke when creating a FRESH token!
    Don't use to convert saved token into object
    """
    pass

class Tokenstore(object):
    """
    Container to store all tokens (and userinfo) and pass them around easily

    Args:
        access_token (object): Windows Live Access Token, instance of :class:`AccessToken`
        refresh_token (object): Windows Live Refresh Token, instance of :class:`RefreshToken`
        user_token (object): Xbox Live User Token, instance of :class:`UserToken`
        device_token (object): Xbox Live Device Token, instance of :class:`DeviceToken`
        title_token (object): Xbox Live Title Token, instance of :class:`TitleToken`
        xsts_token (object): Xbox Live XSTS Token, instance of :class:`XSTSToken`
        userinfo (object): Userdata json node, instance of :class:`XboxLiveUserInfo`
    """
    def __init__(self, access_token=None, refresh_token=None, user_token=None, device_token=None, title_token=None,
                 xsts_token=None, userinfo=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.user_token = user_token
        self.device_token = device_token
        self.title_token = title_token
        self.xsts_token = xsts_token
        self.userinfo = userinfo
