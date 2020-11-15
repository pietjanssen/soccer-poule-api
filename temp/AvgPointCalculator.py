import json

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from models.Match import Match


def requests_retry_session(retries=3, backoff_factor=5, status_forcelist=(500, 502, 503, 504), session=None):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def refresh_data():
    """
    Download and save new Feyenoord data to output.json()
    """
    url = "https://www.feyenoord.nl/api/matches/results"
    response = requests_retry_session().get(url=url)
    response.raise_for_status()
    results = response.json()
    with open('output.json', 'w') as outfile:
        json.dump(results, outfile)


class AvgPointCalculator:

    def __init__(self, refresh=False):
        if refresh:
            refresh_data()

    outfile = open('src/output.json', 'r')
    data = json.load(outfile)

    # Convert json to list of objects (for validation)
    matches: [Match] = []
    for match in data:
        matches.append(Match(**match))