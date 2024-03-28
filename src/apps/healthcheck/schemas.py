from pydantic.dataclasses import dataclass


@dataclass
class HealthcheckResponseSchema:
    status: str = 'OK'
