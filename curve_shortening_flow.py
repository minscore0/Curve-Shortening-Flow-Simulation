import pygame
from scipy.interpolate import splprep, splev
import numpy as np
import math
import matplotlib.pyplot as plt

# pygame setup
pygame.init()
pygame.display.set_caption("Curve Shortening Flow Simulation")
screen = pygame.display.set_mode((1500, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()
screen.fill("white")

# global constants
global dr, ds
ds = 3 # difference in arc length


def prepare_data(curve_data): # reparameterizes and interpolates the curve to with respect arc length (ds)
    x = np.array([point[0] for point in curve_data])
    y = np.array([point[1] for point in curve_data])
    arc_lengths = np.zeros(len(curve_data))

    for i in range(1, len(curve_data)):
        arc_lengths[i] = arc_lengths[i-1] + math.dist(curve_data[i-1], curve_data[i]) # stores the partial sum of arclength at each point
    normalized_arc_lengths = arc_lengths/arc_lengths[-1] # maps arc lengths to [0, 1] by dividing by the total arc length

    tck, u = splprep([x, y], u=normalized_arc_lengths, s=0) # performs spline interpolation based off of the parameter arc length
    new_t = np.linspace(0, 1, round(arc_lengths[-1]/ds))
    new_x, new_y = splev(new_t, tck)

    plt.plot(x, y, 'o', label='Original points')
    plt.plot(new_x, new_y, '-', label='Interpolated curve')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Arc Length Parameterized Spline Interpolation')
    plt.show()

    new_data = [(round(x), round(y)) for x, y in zip(new_x, new_y)]
    return new_data


def connect_endpoints(curve_data):
    start_point = curve_data[0]
    end_point = curve_data[-1]
    dist = math.dist(start_point, end_point)
    num_points = round(dist/20)
    x_diff = (curve_data[-1][0]-curve_data[0][0]) / num_points
    y_diff = (curve_data[-1][1]-curve_data[0][1]) / num_points
    for i in range(1, num_points+1):
        curve_data.append((end_point[0]-((i)*x_diff), end_point[1]-((i)*y_diff)))
    return curve_data


def collect_data(drawing, curve_data): # extends curve to current mouse position
    if drawing:
        position = pygame.mouse.get_pos()
        if len(curve_data) >= 1 and position == curve_data[-1]:
            return curve_data
        curve_data.append(position)
    return curve_data


def draw_curve(screen, curve_data): # draws the curve
    if len(curve_data) < 2:
        return
    for point in range(len(curve_data)-1):
        pygame.draw.aaline(screen, "black", curve_data[point], curve_data[point+1])
    pygame.draw.aaline(screen, "black", curve_data[0], curve_data[-1])
    return


def csf(curve_data): # updates curve data according to curve shortening flow
    pass


def update_display(screen, curve_data): # update display
    screen.fill("white")
    draw_curve(screen, curve_data)
    pygame.display.flip()
    return


# variables
started = False
running = True
drawing = False
curve_data = list()

while running:
    
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not started:
            drawing = True
        
        elif event.type == pygame.MOUSEBUTTONUP and not started:
            print("called")
            if drawing:
                curve_data = connect_endpoints(curve_data)
                curve_data = prepare_data(curve_data)
            drawing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_x:
                curve_data = list()
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                pass

            elif event.key == pygame.K_t: # for testing
                print("test started")

    if drawing:
        curve_data = collect_data(drawing, curve_data)
    update_display(screen, curve_data)
pygame.quit()

### TO DO
# fix weird interpolation in gaps of data
    # try some linear interpolation between last and first point before calling the prepare_data function
# implement csf
