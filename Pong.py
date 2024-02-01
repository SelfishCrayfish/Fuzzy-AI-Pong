from typing import Type
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pygame

# import skfuzzy as fuzz
# import skfuzzy.control as fuzzcontrol

FPS = 60


class Board:
    def __init__(self, width: int, height: int):
        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("AIFundamentals - PongGame")

    def draw(self, *args):
        background = (0, 0, 0)
        self.surface.fill(background)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()


class Drawable:
    def __init__(self, x: int, y: int, width: int, height: int, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface(
            [width, height], pygame.SRCALPHA, 32
        ).convert_alpha()
        self.rect = self.surface.get_rect(x=x, y=y)

    def draw_on(self, surface):
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    def __init__(
            self,
            x: int,
            y: int,
            radius: int = 20,
            color=(255, 10, 0),
            speed: int = 3,
    ):
        super(Ball, self).__init__(x, y, radius, radius, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed = speed
        self.y_speed = speed
        self.start_speed = speed
        self.start_x = x
        self.start_y = y
        self.start_color = color
        self.last_collision = 0

    def bounce_y(self):
        self.y_speed *= -1

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y_power(self):
        self.color = (
            self.color[0],
            self.color[1] + 10 if self.color[1] < 255 else self.color[1],
            self.color[2],
        )
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])
        self.x_speed *= 1.1
        self.y_speed *= 1.1
        self.bounce_y()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.x_speed = self.start_speed
        self.y_speed = self.start_speed
        self.color = self.start_color
        self.bounce_y()

    def move(self, board: Board, *args):
        self.rect.x += round(self.x_speed)
        self.rect.y += round(self.y_speed)

        if self.rect.x < 0 or self.rect.x > (
                board.surface.get_width() - self.rect.width
        ):
            self.bounce_x()

        if self.rect.y < 0 or self.rect.y > (
                board.surface.get_height() - self.rect.height
        ):
            self.reset()

        timestamp = pygame.time.get_ticks()
        if timestamp - self.last_collision < FPS * 4:
            return

        for racket in args:
            if self.rect.colliderect(racket.rect):
                self.last_collision = pygame.time.get_ticks()
                if (self.rect.right < racket.rect.left + racket.rect.width // 4) or (
                        self.rect.left > racket.rect.right - racket.rect.width // 4
                ):
                    self.bounce_y_power()
                else:
                    self.bounce_y()


class Racket(Drawable):
    def __init__(
            self,
            x: int,
            y: int,
            width: int = 80,
            height: int = 20,
            color=(255, 255, 255),
            max_speed: int = 10,
    ):
        super(Racket, self).__init__(x, y, width, height, color)
        self.max_speed = max_speed
        self.surface.fill(color)

    def move(self, x: int, board: Board):
        delta = x - self.rect.x
        delta = self.max_speed if delta > self.max_speed else delta
        delta = -self.max_speed if delta < -self.max_speed else delta
        delta = 0 if (self.rect.x + delta) < 0 else delta
        delta = (
            0
            if (self.rect.x + self.width + delta) > board.surface.get_width()
            else delta
        )
        self.rect.x += delta


