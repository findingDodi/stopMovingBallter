import pygame
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

        self.wall_width = conf.WALL_WIDTH
        self.wall_height = conf.WALL_HEIGHT
        self.wall_position_x = conf.WALL_START_POS_X
        self.wall_position_y = conf.WALL_START_POS_Y
        self.wall_speed = 1
        self.wall_color = (190, 190, 190)
        self.wall_rect = None

        self.ball_position_x = conf.BALL_START_POS_X
        self.ball_position_y = conf.BALL_START_POS_Y
        self.ball_radius = conf.BALL_RADIUS
        self.ball_speed = 2
        self.ball_color = (250, 50, 50)
        self.ball_rect = None

    def draw_wall(self):
        self.wall_rect = pygame.draw.rect(
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
        self.ball_rect = pygame.draw.circle(
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

    def update_wall_height(self):
        self.wall_height /= 1.5

    def reset_wall_height(self):
        self.wall_height = conf.WALL_HEIGHT

    def reset_positions(self):
        self.ball_position_x = conf.BALL_START_POS_X
        self.wall_position_y = conf.WALL_START_POS_Y

    def ball_control(self, event):
        if event.key == pygame.K_RETURN:
            self.last_event = pygame.K_RETURN

    def border_patrol(self):
        if self.ball_position_x > self.screen_width:
            self.ball_speed = 0
            self.game_is_over = True

        if self.wall_position_y < 0:
            self.wall_position_y = 0
            self.wall_speed = 1
        elif self.wall_position_y > self.screen_height - self.wall_height:
            self.wall_position_y = self.screen_height - self.wall_height
            self.wall_speed = -1

    def collision_police(self):
        if self.ball_rect.colliderect(self.wall_rect):
            self.last_event = None
            self.reset_positions()
            self.update_wall_height()

    def draw_game_over_screen(self):
        if self.game_is_over:
            font = pygame.font.SysFont('Open Sans', 40)
            font_color = (255, 255, 255)
            font_position = ((conf.SCREEN_SIZE[0] / 2 - 90), conf.SCREEN_SIZE[1] / 2 - 30)
            font_position2 = ((conf.SCREEN_SIZE[0] / 2 - 160), conf.SCREEN_SIZE[1] / 2 + 10)
            self.screen.fill((55, 55, 55), self.background_rect)
            self.screen.blit(font.render('GAME OVER', True, font_color), font_position)
            self.screen.blit(font.render('PRESS R TO RESTART', True, font_color), font_position2)

    def restart_game(self):
        if self.game_is_over:
            self.reset_wall_height()
            self.reset_positions()
            self.ball_speed = 2
            self.last_event = None
            self.game_is_over = False

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
                    elif event.key == pygame.K_r:
                        self.restart_game()
                    else:
                        self.ball_control(event)

            if not self.game_is_over:
                for i in range(5):
                    self.move_wall()
                    self.move_ball()

                    self.draw_wall()
                    self.draw_ball()

                    self.border_patrol()
                    self.collision_police()
            else:
                self.draw_game_over_screen()

            # final draw
            pygame.display.flip()
