from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from src.services.utils import decode_access_token
from fastapi import Request, Depends
from src.services.user_service import UserService
from src.errors import InvalidToken, AccessTokenRequired
from src.models.db_engine import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.views.user_schema import UserInvestmentSchemaView
from src.errors import UserNotFound

user_service = UserService()

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:

        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_access_token(token)

        if not self.token_valid(token):
            raise InvalidToken()
        self.verify_token_data(token_data)
        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_access_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError(
            "Please Override this method in child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise AccessTokenRequired()

access_token_bearer = AccessTokenBearer()

async def get_current_user(token_details: dict = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)) -> UserInvestmentSchemaView:
    user_email = token_details['user']['email']
    user = await user_service.get_user_by_email(user_email, session)
    if not user:
        raise UserNotFound()
    return user