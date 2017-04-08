class MediaGroup(object):
    GAME_TYPE = "GameType"
    APP_TYPE = "AppType"
    MOVIE_TYPE = "MovieType"
    TV_TYPE = "TVType"
    MUSIC_TYPE = "MusicType"
    MUSIC_ARTIST_TYPE = "MusicArtistType"
    WEB_VIDEO_TYPE = "WebVideoType"
    ENHANCED_CONTENT_TYPE = "EnhancedContentType"
    SUBSCRIPTION_TYPE = "SubscriptionType"

class ScheduleDetailsField(object):
    NAME = "Name"
    ID = "Id"
    IMAGES = "Images"
    DESCRIPTION = "Description"
    PARENTAL_RATING = "ParentalRating"
    PARENT_SERIES = "ParentSeries"
    SCHEDULE_INFO = "ScheduleInformation"

class EDSProvider(object):
    BASE_URL = "https://eds.xboxlive.com"
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

    EDS_PARTNER_IDTYPE_QUERY_STRING = "ScopeIdType=Title&ScopeId=%08X&idType=ScopedMediaId&desiredMediaItemTypes=Movie.TVShow.TVEpisode.TVSeries.TVSeason"
    EDS_XBOXONE_ID_IDTYPE_QUERY_STRING = "idType=Canonical&desiredMediaItemTypes=DGame.DGameDemo.DApp"
    EDS_XBOXONE_MUSIC_IDTYPE_QUERY_STRING = "idType=ZuneCatalog&desiredMediaItemTypes=MusicVideo.MusicArtist.Track.Album"
    EDS_XBOXONE_SEASON_TO_SERIES_ID_IDTYPE_QUERY_STRING = "idType=Canonical&desiredMediaItemTypes=TvSeason"
    EDS_XBOXONE_TITLE_IDTYPE_QUERY_STRING = "idType=XboxHexTitle&desiredMediaItemTypes=DGame.DGameDemo.DApp"
    EDS_XBOXONE_VIDEO_IDTYPE_QUERY_STRING = "idType=ZuneCatalog&desiredMediaItemTypes=Movie.TvShow.TvSeries.TvEpisode.TvSeason"

    ENFORCE_AVAILABILITY_PARAMETER = "&EnforceAvailability=true&conditionsets=action_browse"

    def __init__(self, client):
        self.client = client

    def get_channel_list_download(self, lineup_id):
        url = self.BASE_URL + "/media/%s/tvchannels?" % self.client.lang.locale
        params = {"channelLineupId": lineup_id}
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    # start/endTime format: "2016-07-11T21:50:00.000Z"
    def get_schedule_download(self, lineup_id, start_time, end_time, max_items, skip_items):
        url = self.BASE_URL + "/media/%s/tvchannellineupguide?" % self.client.lang.locale
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
        url = self.BASE_URL + "/media/%s/browse?" % self.client.lang.locale
        params = {
            "orderBy": order_by,
            "maxItems": max_items,
            "skipItems": skip_items
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_recommendations(self, desired_media_item_types, **kwargs):
        url = self.BASE_URL + "/media/%s/recommendations?" % self.client.lang.locale
        params = {
            "desiredMediaItemTypes": self.SEPERATOR.join(desired_media_item_types)
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_related(self, id, desired_media_item_types, media_item_type, **kwargs):
        url = self.BASE_URL + "/media/%s/related?" % self.client.lang.locale
        params = {
            "id": id,
            "desiredMediaItemTypes": desired_media_item_types,
            "MediaItemType": media_item_type
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_fields(self, desired, **kwargs):
        url = self.BASE_URL + "/media/%s/fields?" % self.client.lang.locale
        params = {
            "desired": self.SEPERATOR.join(desired)
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_details(self, id_list, mediagroup, **kwargs):
        if len(id_list) > 10:
            raise Exception('id_list length exceeds 10. Supply fewer please!')

        url = self.BASE_URL + "/media/%s/details?" % self.client.lang.locale
        params = {
            "ids": self.SEPERATOR.join(id_list),
            "MediaGroup": mediagroup
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_crossmediagroup_search(self, search_query, max_items, desired_media_item_types,
                                   target_devices, domain, **kwargs):
        url = self.BASE_URL + "/media/%s/crossMediaGroupSearch?" % self.client.lang.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": desired_media_item_types,
            "targetDevices": target_devices,
            "domain": domain

        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)

    def get_singlemediagroup_search(self, search_query, max_items, desired_media_item_types, **kwargs):
        url = self.BASE_URL + "/media/%s/singleMediaGroupSearch?" % self.client.lang.locale
        params = {
            "q": search_query,
            "maxItems": max_items,
            "desiredMediaItemTypes": desired_media_item_types,
        }
        params.update(kwargs)
        return self.client.session.get(url, params=params, headers=self.HEADERS_EDS)