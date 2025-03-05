from team_class import Team
from player_class import Player
from time import sleep
from typing import Union, List
from constants import COLOR_DICT, POINTS_FOR_WIN, Color, NUM_OF_PLAYERS_IN_LINE_UP
from random import choices
from os import system
from field_class import Field


class Game:
    _id_counter = 0  # Static counter for unique IDs
    _all_instances = []  # Static list to keep track of all instances

    @staticmethod
    def _choose_target(shooter: Player, eligible_players: List[Player]) -> Player:
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
                print(f"{shooter.format_name} tried to shoot {rival.format_name} "
                      f"but the distance calculated was {distance}")
                raise ZeroDivisionError
        return Game._choose_player_by_probabilities(eligible_players, probabilities)

    @staticmethod
    def _choose_player_by_probabilities(options: list, probabilities: list) -> Player:
        try:
            result = choices(options, weights=probabilities)[0]
        except IndexError:
            print(f"options were {options}, probs were {probabilities}")
            raise IndexError
        return result

    def __init__(self, left_team: Team, right_team: Team):
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
        self._carrier_color: Color = self._determine_carrier_color()
        self.field = Field(left_team.color, right_team.color, self._carrier_color)
        self._carrier: Union[Player, None] = None
        self._running_team: Union[Team, None] = None
        self._shooting_team: Union[Team, None] = None

    @property
    def get_id(self):
        return self._id

    # Properties for scores
    @property
    def right_score(self):
        return self._right_score

    def increase_right_score(self):
        self._right_score += 1

    @property
    def left_score(self):
        return self._left_score

    def increase_left_score(self):
        self._left_score += 1

    # Property for carrier color (read-only, based on determine_carrier_color)
    @property
    def carrier_color(self):
        return self._carrier_color

    # Properties for carrier
    @property
    def carrier(self):
        return self._carrier

    def _set_carrier(self, player: Player):
        if not isinstance(player, Player):
            print(f"tried to change carrier but {player} is not a Player")
            raise Exception()
        self._carrier = player

    # Properties for teams
    @property
    def left_team(self):
        return self._left_team

    @property
    def right_team(self):
        return self._right_team

    @property
    def teams(self):
        return self._left_team, self._right_team

    @property
    def scores(self):
        return self._left_score, self._right_score

    @property
    def on_field_players(self):
        return self._left_team.line_up + self._right_team.line_up

    def _determine_carrier_color(self) -> Color:
        colors = [self._left_team.color, self._right_team.color]
        if Color.BLUE not in colors:
            return Color.CYAN
        elif Color.MAGENTA not in colors:
            return Color.PURPLE
        else:
            return Color.LIME

    def _get_columns(self):
        raw_column_lst = []
        final_column_lst = []
        for team in self.teams:
            raw_column_lst.extend(team.get_columns())
        for i in range(NUM_OF_PLAYERS_IN_LINE_UP):
            final_column_lst.append(raw_column_lst[i])
            final_column_lst.append(raw_column_lst[i + NUM_OF_PLAYERS_IN_LINE_UP])
        return final_column_lst

    def _declare_teams(self):
        print(f"{self._left_team.format_team_name()} Vs {self._right_team.format_team_name()}")

    def _prepare_match(self):
        self._left_team.is_left = True
        self._right_team.is_left = False
        self._set_counter = 0
        for team in self.teams:
            team.reset_all_positions()
            team.inhibit_substitution()
        self._declare_teams()

    def _creating_competition(self):
        eligible_players = \
            [player for player in self.on_field_players if player.column not in [0, 21]]
        creating_attributes = [player.creating for player in eligible_players]
        self._set_carrier(Game._choose_player_by_probabilities(eligible_players, creating_attributes))
        self._carrier.create_disc()
        self._determine_running_and_shooting_team()

    def _determine_running_and_shooting_team(self):
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

    def _wrap_with_placeholders(self, string1_to_wrap: str, string2_to_wrap: str):
        left_placeholder = ' ' * (len(self._left_team.name) // 2)
        right_placeholder = ' ' * (len(self._right_team.name) // 2)
        str_list = [left_placeholder, string1_to_wrap, left_placeholder,
                    " : ",
                    right_placeholder, string2_to_wrap, right_placeholder]
        return "".join(str_list)

    def _declare_state(self):
        system("cls")
        print("\n")
        self.field.print_field(self._get_columns(), self._carrier.row)

        print(self._wrap_with_placeholders(self._left_team.format_team_name(), self._right_team.format_team_name()))
        print(self._wrap_with_placeholders(str(self._left_score), str(self._right_score)))
        print(f"set : {self._set_counter}, phase: {self._phase_counter}, turn: {self._turn_counter}")
        if self._carrier is not None:
            print(f"{self._carrier.format_name} holds the disc at position {self._carrier.row, self._carrier.column}")

    def _conclude_match(self):
        print(f"{self._left_team.name if self._left_score == POINTS_FOR_WIN else self._right_team.name} "
              f"won! \n"
              f"the final score was {self._left_score} : {self._right_score}")
        for team in self.teams:
            team.finish_match()
            for player in team.roster:
                if player.game_table["sets_played"][0] > 0:
                    player.present_player(self.get_player_in_top_summary(player))

    def _check_touchdown(self) -> bool:
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

    def _turn(self) -> str:
        self._turn_counter = 0
        sleep_timer = 0

        while True:
            # a loop that runs until a touchdown is scored, the carrier drops the disc or there were more than 10 turns
            self._turn_counter += 1

            self._declare_state()

            for team in self.teams:
                team.advance_all()

            taker = None
            there_was_a_drop = False
            for player in self._shooting_team.line_up:
                target_player = Game._choose_target(player, self._running_team.line_up)
                there_was_a_fall = Player.face_off(player, target_player, self._running_team.is_left)
                if there_was_a_fall and target_player is self.carrier:
                    there_was_a_drop = True
                    taker = player.format_name

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
            if not self.dash_or_successful_pass():
                continue
            result = self._turn()
            if result == "Touchdown":
                break

    def set(self):
        self._set_counter += 1
        for team, score in zip(self.teams, self.scores):
            if score in [0, 3, 6, 9]:
                team.decide_substitution()
            else:
                team.allow_substitution()

            team.reset_all_positions()
            team.add_set_to_players_count()

        self._phase()

    def simulate(self):
        self._prepare_match()
        while self._left_score < POINTS_FOR_WIN and self._right_score < POINTS_FOR_WIN:
            self.set()
        self._conclude_match()

    def decide_pass_probabilities(self):
        running_is_left = self._running_team.is_left
        probabilities = []
        advantages = [self.carrier.compare_columns(player, running_is_left) for player in self._running_team.line_up]
        for player in self._running_team.line_up:
            if max(advantages) == 0:
                return [1 if player is self.carrier else 0 for player in self._running_team.line_up]

            elif player is self.carrier:
                distance_to_carrier = 0
                block_advantage = 1/max(advantages)

            else:
                distance_to_carrier = self.carrier.calculate_distance_to(player)
                block_advantage = self.carrier.compare_columns(player, running_is_left)/max(advantages)

            distance_to_end_zone = player.distance_to_end_zone(self._running_team.is_left)
            end_zone_weight = 1 if distance_to_end_zone == 0 else 1/distance_to_end_zone
            distance_weight = 1 if distance_to_carrier == 0 else 1/distance_to_carrier

            probabilities.append(block_advantage*end_zone_weight*distance_weight)
        return probabilities

    def dash_or_successful_pass(self):
        probabilities = self.decide_pass_probabilities()
        target = self._choose_player_by_probabilities(self._running_team.line_up, probabilities)
        if target is not self._carrier:
            return self.pass_try(target)
        else:
            self._carrier.dash()
            print(f"{self._carrier.format_name} decided to dash")
            return True

    def pass_try(self, target: Player):
        pass_result = Player.pass_play(self._carrier, target, self._running_team.is_left)
        if pass_result:
            print(
                f"{self._carrier.format_name} ({self._carrier.column}) passed it to {target.format_name} ({target.column})")
            self._carrier = target
        else:
            print(f"a failed pass by {self._carrier.format_name} to {target.format_name}")
        return pass_result

    def top_players(self, stat: str):
        threshold = 0
        top_list = []
        for player in self._left_team.roster + self._right_team.roster:
            temp = player.current_match_stat(stat)
            if temp > threshold:
                top_list = [player]
                threshold = temp
            elif temp == threshold and threshold != 0:
                top_list.append(player)
        return top_list

    def get_player_in_top_summary(self, player: Player):
        player_top_list = []
        keys = player.game_table.keys()
        for stat in keys:
            if stat == "sets_played":
                continue
            if player in self.top_players(stat):
                player_top_list.append(stat)
        return player_top_list


