from game_objects.GameObjects import GameActor


class TeamManager:
    def __init__(self, teams = None):

        # doing it this way because of https://www.pullrequest.com/blog/python-pitfalls-the-perils-of-using-lists-and-dicts-as-default-arguments/
        if teams != None:
            self.teams = teams #type: list[Team]
        else:
            self.teams = []

    def get_all_enemies(self, team):
        teams_to_check = [team_to_check for team_to_check in self.teams if team_to_check != team]
        opps = []
        for team in teams_to_check:
            opps.extend(team.members)
        return opps

    def get_first_enemy(self, team):
        opps = self.get_all_enemies(team)
        try:
            return opps[0]
        except ValueError:
            return None
        
    def get_next_enemy(self, team, enemy):
        opps = self.get_all_enemies(team)
        try:
            enemy_index = opps.index(enemy)
            enemy_index = (enemy_index + 1) % len(opps)
            return opps[enemy_index]
        except ValueError:
            # searching for a member that isn't in the list, so just return the first one
            if len(opps) == 0:
                return None
            return opps[0]

class Team:

    def __init__(self, name):
        # not a constructor parameter because https://www.pullrequest.com/blog/python-pitfalls-the-perils-of-using-lists-and-dicts-as-default-arguments/
        self.members = list()
        self.name = name

    def add_member(self, member: "GameActor"):
        self.members.append(member)

    def remove_member(self, member: "GameActor"):
        self.members.remove(member)

    def is_member(self, member: "GameActor"):
        try:
            self.members.index(member)
            return True
        except ValueError:
            return False

    def get_first_member(self):
        try:
            return self.members[0]
        except ValueError:
            return None
    
    def get_next_member(self, member: "GameActor"):
        try:
            member_index = self.members.index(member)
            member_index = (member_index + 1) % len(self.members)
            return self.members[member_index]
        except ValueError:
            # searching for a member that isn't in the list, so just return the first one
            if len(self.members) == 0:
                return None
            return self.members[0]