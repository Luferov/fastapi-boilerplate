from fastapi import APIRouter

from .schemas import HealthcheckResponseSchema

__all__ = ('router',)

router = APIRouter(prefix='/healthcheck', tags=['Healthcheck'])


@router.get(
    '',
    description='Application status',
    response_model=HealthcheckResponseSchema,
)
async def get_healthcheck_status() -> HealthcheckResponseSchema:
    return HealthcheckResponseSchema()
