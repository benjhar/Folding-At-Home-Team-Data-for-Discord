import requests

class team:
    def __init__(self, team):
        r = requests.get(f'https://stats.foldingathome.org/api/team/{teamnum}')
        self.team = r.json()

    def highest_scorer(self.team):
        donors = self.team["donors"]
        users_and_scores = {}
        scores = []
        for donor in donors:
            users_and_scores[donor["name"]] = donor["credit"]
            scores.append(donor["credit"])
        highestscore = max(scores)

        highestscorer = list(users_and_scores.keys())[list(users_and_scores.values()).index(highestscore)]

        return [highestscorer, highestscore]

    def score(self.team):
        return self.team["credit"]

    def work_units(self.team):
        return self.team["wus"]

    def total_teams(self.team):
        return self.team["total_teams"]

    def total_donors(self.team):
        return len(self.team["donors"])

    def rank(self.team):
        return self.team["rank"]

    def logo(self.team):
        return self.team["logo"]

class donor:
    def __init__(self, donor, team=0):
        r = requests.get(f'https://stats.foldingathome.org/api/team/{teamnum}')
        self.team = r.json()

        donors = self.team["donors"]
        donorstats = []
        found = False
        for donor_ in donors:
            if donor_["name"] == donor:
                self.donor = donor_
                found = True
        if not found:
            raise "No user could be found with that name!"

    def name(self.donor):
        return self.donor["name"]

    def id(self.donor):
        return self.donor["id"]

    def score(self.donor):
        return self.donor["credit"]

    def work_units(self.donor):
        return self.donor["wus"]

    def rank(self.donor, self.team):
        donors = self.team["donors"]
        scores = []
        order = []
        for donor in donors:
            scores.append(donor["credit"])
        for i in scores:
            order.append(max(scores))
            scores.pop(scores.index(max(scores)))

        return scores.index(self.donor["credit"])+1
