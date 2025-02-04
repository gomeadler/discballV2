from enum import Enum


class Color(Enum):  # TODO: use it in code
    COLOR_RESET = '\033[0m'
    BLACK = "\033[30m"
    WHITE = "\033[37m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    PURPLE = "\033[38;5;129m"
    ORANGE = "\033[38;5;202m"
    PINK = "\033[38;5;213m"
    LIME = "\033[38;5;154m"
    TEAL = "\033[38;5;37m"
    GRAY = "\033[38;5;240m"
    BROWN = "\033[38;5;124m"


NUM_OF_PLAYERS_IN_TEAM = 8
NUM_OF_PLAYERS_IN_LINE_UP = 5
NUM_OF_TEAMS = 8
POINTS_FOR_WIN = 10
PLAYERS_PATH = r"C:\Users\gomea\PycharmProjects\disc_game_pandas\players_excel.xlsx"
TEAMS_PATH = r"C:\Users\gomea\PycharmProjects\disc_game_pandas\teams_excel.xlsx"


COLOR_RESET = '\033[0m'
COLOR_DICT = {
    "black": "\033[30m",
    "white": "\033[37m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "purple": "\033[38;5;129m",
    "orange": "\033[38;5;202m",
    "pink": "\033[38;5;213m",
    "lime": "\033[38;5;154m",
    "teal": "\033[38;5;37m",
    "gray": "\033[38;5;240m",
    "brown": "\033[38;5;124m"
}


def paint(string: str, color: Color):
    return "".join([color.value, string, Color.COLOR_RESET.value])


#  TODO: change this
TEAMS = ["Team A", "Team B", "Team C", "Team D", "Team E", "Team F", "Team G", "Team H"]
COLORS = ["red", "blue", "green", "yellow", "magenta", "orange", "gray", "brown"]
