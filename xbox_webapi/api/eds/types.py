from xbox_webapi.common.enum import Enum

class MediaItemType(Enum):
    XBOX360_GAME = "Xbox360Game"
    XBOX360_GAME_CONTENT = "Xbox360GameContent"
    XBOX360_GAME_DEMO = "Xbox360GameDemo"

    XBOX_GAME_TRIAL = "XboxGameTrial"
    XBOX_THEME = "XboxTheme"
    XBOX_ORIGINAL_GAME = "XboxOriginalGame"
    XBOX_GAMER_TILE = "XboxGamerTile"
    XBOX_ARCADE_GAME = "XboxArcadeGame"
    XBOX_GAME_CONSUMABLE = "XboxGameConsumable"
    XBOX_GAME_VIDEO = "XboxGameVideo"
    XBOX_GAME_TRAILER = "XboxGameTrailer"
    XBOX_BUNDLE = "XboxBundle"
    XBOX_XNA_GAME = "XboxXnaCommunityGame"
    XBOX_MARKETPLACE = "XboxMarketplace"
    XBOX_APP = "XboxApp"

    XBOXONE_GAME = "DGame"
    XBOXONE_GAME_DEMO = "DGameDemo"
    XBOXONE_CONSUMABLE = "DConsumable"
    XBOXONE_DURABLE = "DDurable"
    XBOXONE_APP = "DApp"
    XBOXONE_ACTIVITY = "DActivity"
    XBOXONE_NATIVE_APP = "DNativeApp"

    METRO_GAME = "MetroGame"
    METRO_GAME_CONTENT = "MetroGameContent"
    METRO_GAME_CONSUMABLE = "MetroGameConsumable"

    AVATAR_ITEM = "AvatarItem"

    MOBILE_GAME = "MobileGame"
    XBOX_MOBILE_PDLC = "XboxMobilePDLC"
    XBOX_MOBILE_CONSUMABLE = "XboxMobileConsumable"

    TV_SHOW = "TVShow"
    TV_EPISODE = "TVEpisode"
    TV_SERIES = "TVSeries"
    TV_SEASON = "TVSeason"

    MUSIC_ALBUM = "Album"
    MUSIC_TRACK = "Track"
    MUSIC_VIDEO = "MusicVideo"
    MUSIC_ARTIST = "MusicArtist"

    WEB_GAME = "WebGame"
    WEB_VIDEO = "WebVideo"
    WEB_VIDEO_COLLECTION = "WebVideoCollection"

    GAME_LAYER = "GameLayer"
    GAME_ACTIVITY = "GameActivity"
    APP_ACTIVITY = "AppActivity"
    VIDEO_LAYER = "VideoLayer"
    VIDEO_ACTIVITY = "VideoActivity"

    SUBSCRIPTION = "Subscription"


class MediaGroup(Enum):
    """
    GameType:
    Xbox360Game, XboxGameTrial, Xbox360GameContent, Xbox360GameDemo, XboxTheme, XboxOriginalGame,
    XboxGamerTile, XboxArcadeGame, XboxGameConsumable, XboxGameVideo, XboxGameTrailer, XboxBundle, XboxXnaCommunityGame,
    XboxMarketplace, AvatarItem, MobileGame, XboxMobilePDLC, XboxMobileConsumable, WebGame, MetroGame, MetroGameContent,
    MetroGameConsumable, DGame, DGameDemo, DConsumable, DDurable

    AppType: XboxApp, DApp
    MovieType: Movie
    TVType: TVShow (one-off TV shows), TVEpisode, TVSeries, TVSeason
    MusicType: Album, Track, MusicVideo
    MusicArtistType: MusicArtist
    WebVideoType: WebVideo, WebVideoCollection
    EnhancedContentType: GameLayer, GameActivity, AppActivity, VideoLayer, VideoActivity, DActivity, DNativeApp
    SubscriptionType: Subscription
    """
    GAME_TYPE = "GameType"
    APP_TYPE = "AppType"
    MOVIE_TYPE = "MovieType"
    TV_TYPE = "TVType"
    MUSIC_TYPE = "MusicType"
    MUSIC_ARTIST_TYPE = "MusicArtistType"
    WEB_VIDEO_TYPE = "WebVideoType"
    ENHANCED_CONTENT_TYPE = "EnhancedContentType"
    SUBSCRIPTION_TYPE = "SubscriptionType"

class ScheduleDetailsField(Enum):
    NAME = "Name"
    ID = "Id"
    IMAGES = "Images"
    DESCRIPTION = "Description"
    PARENTAL_RATING = "ParentalRating"
    PARENT_SERIES = "ParentSeries"
    SCHEDULE_INFO = "ScheduleInformation"

class Domain(Enum):
    XBOX_360 = "Xbox360"
    XBOX_ONE = "Modern"

class IdType(Enum):
    CANONICAL = "Canonical" # BING/MARKETPLACE
    XBOX_HEX_TITLE = "XboxHexTitle"
    SCOPED_MEDIA_ID = "ScopedMediaId"
    ZUNE_CATALOG = "ZuneCatalog"
    ZUNE_MEDIA_INSTANCE = "ZuneMediaInstance"
    AMG = "AMG"
    MEDIA_NET = "MediaNet"
    PROVIDER_CONTENT_ID = "ProviderContentId" # NETFLIX/HULU

class ClientType(Enum):
    C13 = "C13"
    COMMERCIAL_SERVICE = "CommercialService"
    COMPANION = "Companion"
    CONSOLE = "Console"
    EDITORIAL = "Editorial"
    FIRST_PARTY_APP = "1stPartyApp"
    MO_LIVE = "MoLive"
    WINDOWS_PHONE_7 = "PhoneROM"
    RECOMMENDATION_SERVICE = "RecommendationService"
    SAS = "SAS"
    SDS = "SDS"
    SUBSCRIPTION_SERVICE = "SubscriptionService"
    X8 = "X8"
    X13 = "X13"
    WEBBLEND = "Webblend"
    XBOX_COM = "XboxCom"

class DeviceType(Enum):
    XBOX360 = "Xbox360"
    XBOXONE = "XboxDurango"
    XBOX = "Xbox"
    IOS = "iOS"
    IPHONE = "iPhone"
    IPAD = "iPad"
    ANDROID = "Android"
    ANDROID_PHONE = "AndroidPhone"
    ANDROID_SLATE = "AndroidSlate"
    WIN_PC = "WindowsPC"
    WIN_PHONE = "WindowsPhone"
    SERVICE = "Service"
    WEB = "Web"