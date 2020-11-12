from pydantic import BaseModel


class Season(BaseModel):
    Id: str
    Name: str
    SeasonName: str
