import random

from constants import Color, NUM_OF_PLAYERS_IN_LINE_UP, NUM_OF_PLAYERS_IN_TEAM, paint
from player_class import Player
from typing import List

# TODO: shooting order


class Team:
    _id_counter = 0  # Static counter for unique IDs
    _all_instances = []  # Static list to keep track of all instances

    def __init__(self, name: str, color: Color, list_of_player_indexes: list):

        self._team_id = Team._id_counter
        Team._id_counter += 1
        Team._all_instances.append(self)

        self._name: str = name
        self._color: Color = color
        self._roster: List[Player] = [Player.get_all_instances()[i] for i in list_of_player_indexes]
        self._default_starting_roster_ids = list_of_player_indexes
        self._is_left = False
        self._can_substitute = False

    @classmethod
    def get_all_instances(cls):
        """Class method to retrieve all instances."""
        return cls._all_instances

    # Property for team_id
    @property
    def team_id(self):
        return self._team_id

    # Property for name
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    # Property for color
    @property
    def color(self) -> Color:
        return self._color

    @color.setter
    def color(self, new_color: Color):
        if not isinstance(new_color, Color):
            print(f"{new_color} is not a Color")
            raise Exception()
        self._color = new_color

    # Property for roster
    @property
    def roster(self):
        return self._roster

    @property
    def default_starting_roster_ids(self):
        return self._default_starting_roster_ids

    # Property for is_left
    @property
    def is_left(self):
        return self._is_left

    # Property for can_substitute
    @property
    def can_substitute(self):
        return self._can_substitute

    @property
    def line_up(self):
        return self._roster[:NUM_OF_PLAYERS_IN_LINE_UP]

    @is_left.setter
    def is_left(self, value: bool):
        self._is_left = bool(value)

    def reset_roster(self):
        self._roster = [Player.get_all_instances()[i] for i in self._default_starting_roster_ids]

    def decide_substitution(self):
        exiting_player = self.line_up[random.randint(0, NUM_OF_PLAYERS_IN_LINE_UP - 1)]
        entering_player = self._roster[random.randint(NUM_OF_PLAYERS_IN_LINE_UP, NUM_OF_PLAYERS_IN_TEAM - 1)]
        self.substitute(exiting_player, entering_player)
        print(f"{entering_player.format_name} came on for {exiting_player.format_name} at position "
              f"{exiting_player.position}")
        self.inhibit_substitution()

    def substitute(self, player1: Player, player2: Player):
        if not(player1 in self._roster and player2 in self._roster):
            print(f"one of {player1.format_name} and {player2.format_name} doesn't play for this team")
            raise

        first_index = self._roster.index(player1)
        second_index = self._roster.index(player2)
        temp_lst = []
        for i in range(NUM_OF_PLAYERS_IN_TEAM):
            if i == first_index:
                temp_lst.append(player2)
            elif i == second_index:
                temp_lst.append(player1)
            else:
                temp_lst.append(self._roster[i])
        self._roster = temp_lst

    def substitute_default_ids(self, id1: int, id2: int):
        if not (id1 in self._roster and id2 in self._roster):
            print(f"one of {id1} and {id2} doesn't play for this team")
            raise
        temp_lst = []
        for i in range(NUM_OF_PLAYERS_IN_TEAM):
            if i == id1:
                temp_lst.append(id2)
            elif i == id2:
                temp_lst.append(id1)
            else:
                temp_lst.append(self._default_starting_roster_ids[i])
        self._default_starting_roster_ids = temp_lst

    def update_default_roster_to_current(self):
        self._default_starting_roster_ids = [self._roster[i].get_id() for i in range(NUM_OF_PLAYERS_IN_TEAM)]

    def update_default_roster_to_given_id_list(self, id_list: List[int]):
        for player_id in id_list:
            if player_id not in self.default_starting_roster_ids:
                raise Exception()
        self._default_starting_roster_ids = id_list

    def inhibit_substitution(self):
        self._can_substitute = False

    def allow_substitution(self):
        self._can_substitute = True

    def format_team_name(self):
        return paint(self._name, self.color)

    def display_roster(self):
        print(self.format_team_name())
        for player in self._roster:
            print(player.format_name)

    def reset_all_positions(self):
        for i, player in enumerate(self._roster):
            if i < NUM_OF_PLAYERS_IN_LINE_UP:
                player.position = i
                player.reset_position(self._is_left)
            else:
                player.get_off_field()

    def add_set_to_players_count(self):
        for player in self.line_up:
            player.increment_stat_by("sets_played", 1)

    def get_positions(self):
        positions = []
        for player in self.line_up:
            positions.append(tuple([player.row, player.column]))
            if player.column not in range(22):
                raise ValueError(f"{player.format_name} is in an invalid position. "
                                 f"row: {player.row}, col: {player.column}")
        return positions

    def get_columns(self):
        columns = []
        for player in self.line_up:
            columns.append(player.column)
            if player.column not in range(22):
                raise ValueError(f"{player.format_name} is in an invalid position. "
                                 f"row: {player.row}, col: {player.column}")
        return columns

    def advance_all(self):
        for player in self.line_up:
            player.advance(self._is_left)

    def trade_in_player(self, arriving_player: Player):
        self._default_starting_roster_ids.append(arriving_player.get_id)
        self._roster.append(arriving_player)

    def trade_out_player(self, departing_player_id: int):
        self._default_starting_roster_ids.remove(departing_player_id)
        for player in self._roster:
            if player.get_id == departing_player_id:
                self._roster.remove(player)
                break

    def finish_match(self):
        self._is_left = False
        self._can_substitute = False
        for player in self._roster:
            player.get_off_field()
