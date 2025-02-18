import base64

import bcrypt


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return base64.b64encode(hashed).decode()


def validate_password(password: str, hashed_password: str) -> bool:
    hashed_bytes = base64.b64decode(hashed_password.encode())
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_bytes,
    )
