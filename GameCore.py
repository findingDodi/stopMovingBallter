import pygame
import math

import conf


class GameCore:

    def __init__(self):
        self.screen = None
        self.screen_width = conf.SCREEN_SIZE[0]
        self.screen_height = conf.SCREEN_SIZE[1]
        self.game_is_running = True
        self.game_is_over = False
        self.background_rect = pygame.Rect(0, 0, self.screen_width, self.screen_height)

        self.last_event = None

        self.wall_width = 10
        self.wall_height = 200
        self.wall_position_x = self.screen_width - self.wall_width * 2
        self.wall_position_y = self.screen_height / 2
        self.wall_speed = 1
        self.wall_color = (190, 190, 190)

        self.ball_position_x = 20
        self.ball_position_y = self.screen_height / 2
        self.ball_radius = 10
        self.ball_speed = 1
        self.ball_color = (250, 50, 50)

    def draw_wall(self):
        pygame.draw.rect(
            self.screen,
            self.wall_color,
            (
                self.wall_position_x,
                self.wall_position_y,
                self.wall_width,
                self.wall_height
            )
        )

    def draw_ball(self):
        pygame.draw.circle(
            self.screen,
            self.ball_color,
            (
                self.ball_position_x,
                self.ball_position_y
            ),
            self.ball_radius
        )

    def move_wall(self):
        self.wall_position_y += self.wall_speed

    def move_ball(self):
        if self.last_event == pygame.K_RETURN:
            self.ball_position_x += self.ball_speed

    def ball_control(self, event):
        if event.key == pygame.K_RETURN:
            self.last_event = pygame.K_RETURN

    def border_patrol(self):
        if self.ball_position_x > self.screen_width:
            self.game_is_over = True

        if self.wall_position_y < 0:
            self.wall_position_y = 0
            self.wall_speed = 1
        elif self.wall_position_y > self.screen_height - self.wall_height:
            self.wall_position_y = self.screen_height - self.wall_height
            self.wall_speed = -1

    def collision_police(self):
        pass

    def run_game(self):

        pygame.init()
        pygame.display.set_caption("Stop Moving Ballter!!")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)
        clock = pygame.time.Clock()
        self.game_is_running = True

        while self.game_is_running:
            # limit framespeed to 30fps
            clock.tick(30)
            self.screen.fill((55, 55, 55), self.background_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_is_running = False
                    else:
                        self.ball_control(event)

            for i in range(5):
                self.move_wall()
                self.move_ball()
                self.border_patrol()
                self.draw_wall()
                self.draw_ball()

            # final draw
            pygame.display.flip()
