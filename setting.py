from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PLUGSHARE_URL: str = "https://api.plugshare.com/v3"
    STATION_LIST_LINK_BASE: str = 'https://mc.chargepoint.com/map-prod/v2'
    STATION_INFO_LINK_BASE: str = 'https://mc.chargepoint.com/map-prod/v3/station/info'
    COMMENTS_LINK_BASE: str = 'https://account.chargepoint.com/account/v1/driver/tip/'