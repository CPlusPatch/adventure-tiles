""" The main game file """

import threading
import time
import pygame
from pygame.constants import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_7,
    K_8,
    K_s,
    K_l,
    K_ESCAPE,
    QUIT,
)
from level import Level
from pos import Pos
from main import Entity
from variables import RESOLUTION, GameStates


class Game:
    """The main game class"""

    screen: pygame.Surface
    level: Level
    camera_position: Pos
    entities: pygame.sprite.Group
    player: Entity
    last_click: int
    last_keypress: int
    state: GameStates

    def __init__(self, screen: pygame.Surface):
        self.level = Level(Pos(10, 10), self)
        self.camera_position = Pos(3, 4)
        self.entities = pygame.sprite.Group()
        self.player = Entity(Pos(0, 0), Pos(16, 16))
        self.entities.add(self.player)
        self.screen = screen
        self.state = GameStates.PLAYING

    def move_camera(self, pos: Pos):
        """Move the camera to the given position"""
        self.camera_position = pos

    def resume(self):
        """Resume the game"""
        self.state = GameStates.PLAYING

    def pause(self):
        """Pause the game"""
        self.state = GameStates.MENU

    def quit(self):
        """Quit the game"""
        pygame.quit()
        print("Game closed")
        exit()

    def move_player(self):
        """Move the player"""
        INCREMENT = 0.2
        while True:
            if self.state == GameStates.PLAYING:
                keys = pygame.key.get_pressed()
                player0 = self.level.players["0"]
                if keys[K_UP]:
                    self.camera_position -= Pos(0, INCREMENT)
                    player0["pos"] -= Pos(0, INCREMENT)
                    player0["player"].set_direction(180)
                    player0["player"].is_walking = True

                if keys[K_DOWN]:
                    self.camera_position += Pos(0, INCREMENT)
                    player0["pos"] += Pos(0, INCREMENT)
                    player0["player"].set_direction(0)
                    player0["player"].is_walking = True

                if keys[K_LEFT]:
                    self.camera_position -= Pos(INCREMENT, 0)
                    player0["pos"] -= Pos(INCREMENT, 0)
                    player0["player"].set_direction(270)
                    player0["player"].is_walking = True

                if keys[K_RIGHT]:
                    self.camera_position += Pos(INCREMENT, 0)
                    player0["pos"] += Pos(INCREMENT, 0)
                    player0["player"].set_direction(90)
                    player0["player"].is_walking = True

                if (
                    not keys[K_UP]
                    and not keys[K_DOWN]
                    and not keys[K_LEFT]
                    and not keys[K_RIGHT]
                ):
                    player0["player"].is_walking = False
                time.sleep(0.05)

    def loop(self):
        """The main game loop"""
        self.last_click = pygame.time.get_ticks()
        self.last_keypress = pygame.time.get_ticks()

        player_thread = threading.Thread(target=self.move_player)
        player_thread.start()
        while True:
            # Check for pressed keys
            keys = pygame.key.get_pressed()

            if self.last_keypress + 100 < pygame.time.get_ticks():
                self.last_keypress = pygame.time.get_ticks()

                if self.state == GameStates.PLAYING:
                    # If S key is pressed, save game: if L key is pressed, load game
                    if keys[K_s]:
                        self.level.save()
                    if keys[K_l]:
                        self.level.load()

                    # If keys 1-9 are pressed, select the corresponding tile
                    if keys[K_1]:
                        self.level.selected_tile = 0
                    if keys[K_2]:
                        self.level.selected_tile = 1
                    if keys[K_3]:
                        self.level.selected_tile = 2
                    if keys[K_4]:
                        self.level.selected_tile = 3
                    if keys[K_5]:
                        self.level.selected_tile = 4
                    if keys[K_6]:
                        self.level.selected_tile = 5
                    if keys[K_7]:
                        self.level.selected_tile = 6
                    if keys[K_8]:
                        self.level.selected_tile = 7

                    # If any of these keys are pressed, reset ghost rotation to 0
                    if (
                        keys[K_1]
                        or keys[K_2]
                        or keys[K_3]
                        or keys[K_4]
                        or keys[K_5]
                        or keys[K_6]
                        or keys[K_7]
                        or keys[K_8]
                    ):
                        self.level.current_ghost_rotation = 0

                if keys[K_ESCAPE]:
                    if self.state == GameStates.PLAYING:
                        self.pause()
                    elif self.state == GameStates.MENU:
                        self.resume()

            self.screen.fill((0, 0, 0))
            self.level.render(self.camera_position)
            self.level.players["0"]["player"].update()
            self.entities.update()
            # game.entities.draw(game.screen)
            pygame.display.flip()

            # Cap at 60 FPS
            pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    print("Game closed")
                    exit()


if __name__ == "__main__":
    screen1 = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("The Game")
    pygame.font.init()
    pygame.display.init()
    game = Game(screen1)
    print("Game initialized")
    game.loop()
