from xbox_webapi.api.eds.types import ScheduleDetailsField, MediaGroup

class EDSProvider(object):
    EDS_URL = "https://eds.xboxlive.com"
    HEADERS_EDS = {
        'Cache-Control': 'no-cache',
        'Accept': 'application/json',
        'Pragma': 'no-cache',
        'x-xbl-client-type': 'Companion',
        'x-xbl-client-version': '2.0',
        'x-xbl-contract-version': '3.2',
        'x-xbl-device-type': 'WindowsPhone',
        'x-xbl-isautomated-client': 'true'
    }

    SEPERATOR = "."

    def __init__(self, client):
        self.client = client

    def get_channel_list_download(self, lineup_id):
        url = self.EDS_URL + "/media/%s/tvchannels?" % self.client.lang.locale
        params = {"channelLineupId": lineup_id}
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    # start/endTime format: "2016-07-11T21:50:00.000Z"
    def get_schedule_download(self, lineup_id, start_time, end_time, max_items, skip_items):
        url = self.EDS_URL + "/media/%s/tvchannellineupguide?" % self.client.lang.locale
        desired = [
            ScheduleDetailsField.ID,
            ScheduleDetailsField.NAME,
            ScheduleDetailsField.IMAGES,
            ScheduleDetailsField.DESCRIPTION,
            ScheduleDetailsField.PARENTAL_RATING,
            ScheduleDetailsField.PARENT_SERIES,
            ScheduleDetailsField.SCHEDULE_INFO
        ]
        params = {
            "startTime": start_time,
            "endTime": end_time,
            "maxItems": max_items,
            "skipItems": skip_items,
            "channelLineupId": lineup_id,
            "desired": self.SEPERATOR.join(desired)
        }
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_browse_query(self, order_by, max_items, skip_items, **kwargs):
        url = self.EDS_URL + "/media/%s/browse?" % self.client.lang.locale
        params = {
            "orderBy": order_by,
            "maxItems": max_items,
            "skipItems": skip_items
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_recommendations(self, desired, **kwargs):
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)
        url = self.EDS_URL + "/media/%s/recommendations?" % self.client.lang.locale
        params = {
            "desiredMediaItemTypes": desired
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_related(self, id, desired, media_item_type, **kwargs):
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)
        url = self.EDS_URL + "/media/%s/related?" % self.client.lang.locale
        params = {
            "id": id,
            "desiredMediaItemTypes": desired,
            "MediaItemType": media_item_type
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_fields(self, desired, **kwargs):
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)
        url = self.EDS_URL + "/media/%s/fields?" % self.client.lang.locale
        params = {
            "desired": desired
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_details(self, ids, mediagroup, **kwargs):
        if isinstance(ids, list):
            ids = self.SEPERATOR.join(ids)
        url = self.EDS_URL + "/media/%s/details?" % self.client.lang.locale
        params = {
            "ids": ids,
            "MediaGroup": mediagroup
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_crossmediagroup_search(self, search_query, max_items, desired, target_devices, **kwargs):
        if isinstance(desired, list):
            desired = self.SEPERATOR.join(desired)
        url = self.EDS_URL + "/media/%s/crossMediaGroupSearch?" % self.client.lang.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": desired,
            "targetDevices": target_devices

        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_singlemediagroup_search(self, search_query, max_items, media_item_types, **kwargs):
        if isinstance(media_item_types, list):
            media_item_types = self.SEPERATOR.join(media_item_types)
        url = self.EDS_URL + "/media/%s/singleMediaGroupSearch?" % self.client.lang.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": media_item_types
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)
