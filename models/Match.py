import datetime
from typing import Optional

from pydantic import BaseModel
from .League import League
from .HomeTeam import HomeTeam
from .AwayTeam import AwayTeam


class Match(BaseModel):
    Id: str
    HomeTeam: HomeTeam
    AwayTeam: AwayTeam
    Score: str
    League: League
    Date: datetime.datetime
    TicketsAvailable: bool
    ShowTicketsButton: bool
    Result: str
    Hashtag: Optional[str]
    MatchcenterLink: Optional[str]
    TicketshopLink: Optional[str]
    TicketInformationLink: Optional[str]