import requests

def teamstats(teamnum):
    r = requests.get(f'https://stats.foldingathome.org/api/team/{teamnum}')
    return r.json()

def highest_scorer(team):
    donors = team["donors"]
    users_and_scores = {}
    scores = []
    for donor in donors:
        users_and_scores[donor["name"]] = donor["credit"]
        scores.append(donor["credit"])
    highestscore = max(scores)

    highestscorer = list(users_and_scores.keys())[list(users_and_scores.values()).index(highestscore)]

    return [highestscorer, highestscore]

def team_score(team):
    return team["credit"]

def team_work_units(team):
    return team["wus"]
