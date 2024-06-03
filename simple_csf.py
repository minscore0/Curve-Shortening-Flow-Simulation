import pygame
from scipy.interpolate import splprep, splev
import numpy as np
import math
import matplotlib.pyplot as plt
from data_points import data_points

# pygame setup
pygame.init()
pygame.display.set_caption("Curve Shortening Flow Simulation")
screen = pygame.display.set_mode((1500, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()
screen.fill("white")

# global constants
global ds, dt
ds = 10 # difference in arc length (used in parameterization)
dt = 20 # difference in time (used in csf calculation)


def draw_curve(screen, curve_data): # draws the curve
    if len(curve_data) < 2:
        return
    for point in range(len(curve_data)-1):
        pygame.draw.aaline(screen, "black", curve_data[point], curve_data[point+1])
    pygame.draw.aaline(screen, "black", curve_data[0], curve_data[-1])
    return


def remove_repeats(input_list):
    if not input_list:
        return []

    result = [input_list[0]]  # Start with the first element
    for num in input_list[1:]:
        if math.dist(num, result[-1]) > ds:
        #if (round(num[0]), round(num[1])) != (round(result[-1][0]), round(result[-1][1])):  # Only add if it's different from the last added
            result.append(num)
    
    return result


def curve_and_normal(point_1, point_2, point_3): # calculates curvature and normal vector at point_2
    dx = abs(point_3[0] - point_2[0])
    ddx = abs(dx - (point_2[0] - point_1[0]))
    dy = abs(point_3[1] - point_2[1])
    ddy = abs(dx - (point_2[1] - point_1[1]))

    if (dx**2 + dy**2) == 0:
        return 0, (0, 0)

    K = (dx*ddy - dy*ddx)/((dx**2 + dy**2)**(3/2))
    """
    T = (dx/math.sqrt(dx**2 + dy**2), dy/math.sqrt(dx**2 + dy**2))
    N = (T[0]/math.sqrt(T[0]**2+T[1]**2), T[1]/math.sqrt(T[0]**2+T[1]**2))
    """
    N = (-1*dy/math.sqrt(dx**2+dy**2), dx/math.sqrt(dx**2+dy**2))

    return K, N


def csf(curve_data): # updates curve data according to curve shortening flow

    KN_pairs = list()
    new_curve_data = list()

    for i in range(len(curve_data)):

        point_2 = curve_data[i]
        point_1 = curve_data[i - 1]
        point_3 = curve_data[(i + 1) % len(curve_data)]
    
        K, N = curve_and_normal(point_1, point_2, point_3)
        KN_pairs.append((K, N))

    for i in range(len(curve_data)):
        point_2 = curve_data[i]
        K, N = KN_pairs[i]
        x = point_2[0] + 1*dt*K*N[0]
        y = point_2[1] + 1*dt*K*N[1]
        new_curve_data.append([x, y])
        print(new_curve_data)
        print(curve_data)

    #return interpolate(remove_repeats(new_curve_data))
    return remove_repeats(new_curve_data)


def update_display(screen, curve_data): # update display
    screen.fill("white")
    draw_curve(screen, curve_data)
    pygame.display.flip()
    return


# variables
started = False
running = True
drawing = False
curve_data = data_points

while running:
    
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: # quit program
                running = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                started = True

            elif event.key == pygame.K_t: # for testing
                print("test started")

    if started:
        curve_data = csf(curve_data)
    update_display(screen, curve_data)
pygame.quit()

### IDEAS
