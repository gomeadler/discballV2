import pandas
from pandas import DataFrame, read_excel, Series
from numpy import random, clip
from names import get_first_name
from constants import *


# TODO: maybe use matplotlib to show graphics of statistics?
def find_team_by_name(team_name: str) -> int:
    for index, team in enumerate(TEAMS):
        if team == team_name:
            return index

    raise ValueError("Team not found")


def get_color(team_name: str) -> str:
    color = COLOR_DICT["white"]
    for t in TEAMS:
        if t == team_name:
            color = t[1]
            return color
    if color == COLOR_DICT["white"]:
        raise ValueError("Team not found")


###
def random_gaussian_number(mean, std_dev, min_value, max_value) -> int:
    return int(clip(round(random.normal(mean, std_dev)), min_value, max_value))


def create_league(path) -> DataFrame:
    league = {
        "ID": [i for i in range(NUM_OF_TEAMS)],
        "Color": [i for i in COLORS],
        "Name": [i for i in TEAMS]
    }
    df = DataFrame(league)
    df.to_excel(path, index=False)
    return df


def import_league():
    df = read_excel(TEAMS_PATH)
    team_colors = [df.loc[i, "Color"] for i in range(NUM_OF_TEAMS)]
    league_dict = {
        "ID": list(df["ID"]),
        "Color": [COLOR_DICT[team_colors[i]] for i in range(NUM_OF_TEAMS)],
        "Name": list(df["Name"]),
        "touchdowns": [0 for _ in range(NUM_OF_TEAMS)],
        "conceded": [0 for _ in range(NUM_OF_TEAMS)],
        "ratio": [0 for _ in range(NUM_OF_TEAMS)],
        "points": [0 for _ in range(NUM_OF_TEAMS)]
    }
    return DataFrame(league_dict)

"""
def create_empty_stats_dict() -> DataFrame:
    # TODO: maybe add training and improvement

    total_num_of_players = NUM_OF_PLAYERS_IN_TEAM * NUM_OF_TEAMS
    stats_dict = {
        "ID": [i for i in range(total_num_of_players)],
        "sets_played": [0 for _ in range(total_num_of_players)],
        "offence_scores_list": [[] for _ in range(total_num_of_players)],
        "defence_scores_list": [[] for _ in range(total_num_of_players)],
        "rating_list": [[] for _ in range(total_num_of_players)],
        "distance_covered": [0 for _ in range(total_num_of_players)],
        "distance_carried": [0 for _ in range(total_num_of_players)],
        "distance_passed": [0 for _ in range(total_num_of_players)],
        "touchdowns": [0 for _ in range(total_num_of_players)],
        "turns_in_touchdown_strip": [0 for _ in range(total_num_of_players)],
        "creations": [0 for _ in range(total_num_of_players)],
        "end_zone_creation": [0 for _ in range(total_num_of_players)],  # TODO: add to player
        "evasions": [0 for _ in range(total_num_of_players)],
        "carrier_evasions": [0 for _ in range(total_num_of_players)],
        "successful_shots": [0 for _ in range(total_num_of_players)],
        "successful_takedowns": [0 for _ in range(total_num_of_players)],
        "last_ditch_hits": [0 for _ in range(total_num_of_players)],
        "last_ditch_takedowns": [0 for _ in range(total_num_of_players)],
        "carrier_takedowns": [0 for _ in range(total_num_of_players)],
        "hits_taken": [0 for _ in range(total_num_of_players)],
        "balance_losses": [0 for _ in range(total_num_of_players)],
        "drops_made": [0 for _ in range(total_num_of_players)],
        "passes_made": [0 for _ in range(total_num_of_players)],
        "catches made": [0 for _ in range(total_num_of_players)],
        "assists": [0 for _ in range(total_num_of_players)],
        "control_losses": [0 for _ in range(total_num_of_players)],
        "average_offence_score": [0 for _ in range(total_num_of_players)],
        "average_defence_score": [0 for _ in range(total_num_of_players)],
        "average_rating": [0 for _ in range(total_num_of_players)]
    }
    stats_df = DataFrame(stats_dict)
    for column_name in ["average_offence_score", "average_defence_score", "average_rating"]:
        stats_df[column_name] = stats_df[column_name].astype(float)
    return stats_df
"""


