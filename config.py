# Храним все данные о подключениях к различным базам, почтам и т.д.


from pydantic import BaseSettings



class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str


    SECRET_KEY: str # JWT # bash: openssl rand -base64 32
    ALGORITHM: str  # JWT


    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
