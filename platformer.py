# FIXME: There are 2 types of position - relative and absolute, must decide which is better for collision etc.
# IDEA: What about using masks for collision?
# TODO: Make window size flexible, don't work on numbersa

import pygame

from classes.cam import Cam
from classes.map import Map
from classes.tooltip import Tooltip


class Game(object):
    def __init__(self):
        self._running = True
        self._fps = 30
        self.window_size = (1000, 600)

        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)

        self.map_surface = pygame.Surface((800, 600))
        self.inventory_surface = pygame.Surface((200, 600))

        pygame.display.set_caption("Dungeon-RPG")

        self.clock = pygame.time.Clock()

        self.map = Map("map.tmx")

        # Init camera
        Cam.x = 800/2-self.map.player.x
        Cam.y = 600/2-self.map.player.y

        self.font = pygame.font.Font("media/fonts/munro_small.ttf", 22)

        self.tooltip = None

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.USEREVENT:
                self.tooltip = self.font.render(event.msg, True, (0, 0, 0))
            # KEYS
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                elif event.key == pygame.K_SPACE:
                    self.map.player.attack()
            # MOUSE
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Make it short
                if self.map.player.inventory.collide_inventory(pygame.mouse.get_pos()):
                    self.map.player.inventory.equip(self.map.player.inventory.collide_inventory(pygame.mouse.get_pos()))
                elif self.map.player.inventory.collide_equipped(pygame.mouse.get_pos()):
                    self.map.player.inventory.unequip(self.map.player.inventory.collide_equipped(pygame.mouse.get_pos()))


        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.map.player.move_left()
        elif keys[pygame.K_d]:
            self.map.player.move_right()
        elif keys[pygame.K_w]:
            self.map.player.move_top()
        elif keys[pygame.K_s]:
            self.map.player.move_down()

    # TODO: Clear it and decide where should be all updates
    def updates(self):
        self.map.update()

    def run(self):
        while self._running:
            self.events()
            self.updates()

            self.map_surface.fill(((9, 7, 10)))
            self.inventory_surface.blit(pygame.image.load("media/panel.png"), (0, 0))
            # self.screen.fill((9, 7, 10))

            self.map.background_tiles.draw(self.map_surface)
            self.map.collision_tiles.draw(self.map_surface)
            self.map.items.draw(self.map_surface)

            self.map.player.inventory.draw(self.inventory_surface)

            self.map_surface.blit(self.font.render(str(self.clock.get_fps()), True, (255, 255, 255)), (10, 10))
            self.inventory_surface.blit(self.font.render("Piniondze: " + str(self.map.player.inventory.gold) + " BTC", True, (255, 255, 255)), (10, 10))

            # TODO: Made fast, consider if its good
            # IDEA: A co gdyby go zawsze rysować, a jego wyglądem sterować z klasy Player?
            # IDEA: Make animations sprite group?
            # Draws sword when attacking
            if self.map.player.attacking:
                print(self.map.player.sprite_row)
                # FIXME: Rotating change sprite size. That's why deltas are different
                delta_x = 0
                delta_y = 0
                if self.map.player.sprite_row == 1:
                    flip = True
                    delta_x = -24
                elif self.map.player.sprite_row == 2:
                    flip = False
                    delta_x = 16
                elif self.map.player.sprite_row == 3:
                    flip = True
                    delta_y = -16
                elif self.map.player.sprite_row == 0:
                    flip = False
                    delta_y = 32

                self.map_surface.blit(
                    pygame.transform.flip(pygame.transform.rotate(
                        self.map.player.inventory.get_equipped_weapon().image,
                        -self.map.player.attacking_time * 8), flip, False),
                    (400 + delta_x, 300 + delta_y))

            # Blit tooltip if exists
            if self.tooltip:
                self.map_surface.blit(self.tooltip, pygame.mouse.get_pos())
                self.tooltip = None

            self.map_surface.blit(self.map.player.image, (self.map.player.rect.x, self.map.player.rect.y))

            self.screen.blit(self.map_surface, (0, 0))
            self.screen.blit(self.inventory_surface, (800, 0))

            pygame.display.flip()
            self.clock.tick(self._fps)

        pygame.quit()


game = Game()
game.run()
