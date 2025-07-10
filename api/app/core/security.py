from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # Ensure subject is serializable, typically user ID or username
    # Payload can include other claims like roles, permissions etc.
    # For this project, payload should include user_id and role.
    # The 'sub' (subject) claim is standard for the principal.
    # Let's assume 'subject' here is a dictionary like {"user_id": id, "role": "role_name"}
    # or just user_id and role is fetched separately.
    # The task AUTH-01 states: "token payload should include user_id, role, and exp."

    to_encode = {"exp": expire}
    if isinstance(subject, dict):
        to_encode.update(subject) # subject contains user_id and role
    else:
        to_encode["sub"] = str(subject) # Fallback if subject is just a string/id

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError: # Catches various errors like ExpiredSignatureError, InvalidTokenError
        return None

# Example of how to structure the subject for the token based on requirements:
# access_token_data = {
#     "user_id": user.id,
#     "role": user_role_name, # This needs to be determined (e.g., first role, or a primary role)
#     # "sub": user.username # Optionally, if 'sub' should be username
# }
# token = create_access_token(subject=access_token_data)
