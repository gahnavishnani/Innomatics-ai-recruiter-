from pydantic_settings import BaseSettings 

class Setings(BaseSettings):
    openai_api_key : str

    class Config:
        env_file = ".env"

        settings = Settings()