####
def create_players(path) -> DataFrame:
    total_num_of_players = NUM_OF_PLAYERS_IN_TEAM * NUM_OF_TEAMS
    player_ability_dict = {
        "ID": [i for i in range(total_num_of_players)],
        "Name": [get_first_name("Male") for _ in range(total_num_of_players)],
        "Team": [TEAMS[i] for i in range(NUM_OF_TEAMS) for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "Color": [COLORS[i] for i in range(NUM_OF_TEAMS) for _ in range(NUM_OF_PLAYERS_IN_TEAM)],
        "Shirt number": [i + 1 for _ in range(NUM_OF_TEAMS) for i in range(NUM_OF_PLAYERS_IN_TEAM)],
        "speed": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "agility": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "creating": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "shooting": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "stability": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "distribution": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "control": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)],
        "stamina": [random_gaussian_number(65, 15, 0, 100) for _ in range(total_num_of_players)]
    }
    players_df = DataFrame(player_ability_dict)
    players_df.to_excel(path, index=False)
    return players_df


###
def import_players():
    return read_excel(PLAYERS_PATH)


def clear_table(table_name: DataFrame):
    table_name.loc[:, :] = 0


def update_stats_table_from_another(source_table: DataFrame, receiving_table: DataFrame):
    source_table["ID"] = 0
    return receiving_table + source_table


def update_averages(player_id: int, stats_table: DataFrame, is_season: bool):
    for score, score_list in zip(
            ["average_offence_score", "average_defence_score", "average_rating"],
            ["offence_scores_list", "defence_scores_list", "rating_list"]):
        if len(stats_table.loc[player_id, score_list]) < 5 and is_season:
            stats_table.loc[player_id, score] = -1
        else:
            stats_table.loc[player_id, score] = \
                round(Series(stats_table.loc[player_id, score_list]).mean(), 2)


def update_ratio(team_name: str, table: DataFrame):
    ratio = \
        (table.loc[table["Name"] == team_name, "touchdowns"] * 100 // table.loc[table["Name"] == team_name, "conceded"])
    table.loc[table["Name"] == team_name, "ratio"] = ratio


def update_league_table(left_team_name: str, right_team_name: str, match_summary: dict, table: DataFrame):
    left_won = True if match_summary["left score"] > match_summary["right score"] else False
    left_summary = {
        "touchdowns": match_summary["left score"],
        "conceded": match_summary["right score"],
        "points": match_summary["left score"]
    }
    right_summary = {
        "touchdowns": match_summary["right score"],
        "conceded": match_summary["left score"],
        "points": match_summary["right score"]
    }

    if left_won:
        left_summary["points"] += match_summary["left score"] - match_summary["right score"]
    else:
        right_summary["points"] += match_summary["right score"] - match_summary["left score"]

    for key, value in left_summary.items():
        table.loc[table["Name"] == left_team_name, key] += value
    for key, value in right_summary.items():
        table.loc[table["Name"] == right_team_name, key] += value
    for team in [left_team_name, right_team_name]:
        update_ratio(team, table)


def show_league(table: DataFrame):
    sorted_table = table.sort_values(by=["points", "ratio"], ascending=False).loc[:, "Name":]
    sorted_ids = table.sort_values(by=["points", "ratio"], ascending=False).loc[:, "ID"].to_list()
    sorted_table = sorted_table.to_string(index=False).split("\n")
    print_head = True
    for row_num in range(NUM_OF_TEAMS + 1):
        if print_head:
            print(COLOR_RESET, " ", sorted_table[row_num])
            print_head = False
        else:
            color_name = COLORS[sorted_ids[row_num - 1]]
            print("".join([str(row_num) + "  ", COLOR_DICT[color_name], sorted_table[row_num], COLOR_RESET]))

    print("\n")


def find_top_players(stats_table: DataFrame):
    keys_list = list(stats_table.keys())
    first_index = keys_list.index("distance_covered")
    top_players_list = []
    arranged_stats = []
    for stat in keys_list[first_index:]:
        sorted_table = stats_table.sort_values(by=[stat], ascending=False)
        top_index = int(sorted_table["ID"].iloc[0])
        if top_index in top_players_list:
            arranged_stats[top_players_list.index(top_index)].append(stat)
        else:
            top_players_list.append(top_index)
            arranged_stats.append([stat])

    return top_players_list, arranged_stats


def assign_value_to_stat(stat):
    if stat < 65:
        return 0
    if stat < 75:
        return 2
    if stat < 80:
        return 5
    if stat < 85:
        return 15
    if stat < 90:
        return 25
    temp = stat - 90
    return 30 + (temp * 5)
