
# standard imports
import time
import math

import pyautogui as gui

import graphics
from graphics import *


timeDelta = 1.


def rot_left(x, y):
    return -y, x


def rot_right(x, y):
    return y, -x


def dot_prod(a, b):
    # or at least i believe this is dot product, not sure lol
    return a[0] * b[0] + a[1] * b[1]


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
    rotationSpeed = 3. * math.radians(1)  # in radians

    # rotO - relative rotation, rest - global rotation (possibly irrelevant) (rotO = rotZ)
    rotO = rotX = rotY = rotZ = 0.
    moveDelta = 0
    charge = 100
    health = 3

    coolDownTime = 1.  # in seconds
    coolDown = 0.  # counting down from whatever it's set to
    shootNextTime = 0

    # current coords -> new rotation info | current coords have to be unit vector
    def update_rotation(self, e: Enemy):
        # alpha = acos ( a.b / |a||b| )
        # rotO = acos ( [0,1] . [self] / 1)
        self.rotO = math.acos(dot_prod([0, 1], [self.x, self.y]))

        print("p rotation")

    # current rotation -> new coords info
    def update_position(self, e: Enemy):
        self.x = math.cos(self.rotO)
        self.y = math.sin(self.rotO)

    # direction is really either negative or positive
    def move(self, e: Enemy, direction: str):
        # rotate the vector to enemy by 90deg, multiply that by move multiplier
        # then apply closest_point(), deviation should be marginal

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
    squareDim = 20


    def update(self, p: Player):
        # for now apply all the player's values to camera values
        print("c update")

    # obj := standard point notation used here: [x, y]
    # copy this from the js project
    def apply_camera_matrix(self, obj: list, win: GraphWin):
        # after whole drawing space has been completed, apply wikipedia's version of this for perspective
        print("c cam matrix")

    # obj := standard point notation used here: [x, y]
    def apply_rotation_matrix(self, obj: list):

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

        x_increment = [1, 0]
        y_increment = [0, 1]

        x_iter = 0
        y_iter = 0

        color_iter = 0
        color_adjust = 1

        y_base = [0, 0]  # cached y position for ease of resetting position and moving on to a new row

        while y_iter < self.squareDim:

            x_base = y_base  # main iterated position

            while x_iter < self.squareDim:

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

    # hacky version of the tile drawing, deadline's shorter than i though
    def draw_floor_wire(self, win: GraphWin):
        # draw floor wire by wire

        for rawX in range(self.squareDim):
            # this is done to draw in the middle of the field
            y_max = draw_radius = self.squareDim / 2
            y_min = -y_max

            x = rawX - draw_radius

            # these values can be swapped to achieve horizontal lines
            line = [[x, y_min], [x, y_max]]


            print(x)

    def draw_enemy(self, e: Enemy):
        # two methods, sprite or wireframe (pre-generated)
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
