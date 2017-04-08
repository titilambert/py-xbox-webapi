class XboxLiveUserInfo(object):
    """Container for userinfo, received by Xbox Live Authorization"""
    def __init__(self, xuid, userhash, gamertag, age_group, privileges, user_privileges):
        self.xuid = xuid
        self.userhash = userhash
        self.gamertag = gamertag
        self.age_group = age_group
        self.privileges = privileges
        self.user_privileges = user_privileges

    @classmethod
    def from_dict(cls, node):
        """Fill class via JSON node"""
        return cls(node['xid'], node['uhs'], node['gtg'], node['agg'], node['prv'], node['usr'])

    def to_dict(self):
        """Return userinfo as dict"""
        return {
            'xid': self.xuid,
            'uhs': self.userhash,
            'gtg': self.gamertag,
            'agg': self.age_group,
            'prv': self.privileges,
            'usr': self.user_privileges
        }