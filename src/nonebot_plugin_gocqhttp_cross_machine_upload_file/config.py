from nonebot import get_driver
from pydantic import BaseSettings, root_validator


class Config(BaseSettings):
    callback_host: str = "127.0.0.1"
    callback_port: int

    @root_validator(pre=True, allow_reuse=True)
    def callback_validator(cls, values):
        if "callback_port" not in values:
            values["callback_port"] = values.get("port", None)
        return values

    class Config:
        extra = "ignore"


conf = Config(**get_driver().config.dict())
