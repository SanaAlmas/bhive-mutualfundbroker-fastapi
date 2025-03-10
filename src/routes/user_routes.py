from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from src.services.authorization_service import get_current_user
from src.services.utils import create_access_token, verify_password_hash
from src.errors import UserAlreadyExists, InvalidCredentials
from src.models.db_engine import get_session, commit_session
from src.services.user_service import UserService
from src.views.user_schema import UserViewSchema, UserCreateSchema, UserLoginSchema, UserInvestmentSchemaView
from sqlalchemy.ext.asyncio.session import AsyncSession

# Token Expiry Time
REFRESH_TOKEN_EXPIRY = 2

# Initialize Router and Services
auth_router = APIRouter()
user_service = UserService()

def handle_error(exception: Exception, message: str = "An unexpected error occurred", status_code: int = 500):
    raise HTTPException(status_code=status_code, detail=message)


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    try:
        email = user_data.email
        is_user_exists = await user_service.get_user_by_email(email, session)

        if is_user_exists:
            raise UserAlreadyExists()

        user = await user_service.create_user(user_data, session)

        return JSONResponse(
            content={
                "message": "Account created successfully! Check email to verify your account.",
                "status": "success",
                "user": {
                    "email": user.email,
                    "user_id": str(user.user_id)
                }
            },
            status_code=201
        )

    except UserAlreadyExists:
        handle_error("User with this email already exists.", status_code=400)
    except SQLAlchemyError as e:
        handle_error(e, "Database error occurred", status_code=500)
    except Exception as e:
        handle_error(e)


@auth_router.post('/login')
async def login_user(user_data: UserLoginSchema, session: AsyncSession = Depends(get_session)) -> JSONResponse:
    try:
        email = user_data.email
        password = user_data.password

        user = await user_service.get_user_by_email(email, session)

        if user and verify_password_hash(password, user.password_hash):
            access_token = create_access_token(
                user_data={'email': user.email, 'user_id': str(user.user_id)},
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
                refresh=False
            )

            await commit_session(session)

            return JSONResponse(
                content={
                    "message": "Login Successful",
                    "status": "success",
                    "user": {
                        "email": user.email,
                        "user_id": str(user.user_id)
                    }
                },
                status_code=200,
                headers={"Authorization": f"Bearer {access_token}"}
            )

        raise InvalidCredentials()

    except InvalidCredentials:
        handle_error("Invalid email or password", status_code=401)
    except SQLAlchemyError as e:
        handle_error(e, "Database error occurred", status_code=500)
    except Exception as e:
        handle_error(e)

#
# @auth_router.post('/logout')
# async def logout_user() -> JSONResponse:
#     """Handles user logout."""
#     return JSONResponse(
#         content={"message": "Logout successful."},
#         status_code=status.HTTP_200_OK
#     )


@auth_router.get('/me', response_model=UserInvestmentSchemaView)
async def get_current_user_details(current_user: UserViewSchema = Depends(get_current_user)) -> UserInvestmentSchemaView:
    return current_user


@auth_router.get('/welcome')
async def welcome_message():
    return {"message": "Welcome to Bhive MFB App"}
