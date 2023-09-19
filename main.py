from typing import Annotated
from fastapi import Depends, FastAPI, Query
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return fake_decode_token(token)


UserDep = Annotated[User, Depends(get_current_user)]


@app.get("/users/me")
async def read_items(me: UserDep):
    return me
