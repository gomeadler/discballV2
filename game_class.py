from team_class import Team
from player_class import Player
from time import sleep
from typing import Union, List
from constants import COLOR_DICT, POINTS_FOR_WIN
from random import choices
from os import system


class Game:
    _id_counter = 0  # Static counter for unique IDs
    _all_instances = []  # Static list to keep track of all instances

    @staticmethod
    def choose_target(shooter: Player, eligible_players: List[Player]) -> Player:
        probabilities = []
        for rival in eligible_players:
            distance = shooter.calculate_distance_to(rival)
            rival_prob = 1
            if rival.has_disc:
                rival_prob *= 5
            if rival.column in [10, 11]:
                rival_prob *= 2
            try:
                probabilities.append(rival_prob / distance)
            except ZeroDivisionError:
                print(f"{shooter.format_name()} tried to shoot {rival.format_name()} "
                      f"but the distance calculated was {distance}")
                raise ZeroDivisionError
        return Game.choose_player_by_probabilities(eligible_players, probabilities)

    @staticmethod
    def choose_player_by_probabilities(options: list, probabilities: list) -> Player:
        try:
            result = choices(options, weights=probabilities)[0]
        except IndexError:
            print(f"options were {options}, probs were {probabilities}")
            raise IndexError
        return result

    def __init__(self, left_team: Team, right_team: Team, declare: dict):
        Game._id_counter += 1
        Game._all_instances.append(self)
        self._id = Game._id_counter

        self._left_team: Team = left_team
        self._right_team: Team = right_team
        self._right_score = 0
        self._left_score = 0
        self._set_counter = 0
        self._phase_counter = 0
        self._turn_counter = 0
        self._carrier_color = self.determine_carrier_color()
        self._carrier: Union[Player, None] = None
        self._running_team: Union[Team, None] = None
        self._shooting_team: Union[Team, None] = None

    @property
    def teams(self):
        return self._left_team, self._right_team

    @property
    def on_field_players(self):
        return self._left_team.line_up + self._right_team.line_up

    def determine_carrier_color(self):  # TODO: use enum
        colors = [self._left_team.color, self._right_team.color]
        if COLOR_DICT["blue"] not in colors:
            return COLOR_DICT["cyan"]
        elif COLOR_DICT["magenta"] not in colors:
            return COLOR_DICT["purple"]
        else:
            return COLOR_DICT["lime"]

    def declare_teams(self):
        print(f"{self._left_team.name} Vs {self._right_team.name}")

    def prepare_match(self):
        self._left_team.is_left(True)
        self._right_team.is_left(False)
        for team in self.teams:
            team.reset_all_positions()
            team.allow_substitution()
        self.declare_teams()

    def creating_competition(self):
        eligible_players = \
            [player for player in self.on_field_players if player.column not in [0, 21]]
        creating_attributes = [player.creating for player in eligible_players]
        self._carrier = Game.choose_player_by_probabilities(eligible_players, creating_attributes)
        self._carrier.create_disc()
        self.determine_running_and_shooting_team()

    def determine_running_and_shooting_team(self):
        if not self._carrier:
            print("tried to find the running team but there is no carrier")
            raise Exception()
        if self._carrier in self._left_team.roster:
            self._running_team = self._left_team
            self._shooting_team = self._right_team
        elif self._carrier in self._right_team.roster:
            self._running_team = self._right_team
            self._shooting_team = self._left_team
        else:
            print(f"the carrier - {self._carrier.format_name} is not in either team's roster")
            raise Exception()

    def wrap_with_placeholders(self, string1_to_wrap: str, string2_to_wrap: str):
        left_placeholder = ' ' * (len(self._left_team.name) // 2)
        right_placeholder = ' ' * (len(self._right_team.name) // 2)
        str_list = [left_placeholder, string1_to_wrap, left_placeholder,
                    " : ",
                    right_placeholder, string2_to_wrap, right_placeholder]
        return "".join(str_list)

    def declare_state(self):
        system("cls")

        print(self.wrap_with_placeholders(self._left_team.format_team_name(), self._right_team.format_team_name()))
        print(self.wrap_with_placeholders(str(self._left_score), str(self._right_score)))
        print(f"set : {self._set_counter}, phase: {self._phase_counter}, turn: {self._turn_counter}")

    def conclude_match(self):
        self._left_team.is_left(False)
        for team in self.teams:
            team.inhibit_substitution()
            team.reset_roster()
            for player in team.roster:
                player.get_off_field()

        print(f"{self._left_team.name if self._left_score == POINTS_FOR_WIN else self._right_team.name} "
              f"won! \n"
              f"the final score was {self._left_score} : {self._right_score}")

    def check_touchdown(self) -> bool:
        if self._carrier.column in [10, 11]:
            self._carrier.touchdown()
            if self._running_team is self._left_team:
                self._left_score += 1
            elif self._running_team is self._right_team:
                self._right_score += 1
            else:
                print(f"either team isn't the running team!")
                raise Exception()
            return True
        return False

    def turn(self) -> str:
        self._turn_counter = 0

        while True:
            # a loop that runs until a touchdown is scored, the carrier drops the disc or there were more than 10 turns
            self._set_counter += 1

            self.declare_state()

            for team in self.teams:
                team.advance_all()

            there_was_a_drop_at_some_point = False
            taker = None
            for player in self._shooting_team.line_up:
                there_was_a_drop = player.face_off(Game.choose_target(player, self._running_team.line_up))
                if there_was_a_drop:
                    there_was_a_drop_at_some_point = True
                    taker = player.format_name()

            if there_was_a_drop_at_some_point:
                self.declare_state()
                print(f"{taker} has manage to take {self._carrier.format_name()} down!")
                sleep(3)
                return "Drop"

            if self.check_touchdown():
                self.declare_state()
                print(f"{self._carrier.format_name()} scored a touchdown!")
                sleep(3)
                return "Touchdown"

            if self._turn_counter > 9:
                self.declare_state()
                print(f"Time! the disc is now free!")
                sleep(3)
                return "Time"

    def phase(self):
        self._phase_counter = 0
        while True:
            self._phase_counter += 1
            self.creating_competition()
            result = self.turn()
            if result == "Touchdown":
                break

    def set(self):
        self._set_counter += 1
        for team in self.teams:
            team.reset_all_positions()
            team.add_set_to_players_count()

        self.phase()

