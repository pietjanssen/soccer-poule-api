import json

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from models.Match import Match


def main():
    # Download new data
    # refresh_data()

    with open('src/output.json', 'r') as outfile:
        data = json.load(outfile)

        # Convert json to list of objects (for validation)
        matches: [Match] = []
        for match in data:
            matches.append(Match(**match))

        # Filter distinct leagues
        distinct_leagues = []
        for match in matches:
            if match.League.LeagueType and match.League.LeagueType not in distinct_leagues:
                distinct_leagues.append(match.League.LeagueType)

        # Create a selection screen for the user
        for index, distinct_league in enumerate(distinct_leagues):
            print(index, distinct_league)
        print(len(distinct_leagues), "All")
        league_result = int(input("Please select one of the previous Leagues: "))

        # Filter by League selection
        if 0 <= league_result <= len(distinct_leagues):
            if league_result != len(distinct_leagues):
                matches = list(filter(lambda x: x.League.LeagueType == distinct_leagues[league_result], matches))
        else:
            raise IndexError("Please select one of the previous Leagues.")

        # Filter by seasons
        distinct_seasons = []
        for match in matches:
            if match.League.Season.SeasonName and match.League.Season.SeasonName not in distinct_seasons:
                distinct_seasons.append(match.League.Season.SeasonName)

        # Create a selection screen for the user
        for index, distinct_season in enumerate(distinct_seasons):
            print(index, distinct_season)
        print(len(distinct_seasons), "All")
        season_result = int(input("Please select one of the previous Seasons: "))

        # Filter by Season selection
        if 0 <= season_result <= len(distinct_seasons):
            if season_result != len(distinct_seasons):
                matches = list(filter(lambda x: x.League.Season.SeasonName == distinct_seasons[season_result], matches))
        else:
            raise IndexError("Please select one of the previous Leagues.")

        # Filter by teams
        distinct_home_teams = []
        for match in matches:
            if match.HomeTeam and match.HomeTeam.ShortName not in distinct_home_teams:
                distinct_home_teams.append(match.HomeTeam.ShortName)

        # Create a selection screen for the user
        for index, distinct_team in enumerate(distinct_home_teams):
            print(index, distinct_team)
        print(len(distinct_home_teams), "All")
        home_result = int(input("Please select one of the previous Teams as HomeTeam: "))

        # Filter by Season selection
        if 0 <= season_result <= len(distinct_home_teams):
            if season_result != len(distinct_home_teams):
                matches = list(filter(lambda x: x.HomeTeam.ShortName == distinct_home_teams[home_result], matches))
        else:
            raise IndexError("Please select one of the previous Leagues.")

        # Filter by teams
        distinct_away_teams = []
        for match in matches:
            if match.AwayTeam and match.AwayTeam.ShortName not in distinct_away_teams:
                distinct_away_teams.append(match.AwayTeam.ShortName)

        # Create a selection screen for the user
        for index, distinct_team in enumerate(distinct_away_teams):
            print(index, distinct_team)
        print(len(distinct_away_teams), "All")
        away_result = int(input("Please select one of the previous Teams as AwayTeam: "))

        # Filter by Season selection
        if 0 <= season_result <= len(distinct_away_teams):
            if season_result != len(distinct_away_teams):
                matches = list(filter(lambda x: x.AwayTeam.ShortName == distinct_away_teams[away_result], matches))

        score_home = 0
        score_away = 0
        for match in matches:
            scores = match.Score.split("-")
            score_home += int(scores[0])
            score_away += int(scores[1])
        score_home = round(score_home / len(matches), 2)
        score_away = round(score_away / len(matches), 2)

        print(f"Average score of {distinct_home_teams[home_result]}-{distinct_away_teams[away_result]} = {score_home}-{score_away}")


if __name__ == '__main__':
    main()
