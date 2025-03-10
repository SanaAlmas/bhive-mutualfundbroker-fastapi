from fastapi import FastAPI
from src.routes.investment_routes import investment_router
from src.routes.user_routes import auth_router

def create_app() -> FastAPI:
    app_ = FastAPI(
    title='Mutual Fund Broker',
    description='Backend application for a mutual fund brokerage firm',
    contact={
        "name": "Sana Almas",
        "url": "https://github.com/SanaAlmas",
        "email": "sanaalmas19@gmail.com",
    },
    )
    return app_

app = create_app()

app.include_router(
    auth_router,
    prefix='/mfb/auth',
    tags=['auth']
)
app.include_router(
    investment_router,
    prefix="/mfb/investment",
    tags=['investment']
)