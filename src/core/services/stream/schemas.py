from enum import StrEnum, auto


class EventType(StrEnum):
    """
    Топики для процессинга.
    """

    AUDIO_PROCESSING = auto()
    TEXT_PROCESSING = auto()
