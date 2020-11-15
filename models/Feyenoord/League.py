from typing import Optional

from pydantic import BaseModel

from .Season import Season


class League(BaseModel):
    Id: str
    Name: str
    LeagueName: str
    LeagueType: str
    Logo: Optional[str]
    Season: Season
