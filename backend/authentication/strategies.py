from datetime import timedelta, datetime
from typing import Annotated

import jwt

from backend.config import settings


def encode_jwt(
    payload: dict,
    private_key=settings.auth_jwt.private_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
    expire_minutes=settings.auth_jwt.expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    if expire_timedelta:
        expire = now + expire_timedelta

    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: Annotated[str, None],
    public_key=settings.auth_jwt.public_key_path.read_text(),
    algorithm=settings.auth_jwt.algorithm,
) -> Annotated[dict, None]:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
