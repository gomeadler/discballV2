from constants import COLOR_RESET, COLOR_DICT
from data import import_players
from pandas import DataFrame
from random import randint
from math import dist


class Player:
    """A class representing a player during a game."""
    _id_counter = 0  # Static counter for unique IDs
    _all_instances = []  # Static list to keep track of all instances

    @staticmethod
    def create_player_df():
        stats_dict = {
            "sets_played": [0],
            "distance_covered": [0],
            "distance_carried": [0],
            "distance_passes": [0],
            "touchdowns": [0],
            "turns_in_touchdown_strip": [0],
            "creations": [0],
            "end_zone_creation": [0],
            "evasions": [0],
            "carrier_evasions": [0],
            "successful_shots": [0],
            "successful_takedowns": [0],
            "last_ditch_hits": [0],
            "last_ditch_takedowns": [0],
            "carrier_takedowns": [0],
            "hits_taken": [0],
            "balance_losses": [0],
            "drops_made": [0],
            "passes_made": [0],
            "catches_made": [0],
            "assists": [0],
            "control_losses": [0],
        }
        return DataFrame(stats_dict)

    def __init__(self):
        data = import_players().loc[Player._id_counter]
        # personal
        self._id = Player._id_counter
        Player._id_counter += 1
        Player._all_instances.append(self)
        self._name = data["Name"]

        # team related
        self._team = data["Team"]
        self._color = COLOR_DICT[data["Color"]]

        # attributes
        self._speed = data["speed"]
        self._agility = data["agility"]
        self._creating = data["creating"]
        self._shooting = data["shooting"]
        self._stability = data["stability"]
        self._stamina = data["stamina"]
        self._distribution = data["distribution"]
        self._control = data["control"]
        self.value = 0  # TODO: value logic

        # gameplay related
        self._has_disc = False
        self._on_field = False
        self._position = None
        self._has_disc = False
        self._row = None
        self._column = None
        self._delay = False
        self._fatigue = 0

        #  stat related
        # TODO: think if this requires properties
        self.game_table = Player.create_player_df()
        self.season_table = Player.create_player_df()
        self.all_time_stats = Player.create_player_df()

    @classmethod
    def get_all_instances(cls):
        """Class method to retrieve all instances."""
        return cls._all_instances

    # Property getters
    @property
    def get_id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def team(self):
        return self._team

    @property
    def color(self):
        return self._color

    @property
    def speed(self):
        return self._speed

    @property
    def agility(self):
        return self._agility

    @property
    def creating(self):
        return self._creating

    @property
    def shooting(self):
        return self._shooting

    @property
    def stability(self):
        return self._stability

    @property
    def stamina(self):
        return self._stamina

    @property
    def distribution(self):
        return self._distribution

    @property
    def control(self):
        return self._control

    @property
    def attributes(self):
        return self._speed, self._agility, self._creating, self._shooting, self._stability, self._distribution, \
            self._control

    # Property for has_disc
    @property
    def has_disc(self):
        return self._has_disc

    def create_disc(self):
        self.gain_disc()
        self.increment_stat_by("creations", 1)
        if self.column in [10, 11]:
            self.increment_stat_by("end_zone_creation", 1)

    def gain_disc(self):
        self._has_disc = True

    def give_disc_away(self):
        self._has_disc = False

    # Property for on_field
    @property
    def on_field(self):
        return self._on_field

    def get_on_field(self):
        self._on_field = True

    def get_off_field(self):
        self._has_disc = False
        self._on_field = False
        self._position = None
        self._has_disc = False
        self._row = None
        self._column = None
        self._delay = False
        self._fatigue = 0  # TODO: think about the relevant logic

    # Property for position
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    # Property for row
    @property
    def row(self):
        return self._row

    def set_row(self, is_left: bool):
        if not self.on_field:
            self._row = None
            return
        try:
            self._row = self._position * 2
        except TypeError:
            print(f"invalid position for this player - {self.position}")
        if not is_left:
            self._row += 1

    # Property for column
    @property
    def column(self):
        return self._column

    def reset_position(self, is_left: bool):
        self.get_on_field()
        self.give_disc_away()
        self.set_row(is_left)
        self.delay_switch_off()
        if is_left:
            self._column = 1
        else:
            self._column = 20

    def fall_down(self, is_left):
        self.increment_stat_by("hits_taken", 1)
        self.increment_stat_by("balance_losses", 1)
        if self.has_disc:
            self.increment_stat_by("drops_made", 1)
        self.delay_switch_on()
        self.reset_position(is_left)
        if is_left:
            self._column -= 1
        else:
            self._column += 1

    def absorb(self, blocks: int, is_left: bool):
        self.increment_stat_by("hits_taken", 1)
        if self.has_disc and self.column in [10, 11]:
            self.increment_stat_by("last_ditch_hits", 1)
        if is_left:
            blocks *= -1
        self._column -= blocks

    def advance(self, is_left: bool):
        threshold = 10 if is_left else 11
        direction = 1 if is_left else -1

        if self.column == threshold:
            self.increment_stat_by("turns_in_touchdown_strip", 1)
        else:
            self.increase_fatigue()
            distance = abs(self.column - threshold)
            blocks = self.determine_blocks()
            if distance < blocks:
                blocks = distance
            self.increment_stat_by("distance_covered", blocks)
            self._column += blocks * direction
            if self.has_disc:
                self.increment_stat_by("distance_carried", blocks)

    def touchdown(self):
        self.increment_stat_by("touchdowns", 1)

    # Property for delay
    @property
    def delay(self):
        return self._delay

    def delay_switch_on(self):
        self._delay = True

    def delay_switch_off(self):
        self._delay = False

    # Property for fatigue
    @property
    def fatigue(self):  # TODO: fatigue logic
        return self._fatigue

    @fatigue.setter
    def fatigue(self, value):
        self._fatigue = value

    def increase_fatigue(self):
        self._fatigue += 1

    # data manipulation
    def increment_stat_by(self, stat, amount):
        self.game_table.loc[stat] += amount

    # TODO: transfer data from game table to other tables

    @classmethod
    def face_off(cls, shooting_player, target_player, target_is_left: bool):
        shot_quality = randint(1, shooting_player.shooting) // shooting_player.calculate_distance_to(target_player)
        evasion_attempt = randint(1, target_player.agility)
        if shot_quality <= evasion_attempt:
            target_player.evade()
            return False
        else:
            shooting_player.hit_target(target_player.has_disc, target_player.column)
            there_was_a_fall = target_player.retreat(shot_quality, target_is_left)
            if there_was_a_fall:
                shooting_player.takedown(target_player.has_disc, target_player.column)
        return True

    @classmethod
    def pass_play(cls, passer, catcher):
        pass_attempt = randint(1, passer.distribution)
        catch_attempt = randint(1, catcher.control)
        distance = passer.calculate_distance_to(catcher)
        threshold = randint(1, 20) * distance
        if pass_attempt > 0.75 * threshold:
            catch_attempt *= 1.5
        if pass_attempt + catch_attempt >= threshold:
            passer.pass_disc(distance)
            catcher.catch_disc()
            return True
        if pass_attempt < 0.5*threshold:
            passer.pass_fail()
        if catch_attempt < 0.5*threshold:
            catcher.pass_fail()
        return False

    def determine_blocks(self) -> int:
        """randomizes the number of blocks a certain player would advance.
        """
        # TODO: special qualities such as sprinter and slow starter

        if self.delay:
            self.delay_switch_off()
            return 0
        run_attempt = randint(1, self.speed)
        if run_attempt > 66:
            advance_blocks = 3
        elif run_attempt > 33:
            advance_blocks = 2
        else:
            advance_blocks = 1
        return advance_blocks

    def evade(self):
        self.increment_stat_by("evasions", 1)
        if self.has_disc:
            self.increment_stat_by("carrier_evasions", 1)

    def determine_retreat(self, shot_quality: int) -> int:
        balance_attempt = randint(1, self.stability) // 3
        if balance_attempt > shot_quality:
            blocks = 2
        elif balance_attempt == shot_quality:
            blocks = 5
        else:
            blocks = 10
        return blocks

    def retreat(self, shot_quality: int, is_left: bool) -> bool:
        """

        :param shot_quality:
        :param is_left:
        :return: True if player has fallen, False otherwise
        """
        blocks = self.determine_retreat(shot_quality)
        there_is_a_takedown = self.check_fall(blocks, is_left)
        if there_is_a_takedown:
            self.fall_down(is_left)
        else:
            self.absorb(blocks, is_left)
        return there_is_a_takedown

    def hit_target(self, target_has_disc: bool, target_column: int):
        self.increment_stat_by("successful_shots", 1)
        if target_has_disc:
            self.increment_stat_by("carrier_hits", 1)
            if target_column in [10, 11]:
                self.increment_stat_by("last_ditch_hits", 1)

    def takedown(self, target_has_disc: bool, target_column: int):
        self.increment_stat_by("successful_takedowns", 1)
        if target_has_disc:
            self.increment_stat_by("carrier_takedowns", 1)
            if target_column in [10, 11]:
                self.increment_stat_by("last_ditch_takedowns", 1)
        pass

    def check_fall(self, blocks: int, is_left: bool) -> bool:
        if is_left and self.column <= blocks:
            return True
        elif not is_left and (21 - self.column) <= blocks:
            return True
        return False

    def pass_disc(self, distance):
        self.increment_stat_by("passes_made", 1)
        self.increment_stat_by("distance_passed", distance)
        self.give_disc_away()

    def catch_disc(self):
        self.increment_stat_by("catches_made", 1)
        self.gain_disc()

    def pass_fail(self):
        self.increment_stat_by("control_losses", 1)

    def calculate_distance_to(self, player2) -> float:
        result = dist((self.row, self.column), (player2.row, player2.column))
        if result == 0:
            print(f"tried to calculate the distance between {self.format_name()} and {player2.format_name()}. "
                  f"rows were {self.row, player2.row}, columns were {self.column, player2.column}")
            raise ZeroDivisionError
        else:
            return result

    def format_name(self) -> str:
        """
        formats a player's name to match its Team's color.

        :return: string of ANSI escape code (of the Team's color), player's name and ANSI escape code (of a color reset)
        """
        return "".join([self.color, self.name, COLOR_RESET])

    def present_player(self, stats_table: DataFrame, top_stat_list: list):
        # TODO: fit to current system
        keys_list = list(stats_table.keys())
        first_index = keys_list.index("distance_covered")
        print(self.format_name())
        for player_stat in keys_list[first_index:]:
            if player_stat in top_stat_list:
                print(COLOR_DICT["purple"], end="")
            print("   ", player_stat, stats_table.loc[self._id, player_stat])
            print(COLOR_RESET, end="")

    def assess_performance(self, stats_table: DataFrame):
        # TODO: add passing
        player_stats = stats_table.loc[self._id]

        if player_stats["sets_played"]:
            # offence score
            offence_score = 0.0
            offence_score += 10 * player_stats["touchdowns"]
            offence_score += player_stats["creations"] - player_stats["touchdowns"] - player_stats["drops_made"]
            offence_score += player_stats["distance_carried"] / 4
            offence_score += player_stats["carrier_evasions"] / 2
            offence_score -= player_stats["drops_made"] / 2
            if offence_score < 0:  # has printing if someone wants to know
                #  print("under 0", offence_score)
                offence_score = 0.0
            offence_score /= player_stats["sets_played"]

            # defence score
            defence_score = 0.0
            defence_score += 10 * player_stats["last_ditch_takedowns"]
            defence_score += 7 * (player_stats["carrier_takedowns"] - player_stats["last_ditch_takedowns"])
            defence_score += 3 * (player_stats["successful_takedowns"] - player_stats["carrier_takedowns"])
            defence_score += player_stats["last_ditch_hits"] - player_stats["last_ditch_takedowns"]
            defence_score += (player_stats["successful_shots"]
                              - player_stats["successful_takedowns"]
                              - player_stats["last_ditch_hits"]) / 2
            defence_score /= player_stats["sets_played"]
            defence_score *= 1.5

            # total score
            total_score = (offence_score + defence_score + max(offence_score, defence_score))
            if total_score < 5:
                total_score = float(int(total_score))
            elif total_score <= 7.5:
                total_score = int(total_score * 2) / 2
            elif total_score <= 12:
                temp = int((total_score % 7.5) + 1) / 5
                total_score = 7.5 + temp
            else:
                temp = int((total_score % 12) + 1) / 10
                total_score = 8.5 + temp
                if total_score >= 10:
                    total_score = 10.0
            # print(offence_score, defence_score, total_score)

            return offence_score, defence_score, total_score