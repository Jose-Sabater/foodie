from pydantic import BaseSettings


class Settings(BaseSettings):
    back_login: str
    back_meals: str
    back_last_meal: str
    register_url: str
    flask_secret_key: str

    class Config:
        env_file = ".env"


settings = Settings()
