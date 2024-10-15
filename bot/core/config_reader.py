from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class CacheConfig(BaseModel):
    url: str
class BotConfig(BaseModel):
    token_bot: SecretStr


class TableConfig(BaseModel):
    cred_file: SecretStr
    url_table: str


class Settings(BaseSettings):
    bot_config: BotConfig
    table_config: TableConfig
    cache_config: CacheConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


config = Settings()
