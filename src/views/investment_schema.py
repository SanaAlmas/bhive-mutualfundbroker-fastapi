import datetime

from pydantic import BaseModel
import uuid

class InvestmentViewSchema(BaseModel):
    investment_id: uuid.UUID
    scheme_name: str
    scheme_code: int
    units: float
    nav: float
    date: datetime.datetime
    current_value: float
    fund_family: str

class InvestmentCreateSchema(BaseModel):
    scheme_code: int
    units: float
    scheme_name: str
    nav: float
    date: datetime.datetime
    current_value: float
    fund_family: str

class InvestmentUpdateSchema(BaseModel):
    scheme_code: int
    units: float
    current_value: float
