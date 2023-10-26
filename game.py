import pygame
from level import Level
from pos import Pos
from main import Entity
from variables import RESOLUTION

class Game:
    screen: pygame.Surface
    level: Level
    camera_position: Pos
    entities: pygame.sprite.Group
    player: Entity
    last_click: int

    def __init__(self, screen: pygame.Surface):
        self.level = Level(Pos(8, 8), self)
        self.camera_position = Pos(3, 4)
        self.entities = pygame.sprite.Group()
        self.player = Entity(Pos(0, 0), Pos(16, 16))
        self.entities.add(self.player)
        self.screen = screen
    
    def move_camera(self, pos: Pos):
        self.camera_position = pos
    
    def loop(self):
        self.last_click = pygame.time.get_ticks()
        while True:
            # Check for pressed keys
            keys = pygame.key.get_pressed()

            # Move the player
            # Throttle keypresses to 1 per 10 frames
            if keys[pygame.K_UP]:
                self.camera_position -= Pos(0, 1)
            if keys[pygame.K_DOWN]:
                self.camera_position += Pos(0, 1)
            if keys[pygame.K_LEFT]:
                self.camera_position -= Pos(1, 0)
            if keys[pygame.K_RIGHT]:
                self.camera_position += Pos(1, 0)
            
            game.screen.fill((0, 0, 0))
            game.level.render(game.camera_position)
            game.entities.update()
            #game.entities.draw(game.screen)
            pygame.display.flip()

            # Cap at 60 FPS
            pygame.time.Clock().tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print("Game closed")
                    exit()

if __name__ == "__main__":
    screen = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("The Game")
    pygame.font.init()
    pygame.display.init()
    game = Game(screen)
    print("Game initialized")
    game.loop()