import os
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str
    port: int


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "authentication" / "keys" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "authentication" / "keys" / "jwt-public.pem"
    algorithm: str
    expire_minutes: int


class ApiPrefix(BaseModel):
    auth: str = "/auth"
    receipt: str = "/receipt"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(
            os.path.dirname(os.path.dirname(__file__)), ".env.template"
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig
    db: DatabaseConfig
    auth_jwt: AuthJWT
    api_prefix: ApiPrefix = ApiPrefix()


settings = Settings()
