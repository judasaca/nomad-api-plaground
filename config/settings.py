from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    api_base_path: str = Field("http://localhost:8000/fairdi/nomad/latest/api/v1")
    username: str = Field(..., alias="app_username")
    password: SecretStr

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = _Settings()
