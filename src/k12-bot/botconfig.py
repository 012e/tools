from typing import TypedDict


class BotConfig(TypedDict):
    username: str
    password: str
    browser: str
    manual: bool
    max_attemp: int
