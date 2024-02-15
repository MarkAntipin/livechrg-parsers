from pathlib import Path

import dotenv
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class Settings(BaseSettings):
    LIVE_CHARGE_AUTH_TOKEN: str
    LIVE_CHARGE_BASE_URL: str = 'https://api.livechrg.com'

    CHARGE_POINT_AUTH_TOKEN: str
    CHARGE_POINT_BASE_URL: str = 'https://mc.chargepoint.com'

    CHARGE_POINT_COMMENTS_URL: str = 'https://account-eu.chargepoint.com'
    PLUG_SHARE_BASE_URL: str = 'https://api.plugshare.com/v3'

    class Config:
        case_sensitive = False


settings = Settings()
