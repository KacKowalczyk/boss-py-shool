import pyautogui
import graphics

class Enemy:
    x = y = 0
    # will be randomly shuffled every run
    attackList = ['shoot', 'dodge', 'shoot', 'shoot', 'rush']
    midAnimation = 0  # bool

    def update(self):
        print("e update")


class Player:
    x = y = 0
    rotX = rotY = rotZ = 0
    charge = 100
    health = 3

    coolDownTime = 1.
    coolDown = 0.

    def update(self, e: Enemy):
        print("p update")



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

    def update(self, p: Player):
        print("c update")

    def draw_overlay(self, p: Player):
        print("c overlay")

    def draw_floor(self):
        print("c floor")

    def draw_enemy(self, e: Enemy):
        print("c draw")


# create a window, grab output by
# (FPS) hiding the cursor, moving it to center of the window and registering any deviations.
# (GUI) cursor visible and movable + some GUI library
if __name__ == '__main__':

    print(":^/")

    enemy: Enemy = Enemy()
    camera: Camera = Camera()
    player: Player = Player()

    print(":^O")

    enemy.update()
    player.update(enemy)
    camera.update(player)

    print(":^)")

    camera.draw_floor()
    camera.draw_enemy(enemy)
    camera.draw_overlay(player)

    print(":^D")
