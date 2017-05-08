class GamerpicsProvider(object):
    GAMERPICS_URL = "https://gamerpics.xboxlive.com"
    HEADERS_GAMERPICS = {
        'x-xbl-client-type': 'Durango',
        'x-xbl-client-version': '0',
        'x-xbl-contract-version': '1',
        'x-xbl-device-type': 'Console'
    }

    def __init__(self, client):
        self.client = client

    def download_gamerpic(self):
        url = self.GAMERPICS_URL + "/users/me/gamerpic"
        return self.client.session.get(url, headers=self.HEADERS_GAMERPICS)

    def upload_gamerpic(self, png_data):
        url = self.GAMERPICS_URL + "/users/me/gamerpic"
        return self.client.session.post(url, data=png_data, headers=self.HEADERS_GAMERPICS)