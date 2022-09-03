from pydantic import BaseSettings

class Settings(BaseSettings):
    back_login : str 
    back_meals : str
    back_last_meal :str

    class Config:
        env_file= ".env"

settings = Settings()