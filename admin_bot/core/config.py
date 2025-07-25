from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class AdminBotConfig(BaseModel):
    token_bot: str
    super_admin_id: str
    initial_ids: str
    
class AdminImgConfig(BaseModel):
    path: str
    
class YuanRateConfig(BaseModel):
    yuan_rate: int | float

class ClosestDateConfig(BaseModel):
    date: str


class Config(BaseSettings):
    admin_bot_config: AdminBotConfig
    admin_image_config: AdminImgConfig
    yuan_rate_config: YuanRateConfig
    closest_date_config: ClosestDateConfig

    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    
    
settings = Config()
