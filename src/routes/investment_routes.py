from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from src.services.authorization_service import AccessTokenBearer
from src.errors import InvestmentNotFound, SchemeCodeAlreadyExists
from src.models.db_engine import get_session
from src.views.investment_schema import InvestmentViewSchema, InvestmentCreateSchema, InvestmentUpdateSchema
from src.services.investment_service import InvestmentService
from sqlmodel.ext.asyncio.session import AsyncSession
import requests

investment_router = APIRouter()
investment_service = InvestmentService()
access_token_bearer = AccessTokenBearer()


def handle_error(exception: Exception, message: str = "An unexpected error occurred", status_code: int = 500):
    raise HTTPException(status_code=status_code, detail=message)


@investment_router.get('/get-an-investment/{scheme_code}', response_model=InvestmentViewSchema,
                       status_code=status.HTTP_200_OK)
async def get_an_investment(scheme_code: int, session: AsyncSession = Depends(get_session),
                            token_details: dict = Depends(access_token_bearer)) -> dict:
    try:
        user_id = token_details.get('user')['user_id']
        investment = await investment_service.get_investment_by_user_id_scheme_code(user_id, scheme_code, session)

        if not investment:
            raise InvestmentNotFound()

        return investment
    except InvestmentNotFound:
        handle_error("Investment not found", status_code=404)
    except SQLAlchemyError as e:
        handle_error(e, "Database error", status_code=500)
    except Exception as e:
        handle_error(e)


@investment_router.get('/view-portfolio', response_model=List[InvestmentViewSchema], status_code=status.HTTP_200_OK)
async def get_portfolio(session: AsyncSession = Depends(get_session),
                        token_details: dict = Depends(access_token_bearer)) -> list:
    try:
        user_id = token_details.get('user')['user_id']
        investments = await investment_service.get_investments_by_user_id(user_id, session)

        if not investments:
            raise InvestmentNotFound()

        return investments
    except InvestmentNotFound:
        handle_error("No investments found", status_code=404)
    except SQLAlchemyError as e:
        handle_error(e, "Database error", status_code=500)
    except Exception as e:
        handle_error(e)


@investment_router.post('', response_model=InvestmentViewSchema, status_code=status.HTTP_201_CREATED)
async def create_an_investment(investment_data: InvestmentCreateSchema, session: AsyncSession = Depends(get_session),
                               token_details: dict = Depends(access_token_bearer)) -> dict:
    try:
        user_id = token_details.get('user')['user_id']
        existing_investment = await investment_service.get_investment_by_user_id_scheme_code(
            user_id, investment_data.scheme_code, session
        )

        if existing_investment:
            raise SchemeCodeAlreadyExists()

        investment = await investment_service.create_an_investment(investment_data, user_id, session)
        return investment
    except SchemeCodeAlreadyExists:
        handle_error("Scheme code already exists", status_code=400)
    except SQLAlchemyError as e:
        handle_error(e, "Database error", status_code=500)
    except Exception as e:
        handle_error(e)


@investment_router.patch('', response_model=InvestmentViewSchema, status_code=status.HTTP_200_OK)
async def update_an_investment(investment_data: InvestmentUpdateSchema, session: AsyncSession = Depends(get_session),
                               token_details: dict = Depends(access_token_bearer)) -> dict:
    try:
        user_id = token_details.get('user')['user_id']
        investment = await investment_service.update_an_investment(user_id, investment_data, session)

        if not investment:
            raise InvestmentNotFound()

        return investment
    except InvestmentNotFound:
        handle_error("Investment not found", status_code=404)
    except SQLAlchemyError as e:
        handle_error(e, "Database error", status_code=500)
    except Exception as e:
        handle_error(e)


@investment_router.delete('/delete-an-investment/{scheme_code}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_investment(scheme_code: int, session: AsyncSession = Depends(get_session),
                               token_details: dict = Depends(access_token_bearer)) -> None:
    try:
        user_id = token_details.get('user')['user_id']
        investment = await investment_service.delete_an_investment(user_id, scheme_code, session)

        if not investment:
            raise InvestmentNotFound()
    except InvestmentNotFound:
        handle_error("Investment not found", status_code=404)
    except SQLAlchemyError as e:
        handle_error(e, "Database error", status_code=500)
    except Exception as e:
        handle_error(e)


@investment_router.get('/get-json-data-RapidAPI', status_code=status.HTTP_200_OK)
async def get_RapidAPI_data_from_API(token_details: dict = Depends(access_token_bearer)):
    try:
        data = await investment_service.get_funds_from_RapidAPI()
        return {"message": "Data fetched successfully", "data": data}
    except requests.RequestException as e:
        handle_error(e, "Failed to fetch data from RapidAPI", status_code=502)
    except Exception as e:
        handle_error(e)


@investment_router.get('/get-all-fund-families', status_code=status.HTTP_200_OK)
async def get_RapidAPI_fund_families(token_details: dict = Depends(access_token_bearer)):
    try:
        data = await investment_service.get_famity_funds_from_RapidAPI()
        return {"message": "Fund families retrieved successfully", "data": data}
    except requests.RequestException as e:
        handle_error(e, "Failed to fetch fund families", status_code=502)
    except Exception as e:
        handle_error(e)


@investment_router.get('/get-fund-family-open-funds', status_code=status.HTTP_200_OK)
async def get_RapidAPI_fund_families(token_details: dict = Depends(access_token_bearer), fund_family: str = None):
    try:
        data = await investment_service.get_open_funds_by_family(fund_family)
        return {"message": "Open funds retrieved successfully", "data": data}
    except requests.RequestException as e:
        handle_error(e, "Failed to fetch open funds", status_code=502)
    except Exception as e:
        handle_error(e)

# update nav of all the investments
@investment_router.post('/update-all-navs', status_code=status.HTTP_200_OK)
async def update_all_navs_hourly(session: AsyncSession = Depends(get_session)):
    is_update_done = await investment_service.update_nav_for_all_investments(session)
    return is_update_done