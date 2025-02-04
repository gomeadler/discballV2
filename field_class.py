from constants import Color, NUM_OF_PLAYERS_IN_LINE_UP, paint


class Block:
    def __init__(self, color, row_coordinate, col_coordinate):
        self._occupied: bool = False
        self._default_color = color
        self._color: Color = color
        self._row_coordinate = row_coordinate
        self._col_coordinate = col_coordinate

    @property
    def col_coordinate(self):
        return self._col_coordinate

    def light_up(self, color: Color):
        text = "*" if self._occupied else " "
        return paint(text, color)

    def set_color(self, color: Color):
        self._color = color

    def inhabit_block(self):
        self._occupied = True

    def clear_block(self):
        self._occupied = False
        self._color = self._default_color


class Row:
    _id_counter = 0  # Static counter for unique IDs
    _all_instances = []  # Static list to keep track of all instances

    def __init__(self, color_left, color_right):
        self._id = Row._id_counter
        Row._id_counter += 1
        self.row_list = [Block(color_left, self._id, i) for i in range(11)] + \
                        [Block(color_right, self._id, j) for j in range(11, 22)]
        self.row_string = ""

    def make_row_str(self, column, player_color: Color):
        row_lst = []
        for block in self.row_list:
            block.clear_block()
            if block.col_coordinate == column:
                block.inhabit_block()
            row_lst.append(block.light_up(player_color))
        return "|".join(row_lst)


class Field:

    def __init__(self, color_left, color_right, carrier_color):
        self._field_matrice = [Row(color_left, color_right) for _ in range(NUM_OF_PLAYERS_IN_LINE_UP * 2)]
        self._color_left: Color = color_left
        self._color_right: Color = color_right
        self._carrier_color: Color = carrier_color

    def print_field(self, columns, carrier_row):
        field_lst = []
        for i in range(NUM_OF_PLAYERS_IN_LINE_UP * 2):
            if i % 2 == 0:
                color = self._color_left
            else:
                color = self._color_right
            if i == carrier_row:
                color = self._carrier_color
            field_lst.append(self._field_matrice[i].make_row_str(columns[i], color))
        print("\n".join(field_lst))
