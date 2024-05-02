import math
import pygame
from pygame.locals import *
import time
import random

# Initialize pygame
pygame.init()
path_width = 1
count = 0
# Set up the display
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Pendulum")

# Colors
BACKGROUND_COLOR = (255, 255, 255)
PENDULUM_COLOR = (0, 0, 0)
PATH_COLOR = (0,0,0)

# Pendulum parameters
L1 = 200  # Length of the first pendulum
L2 = 200 # Length of the second pendulum
M1 = 40 # Mass of the first pendulum
M2 = 40   # Mass of the second pendulum
G = -9.8  # Acceleration due to gravity

# Initial angles and angular velocities
theta1 = math.pi / 2 - math.radians(89)
theta2 = math.pi / 2 - math.radians(89)
theta1_vel = 0
theta2_vel = 0

# Time step and clock setup
dt = 0.01
clock = pygame.time.Clock()

# Path coordinates
path = []

# Simulation loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Change colors on spacebar press
                BACKGROUND_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                a, b, c = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                PENDULUM_COLOR = (a, b, c)
                PATH_COLOR = (a, b, c)

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Calculate the positions of the pendulum
    x1 = L1 * math.sin(theta1)
    y1 = L1 * math.cos(theta1)
    x2 = x1 + L2 * math.sin(theta2)
    y2 = y1 + L2 * math.cos(theta2)

    # Calculate the center point of the pendulum
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Draw the pendulum
    pygame.draw.line(screen, PENDULUM_COLOR, (center_x, center_y), (center_x + int(x1), center_y - int(y1)), 2)
    pygame.draw.line(screen, PENDULUM_COLOR, (center_x + int(x1), center_y - int(y1)), (center_x + int(x2), center_y - int(y2)), 2)
    pygame.draw.circle(screen, PENDULUM_COLOR, (center_x + int(x1), center_y - int(y1)), M1 // 2)
    pygame.draw.circle(screen, PENDULUM_COLOR, (center_x + int(x2), center_y - int(y2)), M2 // 2)

    # Add the current position of the second pendulum to the path list
    path.append((center_x + int(x2), center_y - int(y2)))

    # Draw the path of the second pendulum's end
    if len(path) >= 2:
        pygame.draw.lines(screen, PATH_COLOR, False, path, path_width)

    # Update the angles and angular velocities
    theta1_acc = (-G * (2 * M1 + M2) * math.sin(theta1) - M2 * G * math.sin(theta1 - 2 * theta2) -
                  2 * math.sin(theta1 - theta2) * M2 * (theta2_vel ** 2 * L2 + theta1_vel ** 2 * L1 * math.cos(theta1 - theta2))) / \
                 (L1 * (2 * M1 + M2 - M2 * math.cos(2 * theta1 - 2 * theta2)))
    theta2_acc = (2 * math.sin(theta1 - theta2) * (theta1_vel ** 2 * L1 * (M1 + M2) + G * (M1 + M2) * math.cos(theta1) +
                  theta2_vel ** 2 * L2 * M2 * math.cos(theta1 - theta2))) / \
                 (L2 * (2 * M1 + M2 - M2 * math.cos(2 * theta1 - 2 * theta2)))
    theta1_vel += theta1_acc * dt
    theta2_vel += theta2_acc * dt
    theta1 += theta1_vel * dt
    theta2 += theta2_vel * dt

    # Update the display
    pygame.display.flip()
    clock.tick(1000000)