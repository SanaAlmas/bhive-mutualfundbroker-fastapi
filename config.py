from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    RAPID_API_URL: str
    RAPID_API_KEY: str
    RAPID_API_HOST: str
    REDIS_URL: str = 'redis://localhost:6379/0'
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    DOMAIN: str

    class Config:
        env_file = '.env'
        extra = 'ignore'

config_obj = Settings()