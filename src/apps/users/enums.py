from enum import StrEnum, auto


class UsersProviderEnum(StrEnum):
    postgres = auto()
    redis = auto()
