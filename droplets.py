from pygame import display, draw, time, event
from pygame import KEYDOWN
import random


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

screen = display.set_mode([800, 600])
screen.fill([0]*3)  # RGB
white = [255, 255, 255]

'''
center = [400, 300]
radius = 50
draw.circle(screen, white, center, radius, 1)
display.flip()
# time.wait(2000)  # milliseconds
'''

circles = []

''' # creepy white circles <3
while not event.poll().type == KEYDOWN:
    circles.append(Circle([random.randint(20, 780), random.randint(20, 580)], 20))

    for c in circles:
        c.radius += 1
        draw.circle(screen, white, c.center, c.radius)
    clock = time.Clock()
    clock.tick(60)
    display.flip()
'''

while not event.poll().type == KEYDOWN:
    screen.fill([0] * 3)
    circles.append(Circle([random.randint(20, 780), random.randint(20, 580)], random.randint(20, 30)))

    for c in circles[:]:
        if c.radius > 55:
            circles.remove(c)
        else:
            c.radius += 1
            draw.circle(screen, white, c.center, c.radius, 1)
    clock = time.Clock()
    clock.tick(60)
    display.flip()

# for c in circles[:]  # slice for copy, bc. cannot delete list i am iterating
