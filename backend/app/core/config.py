from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "ToolBox Backend"

    # DB：默认给一个可用的 PG 连接，.env 或环境变量可覆盖
    DATABASE_URL: str = "postgresql+psycopg://app:app123@localhost:5432/appdb"

    DATA_DIR: Path = Field(default_factory=lambda: Path("data").resolve())
    LOG_LEVEL: Literal["DEBUG","INFO","WARNING","ERROR","CRITICAL"] = "INFO"
    LOG_TO_FILE: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
