from typing import Optional

from pydantic import BaseModel


class Identities(BaseModel):
    email: Optional[str]


class Firebase(BaseModel):
    identities: Identities
    sign_in_provider: str


class User(BaseModel):
    iss: str
    aud: str
    auth_time: int
    user_id: str
    sub: str
    iat: int
    exp: int
    email: str
    email_verified: str
    firebase: Firebase
    uid: str
