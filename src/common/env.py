from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    redis_host: str
    redis_port:int
    redis_password:str
    secret_key:str


settings = Settings() # type: ignore