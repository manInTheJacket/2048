from __future__ import annotations
# Importing necessary modules

from collections.abc import Iterator
from random import randint, random, shuffle
from typing import Any
# Importing functions from a custom module

from src.logics import get_index_from_number, get_number_from_index, quick_copy

# Defining a class for the game board
class GameBoard:
    # Class attribute to track if the board has moved
    is_board_move: bool = False

    # Initializing the game board
    def __init__(self, mas: list | None = None) -> None:

        # If the board is provided, use it; otherwise, create an empty one
        if mas is not None:
            self.__mas = mas
        else:
            self.__mas = [
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
                [0, 0, 0, 0],
            ]
        # Inserting two random numbers (2 or 4) into two random empty cells

        first_slot, second_slot = randint(1, 16), randint(1, 16)
        while first_slot == second_slot:
            first_slot, second_slot = randint(1, 16), randint(1, 16)

        self.insert_2_or_4(*get_index_from_number(first_slot))
        self.insert_2_or_4(*get_index_from_number(second_slot))

    # Overriding the __getitem__ method for convenient access to rows
    def __getitem__(self, item: int) -> list[int]:
        result: list[int] = self.__mas[item]
        return result

    # Overriding the __setitem__ method for updating rows
    def __setitem__(self, key: int, value: Any) -> None:
        self.__mas[key] = value

    # Implementing the Iterator protocol to iterate through rows
    def __iter__(self) -> Iterator:
        return iter(self.__mas)

    # Method to move the board to the left
    def move_left(self, game: Any) -> None:
        # Creating a copy of the current board state

        origin = quick_copy(self)
        # Resetting the game's delta attribute

        game.delta = 0
        # Moving non-zero elements to the left and filling with zeros

        for row in self:
            while 0 in row:
                row.remove(0)
            while len(row) != 4:
                row.append(0)
        # Merging adjacent equal numbers and updating the score

        for x in range(4):
            for y in range(3):
                if self[x][y] != 0 and self[x][y] == self[x][y + 1]:
                    self[x][y] *= 2
                    game.old_score = game.score
                    game.score += self[x][y]
                    game.delta += self[x][y]
                    self[x].pop(y + 1)
                    self[x].append(0)
        # Checking if the board has moved
        self.is_board_move = origin != self.get_mas

    #Similar to previous method
    def move_right(self, game: Any) -> None:
        origin = quick_copy(self)
        game.delta = 0
        for row in self:
            while 0 in row:
                row.remove(0)
            while len(row) != 4:
                row.insert(0, 0)

        for x in range(4):
            for y in range(3, 0, -1):
                if self[x][y] != 0 and self[x][y] == self[x][y - 1]:
                    self[x][y] *= 2
                    game.old_score = game.score
                    game.score += self[x][y]
                    game.delta += self[x][y]
                    self[x].pop(y - 1)
                    self[x].insert(0, 0)
        self.is_board_move = origin != self.get_mas

    #Similar to previous method
    def move_up(self, game: Any) -> None:
        origin = quick_copy(self)
        game.delta = 0
        for y in range(4):
            column = [self[x][y] for x in range(4) if self[x][y] != 0]
            while len(column) != 4:
                column.append(0)
            for x in range(3):
                if column[x] != 0 and column[x] == column[x + 1]:
                    column[x] *= 2
                    game.old_score = game.score
                    game.score += column[x]
                    game.delta += column[x]
                    column.pop(x + 1)
                    column.append(0)
            for x in range(4):
                self[x][y] = column[x]
        self.is_board_move = origin != self.get_mas

    #Similar to the previous method
    def move_down(self, game: Any) -> None:
        origin = quick_copy(self)
        game.delta = 0
        for y in range(4):
            column = [self[x][y] for x in range(4) if self[x][y] != 0]
            while len(column) != 4:
                column.insert(0, 0)
            for x in range(3, 0, -1):
                if column[x] != 0 and column[x] == column[x - 1]:
                    column[x] *= 2
                    game.old_score = game.score
                    game.score += column[x]
                    game.delta += column[x]
                    column.pop(x - 1)
                    column.insert(0, 0)
            for x in range(4):
                self[x][y] = column[x]
        self.is_board_move = origin != self.get_mas

    # Property to get the current state of the board
    @property
    def get_mas(self) -> list[list[int]]:
        """Get board as list."""
        return self.__mas

    # Setter for updating the board state
    @get_mas.setter
    def get_mas(self, value: Any) -> None:
        self.__mas = value

    # Method to check if there are empty cells on the board
    def are_there_zeros(self) -> bool:
        return any(0 in row for row in self)

    # Method to get a list of numbers corresponding to empty cells
    def get_empty_list(self) -> list:
        return [get_number_from_index(i, y) for i in range(4) for y in range(4) if self[i][y] == 0]

    # Method to insert a random 2 or 4 into an empty cell
    def insert_in_mas(self) -> None:
        # Checking if the board has moved and there are empty cells
        if self.is_board_move and self.are_there_zeros():
            self.is_board_move = False
            # Getting a list of empty cells, shuffling it, and selecting a random one
            empty = self.get_empty_list()
            shuffle(empty)
            random_num = empty.pop()
            x, y = get_index_from_number(random_num)
            # Inserting 2 or 4 into the selected cell
            self.insert_2_or_4(x, y)

    # Method to insert a random 2 or 4 into a specified cell
    def insert_2_or_4(self, x: int, y: int) -> None:
        # Randomly choosing whether to insert 2 or 4
        if random() <= 0.90:
            self[x][y] = 2
        else:
            self[x][y] = 4
    # Method to check if any valid moves can be made on the board
    def can_move(self) -> bool:
        for i in range(3):
            for y in range(3):
                if self[i][y] in (self[i][y + 1], self[i + 1][y]):
                    return True
        for i in range(3, 0, -1):
            for y in range(3, 0, -1):
                if self[i][y] in (self[i][y - 1], self[i - 1][y]):
                    return True
        return False