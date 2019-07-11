import requests


def total_teams():
    r = requests.get(f'https://stats.foldingathome.org/api/team/0')
    team = r.json()
    return team["total_teams"]


class Team:
    def __init__(self, team=0):
        r = requests.get(f'https://stats.foldingathome.org/api/team/{team}')
        self.team = r.json()
        self.donors = r.json()["donors"]

    def highest_scorer(self):
        donors = self.donors
        users_and_scores = {}
        scores = []
        wus = []
        for donor in donors:
            users_and_scores[donor["name"]] = donor["credit"]
            scores.append(donor["credit"])
        credit = max(scores)
        wus = donors[scores.index(credit)]["wus"]
        rank = donors[scores.index(credit)]["rank"]
        team = donors[scores.index(credit)]["team"]
        id = donors[scores.index(credit)]["id"]
        name = donors[scores.index(credit)]["name"]

        return {
            "wus": wus,
            "name": name,
            "rank": rank,
            "credit": credit,
            "team": team,
            "id": id
        }

    def most_wus(self):
        donors = self.donors
        users_and_scores = {}
        wus = []
        for donor in donors:
            users_and_scores[donor["name"]] = donor["wus"]
            wus.append(donor["wus"])
        work_units = max(wus)

        credit = donors[wus.index(work_units)]["credit"]
        rank = donors[wus.index(work_units)]["rank"]
        team = donors[wus.index(work_units)]["team"]
        id = donors[wus.index(work_units)]["id"]
        name = donors[wus.index(work_units)]["name"]

        return {
            "wus": work_units,
            "name": name,
            "rank": rank,
            "credit": credit,
            "team": team,
            "id": id
        }

    def score(self):
        return self.team["credit"]

    def work_units(self):
        return self.team["wus"]

    def total_donors(self):
        return len(self.team["donors"])

    def rank(self):
        return self.team["rank"]

    def logo(self):
        return self.team["logo"]

    def stats(self):
        return self.team


class Donor:
    def __init__(self, donorname, team=0):
        r = requests.get(f'https://stats.foldingathome.org/api/team/{team}')
        self.team = r.json()

        donors = self.team["donors"]
        found = False
        for donor in donors:
            if donor["name"] == str(donorname):
                self.donor = donor
                found = True
        if not found and team == 0:
            raise Exception(
                f"\n\nNo user could be fou  nd with that name: {donorname}.\n This could be due to the user not being on the leaderboard for the default team, as the api only displays the top 1000 members of a team."
            )
        elif not found:
            raise Exception(
                f"\n\nNo user could be found with that name: {donorname}")

    def name(self):
        return self.donor["name"]

    def id(self):
        return self.donor["id"]

    def score(self):
        return self.donor["credit"]

    def work_units(self):
        return self.donor["wus"]

    def team_id(self):
        team = self.team
        return team["team"]

    def rank(self):
        donors = self.team["donors"]
        scores = []
        order = []
        for donor in donors:
            scores.append(donor["credit"])
        for i in scores:
            order.append(max(scores))
            scores.pop(scores.index(max(scores)))

        return order.index(self.donor["credit"]) + 1


class Monthly:
    def __init__(self):
        target = "https://stats.foldingathome.org/api"
        r = requests.get(f"{target}/teams-monthly")
        self.teams = r.json()
        self.Teams = self.Teams(self.teams)

    class Teams:
        def __init__(self, input):
            self.teams = input

        def highest_scorer(self):
            teams = self.teams["results"]
            teams_and_scores = {}
            scores = []
            for team in teams:
                teams_and_scores[team["name"]] = team["credit"]
                scores.append(team["credit"])

            credit = max(scores)
            wus = teams[scores.index(credit)]["wus"]
            rank = teams[scores.index(credit)]["rank"]
            team = teams[scores.index(credit)]["team"]
            name = teams[scores.index(credit)]["name"]

            return {
                "wus": wus,
                "name": name,
                "rank": rank,
                "credit": credit,
                "team": team
            }

        def most_wus(self):
            teams = self.teams["results"]
            teams_and_scores = {}
            wus = []
            for team in teams:
                teams_and_scores[team["name"]] = team["wus"]
                wus.append(team["wus"])
            work_units = max(wus)

            credit = teams[wus.index(work_units)]["credit"]
            rank = teams[wus.index(work_units)]["rank"]
            team = teams[wus.index(work_units)]["team"]
            name = teams[wus.index(work_units)]["name"]

            return {
                "wus": work_units,
                "name": name,
                "rank": rank,
                "credit": credit,
                "team": team
            }

        def team_list(self):
            return self.teams["results"]
