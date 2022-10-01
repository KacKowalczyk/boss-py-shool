
# standard imports
import time
import math

# install those packages
import pyautogui as gui

import graphics
from graphics import *


timeDelta = 1.


class Enemy:
    # enemy - player distance will be always 1 to save on some calculations
    x = y = 0

    # side note: the number is the charging time, and the move itself is executed when that time passes
    # this is an example list, the real one will be arranged at runtime
    moveList = [('shoot', 0.5), ('dodge', 1.), ('shoot', 0.5), ('shoot', 0.5), ('rush', 1.)]
    moveIter = 0

    midAnimation = 0  # bool

    def __init__(self):
        # +-50% from the original value
        # name, duration, probability
        moves = 8  # number of generated moves
        available_moves = [('shoot', 0.5, 7), ('rush', 1.2, 3), ('dodge', 0.8, 1)]

    def find_closest_point(self, x, y):
        x_abs = x - self.x
        y_abs = y - self.y
        r = math.sqrt(x_abs ** 2 + y_abs ** 2)

        return x_abs / r + self.x, y_abs / r + self.y


    def update(self):
        print("e update")

        self.moveIter += 1


class Player:
    x = y = 0  # will be derived from rotation (and the other way around in case of dodge move)
    rotationSpeed = 3 * math.radians(1)  # in degrees

    # rotO - relative rotation, rest - global rotation (possibly irrelevant) (rotO = rotZ)
    rotO = rotX = rotY = rotZ = 0
    moveDelta = 0
    charge = 100
    health = 3

    coolDownTime = 1.  # in seconds
    coolDown = 0.  # counting down from whatever it's set to
    shootNextTime = 0

    # current coords -> new rotation info
    def update_rotation(self, e: Enemy):
        print("p rotation")

    # current rotation -> new coords info
    def update_position(self, e: Enemy):
        print("p position")

    # direction is really either negative or positive
    def move(self, e: Enemy, direction: int):
        print("p move")

    def shoot(self, e: Enemy):
        if e.midAnimation == 1:
            return

        self.coolDown = self.coolDownTime
        self.charge -= 40
        self.shootNextTime = 1

    def update(self, e: Enemy):

        if e.midAnimation == 1:
            (x, y) = e.find_closest_point(self.x, self.y)
            self.x = x
            self.y = y
            e.midAnimation = 0


# overlay and drawing, the actual player is strictly bound to the Enemy,
# the camera should move smoothly while the player shouldn't
class Camera:
    x = y = 0
    rotX = rotY = rotZ = 0
    outFocal = 33
    defaultFocal = 35
    zoomFocal = 38

    # overlay variables
    swingIter = 0  # weapon's swing sinusoid's iterator

    weaponModel = "w_rifle.png"

    def update(self, p: Player):
        print("c update")

    def apply_camera_matrix(self, win: GraphWin):
        print("c cam matrix")

    def apply_rotation_matrix(self, obj: tuple, rad: float):
        print("c rot matrix")

    def draw_overlay(self, p: Player, win: GraphWin):
        swing_x_pre_multiplier = math.pi / 3
        swing_x_post_multiplier = 1

        swing_y_pre_multiplier = math.pi
        swing_y_post_multiplier = 0.2

        swing_iter_steps = 0.1
        swing_iter_cap = math.pi * 10  # putting a big number here is a hacky way to avoid animation jumps

        movement_multiplier = 100

        swing_x_offset = math.sin(self.swingIter * swing_x_pre_multiplier) * swing_x_post_multiplier
        swing_y_offset = math.cos(self.swingIter * swing_y_pre_multiplier) * swing_y_post_multiplier

        base_pos_x = win.getWidth() / 2
        base_pos_y = win.getHeight() - 100

        img = Image(Point(base_pos_x + swing_x_offset * movement_multiplier,
                          base_pos_y + swing_y_offset * movement_multiplier),
                          "w_rifle.png")

        img.draw(win)

        self.swingIter += swing_iter_steps * p.moveDelta  # time delta already applied
        if self.swingIter > swing_iter_cap:
            self.swingIter = 0

    # draws floor tile-by-tile, draw_floor_wire will be a simpler but more crude version of this
    def draw_floor_tiles(self):
        # rotation of a single square will be calculated
        # every new square will be created using derived rotation (each vertex shifted by x/y_increment
        # squares will be drawn on a N by N grid that will be skewed at an angle
        # squares beyond the horizon or beyond any of the visible edges will not be drawn
        # fov will be fixed at 90deg, and the board will always be skewed to the left

        square_dim = 20

        x_increment = [1, 0]
        y_increment = [0, 1]

        x_iter = 0
        y_iter = 0

        color_iter = 0
        color_adjust = 1

        y_base = [0, 0]  # cached y position for ease of resetting position and moving on to a new row

        while y_iter < square_dim:

            x_base = y_base  # main iterated position

            while x_iter < square_dim:

                color_iter += 1
                x_base += x_increment
                x_iter += 1

            if color_adjust == 1:
                color_iter = 1
                color_adjust = 0
            else:
                color_iter = 0
                color_adjust = 1

            y_base += y_increment

            x_iter = 0
            y_iter += 1

    def draw_enemy(self, e: Enemy):
        print("c draw")


# create a window, grab output by
# (FPS) hiding the cursor, moving it to center of the window and registering any deviations.
# (GUI) cursor visible and movable + some GUI library
if __name__ == '__main__':

    print("\n:^O\n")

    window = GraphWin('Don\'t stop me now, kek.', 800, 600, autoflush=False)
    enemy: Enemy = Enemy()
    camera: Camera = Camera()
    player: Player = Player()

    print("\n:^)\n")

    # window closing magically fixed itself :DDD
    while window.isOpen():
        start_time = time.time()

        enemy.update()
        player.update(enemy)
        camera.update(player)

        # very slow, sufficient for now
        for item in window.items[:]:
            item.undraw()

        camera.draw_floor_tiles()
        camera.draw_enemy(enemy)
        camera.draw_overlay(player, window)

        window.update()

        timeDelta = time.time() - start_time

    print("\n:^D")
