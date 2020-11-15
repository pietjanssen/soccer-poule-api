import json

from tools.ResourceTools import requests_retry_session


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