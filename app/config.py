from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = getenv('API_V1', '/api/v1')

    POSTGRES_DB: str = getenv('POSTGRES_DB', 'test')
    POSTGRES_HOST: str = getenv('POSTGRES_HOST', '127.0.0.1')
    POSTGRES_PORT: int = getenv('POSTGRES_PORT', '5432')
    POSTGRES_USER: str = getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD: str = getenv('POSTGRES_PASSWORD', 'qwerty')
    POSTGRES_ENGINE_URI: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
                               f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    REDIS_HOST: str = getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT: int = getenv('REDIS_PORT', '6379')
    REDIS_TTL: int = getenv('REDIS_TTL', '86400')

    JWT_KEY: str = getenv('JWT_KEY', "P9;FrLVK,}tY:RHaR[2z2|]/Sfvn:1OZcDvs1p`C7C<h0BhFGM8e2}05mal:I9ZOx{{W6X[6v3Nh2m/;S|xOYSeA9wl9|6.aJ.J{.--atoJT7KREiTWH=WSf?bvL{Dg")


settings = Settings()
