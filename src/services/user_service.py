from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.models.db_models import User
from src.views.user_schema import UserViewSchema, UserCreateSchema
from src.services.utils import generate_password_hash

JTI_EXPIRY = 3600

class UserService:

    async def get_user_by_email(self, email: str, session: AsyncSession) -> UserViewSchema:
        statement = select(User).where(User.email==email)
        result = await session.execute(statement)
        user = result.scalars().first()
        return user

    async def create_user(self, user_data_dict: UserCreateSchema, session: AsyncSession) -> UserViewSchema:

        user_data_dict = user_data_dict.model_dump()
        password = user_data_dict["password"]
        if password:
            user_data_dict["password_hash"] = generate_password_hash(password)
            del user_data_dict["password"]  # Remove the plain password from the dictionary

        user = User(**user_data_dict)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user