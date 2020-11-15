import json
from typing import List

from fastapi import APIRouter, Depends

from models.User import User
from tools.Firebase import get_current_user
from tools.ResourceTools import requests_retry_session
from models.Feyenoord.Match import Match

router = APIRouter()


def refresh_feyenoord_data():
    """
    Download and save new Feyenoord data to output.json()
    """
    url = "https://www.feyenoord.nl/api/matches/results"
    response = requests_retry_session().get(url=url)
    response.raise_for_status()
    results = response.json()
    with open('output.json', 'w') as outfile:
        json.dump(results, outfile)


@router.get("/feyenoord", response_model=List[Match])
def get_feyenoord_match_results(renew: bool = False, user: User = Depends(get_current_user)):
    """
    Get Feyenoord match results
    """

    if renew:
        refresh_feyenoord_data()

    try:
        outfile = open('src/output.json', 'r')
    except OSError:
        refresh_feyenoord_data()
        outfile = open('src/output.json', 'r')
    data = json.load(outfile)
    return data
