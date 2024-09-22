from typing import Union

from pydantic import BaseModel


# note: always use BaseModel to trigger Pydantic checking

class ExampleReq(BaseModel):
    username: str
    password: str
    email: str
    full_name: Union[str, None] = None


class Example:
    id: int
    username: str
    password: str
    email: str
    full_name: Union[str, None] = None

    def __init__(self, req: ExampleReq, user_id: int):
        self.id = user_id
        self.username = req.username
        self.password = req.password
        self.email = req.email
        self.full_name = req.full_name


class ExampleResp(BaseModel):
    id: int
    username: str
    email: str
    full_name: Union[str, None] = None

    @staticmethod
    def new(e: Example):
        return ExampleResp(
            id=e["id"],
            username=e["username"],
            email=e["email"],
            full_name=e["full_name"],
        )
