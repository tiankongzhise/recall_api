from pydantic_settings import BaseSettings

from typing import Dict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RETRY_COUNT: int = 3
    RETRY_DELAY: int = 1 # seconds

    FORWARD_RULES: Dict[str, str] = {
        "baidu": "http://bdapi.hnzzzsw.com",
        # Add other channels here in the future
        # "another_channel": "http://another_api.example.com",
    }

settings = Settings()