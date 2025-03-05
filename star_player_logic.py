from player_class import Player
from team_class import Team
from game_class import Game
from constants import Color, NUM_OF_PLAYERS_IN_TEAM
from time import sleep


def validate_answer(text: str, options: list):
    while True:
        your_input = None
        try:
            your_input = int(input(text))
        except ValueError:
            pass
        finally:
            if your_input in options:
                return your_input
            print(f"that not an option.\n"
                  f"the options are {options}. try again")


class MainPlayerGame(Game):
    def __init__(self, left_team: Team, right_team: Team):
        super().__init__(left_team, right_team)
        self.main_team = None
        self.main_player: Player = self.decide_player()

    def decide_player(self):
        team_ids = [team.team_id for team in self.teams]
        chosen_team_id = validate_answer(f"choose team. use id's from the following list: {team_ids}", team_ids)
        for team in self.teams:
            if team.team_id == chosen_team_id:
                self.main_team = team
                player_ids = [player.get_id for player in team.roster]
                chosen_player_id = validate_answer(f"choose player. "
                                                   f"use id's from the following list: {player_ids}", player_ids)
                for player in team.roster:
                    if player.get_id == chosen_player_id:
                        print(
                            f"you chose {player.format_name}. you will play for {self.main_team.format_team_name()}")
                        player.is_star_player = True
                        return player
        raise Exception()

    def _turn(self) -> str:
        self._turn_counter = 0
        sleep_timer = 3

        self._declare_state()

        while True:
            # a loop that runs until a touchdown is scored, the carrier drops the disc or there were more than 10 turns
            self._turn_counter += 1

            for team in self.teams:
                team.advance_all()

            self._declare_state()

            taker = None
            there_was_a_drop = False
            for player in self._shooting_team.line_up:
                if player is self.main_player:
                    target_num = validate_answer("choose which player to shoot", [position for position in range(5)])
                    target_player = self._running_team.line_up[target_num]
                else:
                    target_player = Game._choose_target(player, self._running_team.line_up)
                there_was_a_fall = Player.face_off(player, target_player, self._running_team.is_left)
                if there_was_a_fall and target_player is self.carrier:
                    there_was_a_drop = True
                    taker = player.format_name

            sleep(sleep_timer)

            if there_was_a_drop:
                self._declare_state()
                print(f"{taker} has manage to take {self._carrier.format_name} down!")
                sleep(sleep_timer)
                return "Drop"

            if self._check_touchdown():
                self._declare_state()
                print(f"{self._carrier.format_name} scored a touchdown!")
                sleep(sleep_timer)
                return "Touchdown"

            if self._turn_counter > 9:
                self._declare_state()
                print(f"Time! the disc is now free!")
                sleep(sleep_timer)
                return "Time"

    def _phase(self):
        self._phase_counter = 0
        while True:
            self._phase_counter += 1
            self._creating_competition()
            self._declare_state()
            if self.carrier is self.main_player:
                play_turn = self.choose_dash_or_pass()
            else:
                play_turn = self.dash_or_successful_pass()
            if not play_turn:
                continue

            result = self._turn()
            if result == "Touchdown":
                break

    def choose_dash_or_pass(self):
        print(f"you have created the disc! \n"
              f"would you rather dashing with it or passing it to another player?")
        if validate_answer("for dash, press 0. for pass, press 1", [0, 1]) == 0:
            self.main_player.dash()
            return True
        else:
            options = [player.position for player in self._running_team.line_up if player is not self.main_player]
            target_num = validate_answer("choose a player to pass to", options)
            return self.pass_try(self._running_team.line_up[target_num])


for i in range(NUM_OF_PLAYERS_IN_TEAM*2):
    Player()


team1 = Team("A", Color.RED, list(range(NUM_OF_PLAYERS_IN_TEAM)))
team2 = Team("B", Color.BLUE, list(range(NUM_OF_PLAYERS_IN_TEAM, NUM_OF_PLAYERS_IN_TEAM * 2)))
game1 = MainPlayerGame(team1, team2)
game2 = Game(team1, team2)
game2.simulate()
