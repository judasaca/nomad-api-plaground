from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    api_base_path: str = Field("localhost:3000")

    model_config = SettingsConfigDict()


settings = _Settings()
