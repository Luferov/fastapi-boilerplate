from src.core.use_cases import UseCaseProtocol

from ..schemas.users import UserResponseSchema
from ..services import UsersServiceProtocol

UsersUseCaseProtocol = UseCaseProtocol[list[UserResponseSchema]]


class UsersUseCaseImpl:
    def __init__(self, users_service: UsersServiceProtocol) -> None:
        self.users_service = users_service

    async def __call__(self) -> list[UserResponseSchema]:
        return [
            UserResponseSchema.model_validate(user.model_dump(), from_attributes=True)
            for user in await self.users_service.get_users()
        ]
