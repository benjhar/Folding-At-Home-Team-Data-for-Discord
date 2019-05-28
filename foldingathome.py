import requests

def teamstats(teamnum):
    r = requests.get("https://stats.foldingathome.org/api/team/" + str(teamnum))
    return r.json()

def donor_stats(teamnum, user):
    team = teamstats(teamnum)
    donors = team["donors"]
    donorstats = []
    found = False
    for donor in donors:
        if donor["name"] == user:
            donorstats.append(user)
            donorstats.append(donor["credit"])
            donorstats.append(donor["wus"])
            return donorstats
    if not found:
        raise "No user could be found with that name!"
        

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