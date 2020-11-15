from typing import Optional

from pydantic import BaseModel


class AwayTeam(BaseModel):
    Id: str
    Name: str
    ShortName: str
    Stadium: str
    City: str
    isFeyenoordTeam: Optional[bool]
    TeamName: str
    Logo: str