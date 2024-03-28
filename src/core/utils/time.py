"""
Модель работы с датами.
"""

import datetime


async def ts_now() -> float:
    """
    Возвращает текущий timestamp по GTM.

    :return: Значение в секундах
    """
    return datetime.datetime.now(datetime.timezone.utc).timestamp()
