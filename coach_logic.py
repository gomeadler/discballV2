from star_player_logic import validate_answer
from team_class import Team
from player_class import Player
from game_class import Game
from constants import Color, NUM_OF_PLAYERS_IN_LINE_UP, NUM_OF_PLAYERS_IN_TEAM


class ManagerGame(Game):
    def __init__(self, left_team: Team, right_team: Team):
        super().__init__(left_team, right_team)
        self.main_team = self.decide_main_team()

    def _prepare_match(self):
        self._left_team.is_left = True
        self._right_team.is_left = False
        self._set_counter = 0
        self.choose_line_up()
        for team in self.teams:
            team.reset_all_positions()
            team.inhibit_substitution()
        self._declare_teams()

    def decide_main_team(self):
        team_ids = [team.team_id for team in self.teams]
        chosen_team_id = validate_answer(f"choose team. use id's from the following list: {team_ids}", team_ids)
        for team in self.teams:
            if team.team_id == chosen_team_id:
                return team
        raise Exception()

    def choose_line_up(self):
        options = self.main_team.default_starting_roster_ids[:]
        new_roster_ids = []
        for player in self.main_team.roster:
            player.present_player_attributes()
        if not bool(validate_answer("would you like to change line up? \nif so, press 1, otherwise 0", [0, 1])):
            return

        for position in range(NUM_OF_PLAYERS_IN_LINE_UP):
            chosen_id = validate_answer(f"choose player for position {position}", options)
            options.remove(chosen_id)
            new_roster_ids.append(chosen_id)
        new_roster_ids.extend(options)
        self.main_team.update_default_roster_to_given_id_list(new_roster_ids)
        self.main_team.reset_roster()
        self.main_team.display_roster()

    def coach_substitution(self):
        if not self.main_team.can_substitute:
            return
        if bool(validate_answer("would you like to make a substitution? if so press 1, otherwise 0", [0, 1])):
            exit_options = [num for num in range(NUM_OF_PLAYERS_IN_LINE_UP)]
            enter_options = [num for num in range(NUM_OF_PLAYERS_IN_LINE_UP, NUM_OF_PLAYERS_IN_TEAM)]
            exiting_player = self.main_team.line_up[validate_answer(f"choose player to sub out", exit_options)]
            entering_player = self.main_team.roster[validate_answer(f"choose player to sub in", enter_options)]
            self.main_team.substitute(entering_player, exiting_player)
            print(f"{entering_player.format_name} came on for {exiting_player.format_name} at position "
                  f"{exiting_player.position}")
            self.main_team.inhibit_substitution()

    def set(self):
        self._set_counter += 1
        for team in self.teams:
            if team is self.main_team and team.can_substitute:
                self.coach_substitution()
            elif team.can_substitute:
                team.decide_substitution()

            team.reset_all_positions()
            team.add_set_to_players_count()

        self._phase()


for i in range(NUM_OF_PLAYERS_IN_TEAM*2):
    Player()

team1 = Team("A", Color.RED, list(range(NUM_OF_PLAYERS_IN_TEAM)))
team2 = Team("B", Color.BLUE, list(range(NUM_OF_PLAYERS_IN_TEAM, NUM_OF_PLAYERS_IN_TEAM * 2)))
game1 = ManagerGame(team1, team2)
game2 = Game(team1, team2)
game1.simulate()
