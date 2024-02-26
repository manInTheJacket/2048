# Library for encoding and decoding JSON data
import json
# Library for interacting with the operating system
import os
# Library providing access to variables and functions related to the Python interpreter
import sys
from pathlib import Path

import pygame as pg

from src import config, database
from src.board import GameBoard
from src.config import BG_PATH, CAPTION, ELEMENTS_PATH, MIN_NAME_LENGTH, resource_path
from src.interface import Interface
from src.logics import get_side, quick_copy

# Dictionary containing paths to audio tracks for different game states
audio_tracks = {
    "game": "music/Rachmaninoff - Prelude in G minor, op. 23, No. 5.mp3",
    "menu": "music/С. В. Рахманинов - Остров мёртвых.mp3",
}

# Function to play music based on the provided track ID
def play_music(track_id):
    if track_id in audio_tracks:
        pg.mixer.music.load(audio_tracks[track_id])
        pg.mixer.music.play(-1)
    else:
        print(f"Music with ID '{track_id}' not found.")

# Main game class inheriting from Interface
class App(Interface):
    board: GameBoard
    copy_board: list
    move_mouse: bool
    position: tuple[int, int]
    def __init__(self) -> None:
        super().__init__()
        self.board = GameBoard()
        self.move_mouse = False

    # Method to handle the screen for entering a username
    def put_name(self) -> None:
        def _render(game: Interface) -> None:
            name_bg = pg.image.load(resource_path(BG_PATH / Path("input_username.jpg")))
            menu = pg.image.load(resource_path(ELEMENTS_PATH / Path("home.png")))
            game.screen.blit(
                pg.font.Font(game.generalFont, 120).render(CAPTION, True, config.COLORS["WHITE"]),
                (108, 60),
            )
            game.screen.blit(name_bg, (0, 0))
            game.screen.blit(pg.transform.scale(menu, [50, 50]), (236, 494))
            game.screen.blit(
                pg.font.Font(game.generalFont, 45).render("OK", True, config.COLORS["WHITE"]),
                (229, 371),
            )

        active_colour = "#013df2"
        inactive_colour = "#33346b"
        ok_box = pg.Rect(118, 383, 289, 80)
        input_box = pg.Rect(118, 283, 289, 80)
        menu_box = pg.Rect(225, 483, 75, 75)

        _render(self)
        font_input = pg.font.Font(self.generalFont, 48)
        pg.draw.rect(self.screen, color := inactive_colour, input_box, 1, border_radius=15)
        pg.display.update()

        name = ""
        active = False
        input_name = False
        while not input_name:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    active = bool(input_box.collidepoint(event.pos))
                    if ok_box.collidepoint(event.pos):
                        if len(name) >= MIN_NAME_LENGTH:
                            self.username = name
                            input_name = True
                    elif menu_box.collidepoint(event.pos):
                        self.draw_menu()
                        return
                    color = active_colour if active else inactive_colour
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
                    if active:
                        if event.key == pg.K_RETURN:
                            if len(name) >= MIN_NAME_LENGTH:
                                self.username = name
                                input_name = True
                        elif event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        elif font_input.render(name, True, config.COLORS["WHITE"]).get_width() < 261:
                            name += event.unicode
            _render(self)
            if name == "" and color == inactive_colour:
                self.screen.blit(font_input.render("Username", True, config.COLORS["GRAY"]), (155, 267))
            txt = font_input.render(name, True, config.COLORS["WHITE"])
            pg.draw.rect(self.screen, color, input_box, 1, border_radius=15)
            self.screen.blit(txt, (input_box.w - txt.get_width() // 2 - 26, 267))
            pg.display.update()

    # Method to load the last saved game
    def load_game(self) -> None:
        path = Path.cwd()

        if "save.txt" in os.listdir(path):
            with open("save.txt") as file:
                data = json.load(file)
                self.board = GameBoard(data["board"])
                self.score = data["score"]
                self.username = data["user"]
            full_path = path / Path("save.txt")
            Path(full_path).unlink()
        else:
            super().__init__()
            self.board = GameBoard()
            self.move_mouse = False

    # Method to save the current game state
    def save_game(self) -> None:
        data = {"user": self.username, "score": self.score, "board": self.board.get_mas}
        with open("save.txt", "w") as outfile:
            json.dump(data, outfile)

    # Method to update the game state, draw the main screen, and update the display
    def update(self) -> None:
        self.board.insert_in_mas()
        self.draw_main()
        pg.display.update()

    # Method to check for victory on the board
    def is_victory(self) -> bool:
        return any(2048 in row for row in self.board)

    # Method to draw the screen when the "around arrow" is clicked during play
    def around_arrow(self) -> None:
        cancel_box = pg.Rect(145, 415, 150, 70)
        repeat_box = pg.Rect(305, 415, 150, 70)

        blur = pg.Surface((self.width, self.height), pg.SRCALPHA)
        blur.fill((0, 0, 0, 140))
        self.screen.blit(blur, (0, 0))

        self.screen.blit(
            pg.font.Font(self.generalFont, 53).render("Reset game?", True, config.COLORS["WHITE"]),
            (60, 200),
        )
        font_h3 = pg.font.Font(self.generalFont, 32)
        self.screen.blit(
            font_h3.render("Are you sure you wish to", True, config.COLORS["WHITE"]),
            (60, 300),
        )
        self.screen.blit(font_h3.render("reset the game?", True, config.COLORS["WHITE"]), (60, 340))

        pg.draw.rect(self.screen, (110, 110, 110), cancel_box, border_radius=12)
        self.screen.blit(font_h3.render("Cancel", True, config.COLORS["WHITE"]), (174, 413))

        pg.draw.rect(self.screen, (110, 110, 110), repeat_box, border_radius=12)
        self.screen.blit(font_h3.render("Reset", True, config.COLORS["WHITE"]), (341, 413))
        pg.display.update()

        make_decision = False
        while not make_decision:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.save_game()
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key in (pg.K_BACKSPACE, pg.K_ESCAPE):  # cancel
                        self.update()
                        make_decision = True
                    elif event.key == pg.K_RETURN:  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.update()
                        make_decision = True
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if cancel_box.collidepoint(event.pos):  # cancel
                        self.update()
                        make_decision = True
                    elif repeat_box.collidepoint(event.pos):  # reset
                        super().__init__()
                        self.board = GameBoard()
                        self.update()
                        make_decision = True

    # Method to revert to the previous state when the "back arrow" is clicked during play
    def back_arrow(self) -> None:
        if self.copy_board is not None and self.copy_board != self.board.get_mas:
            self.board.get_mas = [list(row) for row in self.copy_board]
            self.score = self.old_score
            self.draw_main()
            pg.display.update()

    # Method to handle all user events
    def handle_events(self) -> bool:
        repeat_box = pg.Rect(447, 153, 58, 58)
        menu_box = pg.Rect(305, 153, 58, 58)
        back_arrow_box = pg.Rect(376, 153, 58, 58)
        play_ground = pg.Rect(15, 225, 488, 488)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.save_game()
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:  # Clicked on the mouse button
                if menu_box.collidepoint(event.pos):  # Menu
                    database.insert_result(self.username, self.score)
                    self.username = None
                    return True
                if back_arrow_box.collidepoint(event.pos):  # Back arrow
                    self.back_arrow()
                elif repeat_box.collidepoint(event.pos):  # Encapsulated arrow
                    self.around_arrow()
                elif play_ground.collidepoint(event.pos):  # Swipe mouse part 1
                    self.move_mouse = True
                    self.position = event.pos
            elif event.type == pg.MOUSEBUTTONUP:  # Released the mouse button
                if self.move_mouse:  # Swipe mouse part 2
                    self.move_mouse = False
                    if self.position != event.pos:
                        source_swipe = get_side(self.position, event.pos)
                        if source_swipe[1] > 30:
                            command_side = {
                                "UP": self.board.move_up,
                                "DOWN": self.board.move_down,
                                "LEFT": self.board.move_left,
                                "RIGHT": self.board.move_right,
                            }
                            self.copy_board = quick_copy(self.board)
                            command_side[source_swipe[0]](self)
                            self.update()
                            if self.is_victory():
                                self.draw_victory()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.save_game()
                    pg.quit()
                    sys.exit()
                elif event.key in (pg.K_LEFT, pg.K_a):  # Left
                    self.copy_board = quick_copy(self.board)
                    self.board.move_left(self)
                elif event.key in (pg.K_RIGHT, pg.K_d):  # Right
                    self.copy_board = quick_copy(self.board)
                    self.board.move_right(self)
                elif event.key in (pg.K_UP, pg.K_w):  # Up
                    self.copy_board = quick_copy(self.board)
                    self.board.move_up(self)
                elif event.key in (pg.K_DOWN, pg.K_s):  # Down
                    self.copy_board = quick_copy(self.board)
                    self.board.move_down(self)
                self.update()
                if self.is_victory():
                    self.draw_victory()
        return False

    # timer checker to stop game
    def time_check(self):
        if self.timer <= 0:
            return False
        return True

    # Main game loop
    def run(self) -> None:
        try:
            while True:
                pg.mixer.music.stop()
                self.load_game()
                if self.username is None:
                    play_music("menu")
                    self.draw_menu()
                    self.show_cutscene_one()
                    self.show_cutscene_Two()
                    play_music("game")
                self.draw_main()
                while self.board.are_there_zeros() and self.board.can_move() and self.time_check():
                    pg.display.update()
                    if self.handle_events() is True:
                        pg.mixer.music.stop()
                        break
                    self.update_timer()
                    self.draw_timer()
                    pg.display.update()
                    self.clock.tick(self.framerate)
                else:
                    self.draw_game_over()
        except Exception as exc:
            self.save_game()
            raise exc from None