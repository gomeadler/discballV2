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
    def _create_player_df():
        stats_dict = {
            "sets_played": [0],
            # offensive
            # points gain
            "touchdowns": [0],
            "assists": [0],

            # advancements
            "distance_carried": [0],
            "distance_passed": [0],
            "advancement_by_catch": [0],

            # creating
            "creations": [0],
            "end_zone_creation": [0],

            # holding
            "carrier_evasions": [0],
            "drop_avoidance": [0],

            # defensive
            "last_ditch_hits": [0],
            "last_ditch_takedowns": [0],
            "carrier_takedowns": [0],
            "carrier_hits": [0],

            # formation
            # positioning
            "distance_covered": [0],
            "turns_in_touchdown_strip": [0],
            "evasions": [0],
            "fall_avoidance": [0],

            # pressure
            "successful_shots": [0],
            "successful_takedowns": [0],

            # fails
            # offensive fail
            "drops_made": [0],
            "failed_passes": [0],
            "failed_catches": [0],

            # positioning fails
            "hits_taken": [0],
            "balance_losses": [0],

            # pass numbers
            "passes_made": [0],
            "catches_made": [0],
            "dashes": [0]
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
        self.game_table = Player._create_player_df()
        self.season_table = Player._create_player_df()
        self.all_time_stats = Player._create_player_df()

        self.is_star_player: bool = False

    # class methods
    @classmethod
    def get_all_instances(cls):
        """Class method to retrieve all instances."""
        return cls._all_instances

    @classmethod
    def delete_all_instances(cls):
        """Class method to retrieve all instances."""
        for item in cls._all_instances:
            del item
        cls._all_instances.clear()
        cls._id_counter = 0

    @classmethod
    def face_off(cls, shooting_player, target_player, target_is_left: bool):
        shot_quality = randint(1, shooting_player.shooting) // shooting_player.calculate_distance_to(target_player)
        evasion_attempt = randint(1, target_player.agility)
        if shot_quality <= evasion_attempt:
            target_player.evade()
            if shooting_player.is_star_player:
                print(f"{shooting_player.format_name} has missed!")
            return False
        else:
            target_is_carrier = target_player.has_disc
            target_initial_column = target_player.column
            shooting_player.hit_target(target_is_carrier, target_initial_column)
            there_was_a_fall = target_player.retreat(shot_quality, target_is_left)
            if there_was_a_fall:
                shooting_player.takedown(target_is_carrier, target_initial_column)
            return there_was_a_fall

    @classmethod
    def pass_play(cls, passer, catcher, is_left):
        pass_attempt = randint(1, passer.distribution)
        catch_attempt = randint(1, catcher.control)
        distance = passer.calculate_distance_to(catcher)
        threshold = randint(1, 20) * distance
        blocks_difference = passer.compare_columns(catcher, is_left)
        if pass_attempt > 0.75 * threshold:
            catch_attempt *= 1.5
        if pass_attempt + catch_attempt >= threshold:

            passer.pass_disc(blocks_difference)
            catcher.catch_disc(blocks_difference)
            return True
        else:
            passer.pass_fail()
            passer.give_disc_away()
            catcher.catch_fail()
            return False

    # Properties
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
    def color(self) -> str:
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

    @property
    def attribute_names(self):
        return "speed, agility, creating, shooting, stability, distribution, control".split(", ")

    # Property for has_disc
    @property
    def has_disc(self):
        return self._has_disc

    @property
    def on_field(self):
        return self._on_field

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: int):
        self._position = value

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def delay(self):
        return self._delay

    @property
    def fatigue(self):  # TODO: fatigue logic
        return self._fatigue

    @fatigue.setter
    def fatigue(self, value):
        self._fatigue = value

    # disc related methods
    def create_disc(self):
        self.gain_disc()
        self.increment_stat_by("creations", 1)
        if self.column in [10, 11]:
            self.increment_stat_by("end_zone_creation", 1)

    def gain_disc(self):
        self._has_disc = True

    def give_disc_away(self):
        self._has_disc = False

    # field related methods
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

    # row related methods
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

    def reset_position(self, is_left: bool):
        self.get_on_field()
        self.give_disc_away()
        self.set_row(is_left)
        self._delay_switch_off()
        if is_left:
            self._column = 1
        else:
            self._column = 20

    def _determine_blocks(self) -> int:
        """randomizes the number of blocks a certain player would advance.
        """
        # TODO: special qualities such as sprinter and slow starter

        if self.delay:
            self._delay_switch_off()
            return 0
        run_attempt = randint(1, self.speed)
        if run_attempt > 66:
            advance_blocks = 3
        elif run_attempt > 33:
            advance_blocks = 2
        else:
            advance_blocks = 1
        return advance_blocks

    def advance(self, is_left: bool):
        original_column = self.column  # TODO: remove later
        threshold = 10 if is_left else 11
        direction = 1 if is_left else -1

        if self.column == threshold:
            self.increment_stat_by("turns_in_touchdown_strip", 1)
        elif self._delay:
            self._delay_switch_off()
        else:
            self.increase_fatigue()
            distance = abs(self.column - threshold)
            blocks = self._determine_blocks()
            if distance < blocks:
                blocks = distance
            self.increment_stat_by("distance_covered", blocks)
            self._column += blocks * direction
            if self.is_star_player:
                print(f"{self.format_name} used to be at {original_column}, and advanced to {self.column}")
            if self.has_disc:
                self.increment_stat_by("distance_carried", blocks)

    def touchdown(self):
        self.increment_stat_by("touchdowns", 1)

    def _determine_retreat(self, shot_quality: int) -> int:
        balance_attempt = randint(1, self.stability) // 3
        if balance_attempt > shot_quality:
            blocks = 2
        elif balance_attempt == shot_quality:
            blocks = 5
        else:
            blocks = 10
        return blocks

    def retreat(self, shot_quality: int, is_left: bool) -> bool:
        original_column = self.column  # TODO: remove later
        blocks = self._determine_retreat(shot_quality)
        there_is_a_takedown = self._check_fall(blocks, is_left)
        if there_is_a_takedown:
            self.fall_down(is_left)
        else:
            self.absorb(blocks, is_left)
            if self.is_star_player:
                print(f"{self.format_name} used to be at {original_column}, and retreated to {self.column}")
        return there_is_a_takedown

    # face_off related methods
    def evade(self):
        self.increment_stat_by("evasions", 1)
        if self.has_disc:
            self.increment_stat_by("carrier_evasions", 1)
        if self.is_star_player:
            print(f"{self.format_name} has managed to evade a shot!")

    def hit_target(self, target_has_disc: bool, target_column: int):
        self.increment_stat_by("successful_shots", 1)
        if target_has_disc:
            self.increment_stat_by("carrier_hits", 1)
            if target_column in [10, 11]:
                self.increment_stat_by("last_ditch_hits", 1)
        if self.is_star_player:
            print(f"{self.format_name} has made a successful shot!")

    def takedown(self, target_has_disc: bool, target_column: int):
        self.increment_stat_by("successful_takedowns", 1)
        if target_has_disc:
            self.increment_stat_by("carrier_takedowns", 1)
            if target_column in [10, 11]:
                self.increment_stat_by("last_ditch_takedowns", 1)
        pass

    def _check_fall(self, blocks: int, is_left: bool) -> bool:
        if is_left and self.column <= blocks:
            return True
        elif not is_left and (21 - self.column) <= blocks:
            return True
        return False

    def fall_down(self, is_left: bool):
        original_column = self.column
        direction = 1 if is_left else -1
        self.increment_stat_by("hits_taken", 1)
        self.increment_stat_by("balance_losses", 1)
        if self.has_disc:
            self.increment_stat_by("drops_made", 1)
        self._delay_switch_on()
        self.reset_position(is_left)
        self._column -= direction
        if self.is_star_player:
            print(f"{self.format_name} used to be at {original_column}, and fell to {self.column}")

    def absorb(self, blocks: int, is_left: bool):
        self.increment_stat_by("hits_taken", 1)
        fall_avoidance = 10 - self.distance_to_end_zone(is_left) - blocks
        self.increment_stat_by("fall_avoidance", fall_avoidance)
        if self.has_disc:
            self.increment_stat_by("drop_avoidance", fall_avoidance)
        if self.has_disc and self.column in [10, 11]:
            self.increment_stat_by("last_ditch_hits", 1)
        if not is_left:
            blocks *= -1
        self._column -= blocks

    # fatigue related methods
    def increase_fatigue(self):
        self._fatigue += 1

    # delay related methods
    def _delay_switch_on(self):
        self._delay = True

    def _delay_switch_off(self):
        self._delay = False

    # data manipulation
    def increment_stat_by(self, stat, amount):
        self.game_table[stat] += amount

    # TODO: transfer data from game table to other tables

    # passing related methods
    def pass_disc(self, blocks_difference: int):
        self.increment_stat_by("passes_made", 1)
        self.increment_stat_by("distance_passed", blocks_difference)
        self.give_disc_away()

    def catch_disc(self, blocks_difference: int):
        self.increment_stat_by("catches_made", 1)
        self.increment_stat_by("advancement_by_catch", blocks_difference)
        self.gain_disc()

    def pass_fail(self):
        self.increment_stat_by("failed_passes", 1)

    def catch_fail(self):
        self.increment_stat_by("failed_catches", 1)

    def dash(self):
        self.increment_stat_by("dashes", 1)

    # other
    def calculate_distance_to(self, player2) -> float:
        result = dist((self.row, self.column), (player2.row, player2.column))
        if result == 0:
            print(f"tried to calculate the distance between {self.format_name} and {player2.format_name}. "
                  f"rows were {self.row, player2.row}, columns were {self.column, player2.column}")
            raise ZeroDivisionError
        else:
            return result

    def compare_columns(self, player2, is_left: bool) -> int:
        direction = 1 if is_left else -1
        difference = (player2.column - self.column) * direction
        if difference > 0:
            return difference
        return 0

    def distance_to_end_zone(self, is_left: bool):
        threshold = 10 if is_left else 11
        return abs(self.column - threshold)

    @property
    def format_name(self) -> str:  # TODO: use enum
        """
        formats a player's name to match its Team's color.

        :return: string of ANSI escape code (of the Team's color), player's name and ANSI escape code (of a color reset)
        """
        return "".join([self.color, self.name, COLOR_RESET])

    def current_match_stat(self, stat: str):
        return self.game_table[stat][0]

    def present_player_game_stats(self, top_stat_list: list):
        keys_list = list(self.game_table.keys())
        print(self.format_name)
        for player_stat in keys_list:
            print(player_stat, end="- ")
            if player_stat in top_stat_list:
                print(COLOR_DICT["purple"], end="")
            print(self.current_match_stat(player_stat))
            print(COLOR_RESET, end="")
        self.assess_performance()

    def present_player_attributes(self):
        print(self.format_name, self.get_id)
        for name, value in zip(self.attribute_names, self.attributes):
            print(f"{name}: {value}")

    def get_score_from_categories(self, categories, weights):
        return sum([self.current_match_stat(categories[i]) * weights[i] for i in range(len(categories))])

    def get_offence_score(self):
        points_categories = ["touchdowns", "assists"]
        touchdowns_score = self.get_score_from_categories(points_categories, [1, 0.8])
        advancement_stats = ["distance_carried", "distance_passed", "advancement_by_catch"]
        advancement_score = self.get_score_from_categories(advancement_stats, [1, 1, 1])
        creation_stats = ["creations", "end_zone_creation"]
        creation_score = self.get_score_from_categories(creation_stats, [1, 2])
        holding_stats = ["carrier_evasions", "drop_avoidance"]
        holding_score = self.get_score_from_categories(holding_stats, [10, 1])
        offence_scores_list = [touchdowns_score, advancement_score, creation_score, holding_score]

        offence_weights = [1, 0.05, 0.2, 0.005]
        return round(sum([offence_scores_list[i] * offence_weights[i] for i in range(len(offence_scores_list))]), 2)

    def get_defence_score(self):
        defence_categories = ["last_ditch_hits", "last_ditch_takedowns", "carrier_takedowns", "carrier_hits"]
        defence_weights = [0.5, 1, 0.5, 0.2]
        return round(self.get_score_from_categories(defence_categories, defence_weights), 2)

    def get_fail_score(self):
        off_fail_categories = ["drops_made", "failed_passes", "failed_catches"]
        off_fail_weights = [1, 0.4, 0.2]
        off_fail_score = self.get_score_from_categories(off_fail_categories, off_fail_weights)

        pos_fail_categories = ["hits_taken", "balance_losses"]
        pos_fail_weights = [0.2, 1]
        pos_fail_score = self.get_score_from_categories(pos_fail_categories, pos_fail_weights)

        fail_scores_list = [off_fail_score, pos_fail_score]
        fail_weights = [1, 0.2]
        return round(sum([fail_scores_list[i] * fail_weights[i] for i in range(len(fail_scores_list))]), 2)

    def get_formation_score(self):
        positioning_categories = ["distance_covered", "turns_in_touchdown_strip", "evasions", "fall_avoidance"]
        positioning_weights = [0.25, 1, 0.25, 0.05]
        positioning_score = self.get_score_from_categories(positioning_categories, positioning_weights)

        pressure_categories = ["successful_shots", "successful_takedowns"]
        pressure_weights = [0.2, 1]
        pressure_score = self.get_score_from_categories(pressure_categories, pressure_weights)

        formation_scores_list = [positioning_score, pressure_score]
        formation_weights = [0.1, 0.2]
        return round(sum([formation_scores_list[i] * formation_weights[i] for i in range(len(formation_scores_list))]), 2)

    def assess_performance(self):
        def standardize_score(raw: float, mean: float, std: float):
            z_score = (raw - mean) / std
            standardized = round(5.5 + z_score * 1.5, 1)
            if standardized > 10:
                standardized = 10.0
            elif standardized < 1:
                standardized = 1.0
            return standardized

        if self.current_match_stat("sets_played"):
            offence_score = standardize_score(self.get_offence_score(), 4.88, 3.46)
            defence_score = standardize_score(self.get_defence_score(), 2.59, 2.38)
            formation_score = standardize_score(self.get_formation_score(), 8, 1.896)
            fail_score = standardize_score(self.get_fail_score(), 2.2, 1.53)
            print("off", offence_score, "def", defence_score, "form", formation_score, "fail", fail_score)
