from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from src.clients.investment_client import get_openended_schemes_codes, get_fund_list_RapidAPI
from src.views.investment_schema import InvestmentCreateSchema, InvestmentUpdateSchema
from src.models.db_models import Investment
from sqlmodel import select, desc, and_


class InvestmentService:

    async def get_all_investments(self, session: AsyncSession):
        statement = select(Investment).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_investment_by_user_id_scheme_code(self, user_id: str, scheme_code: int, session: AsyncSession):
        statement = select(Investment).where(and_(Investment.user_id == user_id, Investment.scheme_code == scheme_code)).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.first()

    async def get_investments_by_user_id(self, user_id: str, session: AsyncSession):
        statement = select(Investment).where(and_(Investment.user_id == user_id)).order_by(desc(Investment.created_at))
        result = await session.exec(statement)
        return result.all()

    async def create_an_investment(self, investment_data: InvestmentCreateSchema, user_id: str, session: AsyncSession):

        investment_data_dict = investment_data.model_dump()
        print(f"investment details: {str(investment_data_dict)}")
        investment = Investment(**investment_data_dict)
        investment.user_id = user_id

        # add to the db
        session.add(investment)
        await session.commit()
        await session.refresh(investment)

        return investment

    # update an investment, allowed only for units
    async def update_an_investment(self, user_id: str, investment_data: InvestmentUpdateSchema, session: AsyncSession):

        # get the investment details
        investment = await self.get_investment_by_user_id_scheme_code(user_id, investment_data.scheme_code, session)

        # if investment not found
        if not investment:
            return None

        # convert investment data into a dictionary
        investment_data_dict = investment_data.model_dump()

        # update the attributes
        for key, value in investment_data_dict.items():
            setattr(investment, key, value)

        await session.commit()
        await session.refresh(investment)

        return investment

    # delete an investment
    async def delete_an_investment(self, user_id: str, scheme_code: str, session: AsyncSession):
        # get the investment details
        investment = await self.get_investment_by_user_id_scheme_code(user_id, scheme_code, session)

        # if investment not found
        if not investment:
            return None

        # delete the investment from db
        await session.delete(investment)
        await session.commit()
        return investment

    # update all nav values of investments
    async def update_nav_for_all_investments(self, session: AsyncSession):

        # get all investments
        investments = await self.get_all_investments(session)

        # update the current nav value and current_value of units
        try:
            for investment in investments:
                latest_mutual_fund_info = await get_openended_schemes_codes(investment.scheme_code)
                date_ = datetime.strptime(latest_mutual_fund_info['Date'], "%d-%b-%Y")
                investment.date = date_.strftime("%Y-%m-%d")
                investment.nav = round((latest_mutual_fund_info['Net_Asset_Value']), 4)
                investment.current_value = round((latest_mutual_fund_info['Net_Asset_Value'] * investment.units), 4)
                session.add(investment)

            await session.commit()

            print("Done updating investments every hour...")

            return {
                'message': 'All NAVs have been updated successfully.'
            }
        except Exception as e:
            print(f"Exception occurred while updating the NAV details: {str(e)}")
            return {
                'message': 'Update not successful'
            }


    async def get_funds_from_RapidAPI(self):
        try:
            queries = {}
            data = await get_fund_list_RapidAPI(queries)
            return data
        except Exception as e:
            print(f"Error reading JSON from file: {str(e)}")
            return {
                "message" : "Error while fetching"
            }

    async def get_famity_funds_from_RapidAPI(self):
        try:
            queries = {}
            data = await get_fund_list_RapidAPI(queries)

            family_funds = list(set([item["Mutual_Fund_Family"] for item in data['data']]))
            return family_funds
        except Exception as e:
            print(f"Error reading JSON from file: {str(e)}")
            return {
                "message" : "Error while fetching"
            }

    async def get_open_funds_by_family(self, fund_family):
        try:
            queries = {"Mutual_Fund_Family" : fund_family}
            data = await get_fund_list_RapidAPI(queries)
            return data
        except Exception as e:
            print(f"Error reading JSON from file: {str(e)}")
            return {
                "message" : "Error while fetching"
            }