class Player:
    def __init__(self, racket: Racket, ball: Ball, board: Board) -> None:
        self.ball = ball
        self.racket = racket
        self.board = board

    def move(self, x: int):
        self.racket.move(x, self.board)

    def move_manual(self, x: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass

    def act(self, x_diff: int, y_diff: int):
        """
        Do nothing, control is defined in derived classes
        """
        pass


class PongGame:
    def __init__(
            self, width: int, height: int, player1: Type[Player], player2: Type[Player]
    ):
        pygame.init()
        self.board = Board(width, height)
        self.fps_clock = pygame.time.Clock()
        self.ball = Ball(width // 2, height // 2)

        self.opponent_paddle = Racket(x=width // 2, y=0)
        self.oponent = player1(self.opponent_paddle, self.ball, self.board)

        self.player_paddle = Racket(x=width // 2, y=height - 20)
        self.player = player2(self.player_paddle, self.ball, self.board)

    def run(self):
        while not self.handle_events():
            self.ball.move(self.board, self.player_paddle, self.opponent_paddle)
            self.board.draw(
                self.ball,
                self.player_paddle,
                self.opponent_paddle,
            )
            self.oponent.act(
                self.oponent.racket.rect.centerx - self.ball.rect.centerx,
                self.oponent.racket.rect.centery - self.ball.rect.centery,
            )
            self.player.act(
                self.player.racket.rect.centerx - self.ball.rect.centerx,
                self.player.racket.rect.centery - self.ball.rect.centery,
            )
            self.fps_clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                return True
        keys = pygame.key.get_pressed()
        if keys[pygame.constants.K_LEFT]:
            self.player.move_manual(0)
        elif keys[pygame.constants.K_RIGHT]:
            self.player.move_manual(self.board.surface.get_width())
        return False


class NaiveOponent(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(NaiveOponent, self).__init__(racket, ball, board)

    def act(self, x_diff: int, y_diff: int):
        x_cent = self.ball.rect.centerx
        self.move(x_cent)


class HumanPlayer(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(HumanPlayer, self).__init__(racket, ball, board)

    def move_manual(self, x: int):
        self.move(x)


# ----------------------------------
# DO NOT MODIFY CODE ABOVE THIS LINE
# ----------------------------------


# The FuzzyPlayer class contains all the logic needed to accomplish the task described in README
# In short, I used TSK method to create rules that control the racket and its speed in relation to the
# ball's location on the screen

HEIGHT = 400
WIDTH = 800
BALL_SPEED = 30


def verify_velocity(velocity_arg):
    if velocity_arg < -BALL_SPEED: return -BALL_SPEED
    if velocity_arg > BALL_SPEED:
        return BALL_SPEED
    else:
        return velocity_arg


class FuzzyPlayer(Player):
    def __init__(self, racket: Racket, ball: Ball, board: Board):
        super(FuzzyPlayer, self).__init__(racket, ball, board)

        distance_x = ctrl.Antecedent(universe=np.arange(-WIDTH, WIDTH + 1), label="x_dist", )
        distance_y = ctrl.Antecedent(universe=np.arange(0, HEIGHT + 1), label="y_dist")

        velocity = ctrl.Consequent(universe=np.arange(-BALL_SPEED, BALL_SPEED + 1), label="velocity")

        corners = racket.width / 2
        distance_x["left"] = fuzz.trimf(distance_x.universe, [-WIDTH, -WIDTH, -corners])
        distance_x["center"] = fuzz.trimf(distance_x.universe, [-WIDTH, 0, WIDTH])
        distance_x["right"] = fuzz.trimf(distance_x.universe, [corners, WIDTH, WIDTH])

        distance_y["high"] = fuzz.trimf(distance_y.universe, [HEIGHT // 2, HEIGHT, HEIGHT])
        distance_y["mid"] = fuzz.trimf(distance_y.universe, [0, HEIGHT // 2, HEIGHT])
        distance_y["low"] = fuzz.trimf(distance_y.universe, [0, 0, HEIGHT // 2])

        velocity["left"] = fuzz.trimf(velocity.universe, [-BALL_SPEED, -BALL_SPEED, 0])
        velocity["stay"] = fuzz.trimf(velocity.universe, [-BALL_SPEED, 0, BALL_SPEED])
        velocity["right"] = fuzz.trimf(velocity.universe, [0, BALL_SPEED, BALL_SPEED])

        rule1 = ctrl.Rule(
            distance_x["left"] & (distance_y["low"] | distance_y["mid"] | distance_y["high"]),
            velocity["left"]
        )
        rule2 = ctrl.Rule(
            distance_x["center"] & (distance_y["low"] | distance_y["mid"] | distance_y["high"]),
            velocity["stay"]
        )
        rule3 = ctrl.Rule(
            distance_x["right"] & (distance_y["low"] | distance_y["mid"] | distance_y["high"]),
            velocity["right"]
        )

        control_system = ctrl.ControlSystem(
            [
                rule1,
                rule2,
                rule3,
            ]
        )
        self.controller = ctrl.ControlSystemSimulation(control_system)
        distance_x.view()
        distance_y.view()
        velocity.view()
        plt.show()

    def act(self, x_diff: int, y_diff: int):
        velocity = self.make_decision(x_diff, y_diff)
        self.move(self.racket.rect.x + velocity)

    def make_decision(self, x_diff: int, y_diff: int):
        self.controller.input['x_dist'] = -x_diff
        self.controller.input['y_dist'] = y_diff

        self.controller.compute()

        retval = self.controller.output['velocity'] * 2137
        return verify_velocity(retval)


if __name__ == "__main__":
    # Line 'game = PongGame(800, 400, NaiveOponent, HumanPlayer)'
    # allows the user to enjoy a game of Pong against the computer opponent
    # Line 'game = PongGame(800, 400, NaiveOponent, FuzzyPlayer)'
    # shows how the fuzzy AI works against the computer opponent
    # Comment and uncomment them accordingly

    # game = PongGame(800, 400, NaiveOponent, HumanPlayer)
    game = PongGame(800, 400, NaiveOponent, FuzzyPlayer)
    game.run()
