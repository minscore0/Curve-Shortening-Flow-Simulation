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
global ds
ds = 25 # difference in arc length (used in parameterization)
dt = 20 # difference in time (used in csf calculation)


def interpolate(curve_data): # reparameterizes and interpolates the curve to with respect arc length (ds)
    x = np.array([point[0] for point in curve_data])
    y = np.array([point[1] for point in curve_data])
    arc_lengths = np.zeros(len(curve_data))

    for i in range(1, len(curve_data)):
        arc_lengths[i] = arc_lengths[i-1] + math.dist(curve_data[i-1], curve_data[i]) # stores the partial sum of arclength at each point
    normalized_arc_lengths = arc_lengths/arc_lengths[-1] # maps arc lengths to [0, 1] by dividing by the total arc length

    tck, u = splprep([x, y], u=normalized_arc_lengths, s=0) # performs spline interpolation based off of the parameter arc length
    new_t = np.linspace(0, 1, round(arc_lengths[-1]/ds))
    new_x, new_y = splev(new_t, tck)

    """
    plt.plot(x, y, 'o', label='Original points')
    plt.plot(new_x, new_y, '-', label='Interpolated curve')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Arc Length Parameterized Spline Interpolation')
    plt.show()
    """

    new_data = [[x, y] for x, y in zip(new_x, new_y)]
    return new_data


def connect_endpoints(curve_data):
    start_point = curve_data[0]
    end_point = curve_data[-1]
    dist = math.dist(start_point, end_point)
    num_points = round(dist/20)
    if num_points == 0:
        return curve_data
    x_diff = (curve_data[-1][0]-curve_data[0][0]) / num_points
    y_diff = (curve_data[-1][1]-curve_data[0][1]) / num_points
    for i in range(1, num_points):
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


def remove_repeats(input_list):
    if not input_list:
        return []

    result = [input_list[0]]  # Start with the first element
    for num in input_list[1:]:
        if math.dist(num, result[-1]) > 5:
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
        point_1 = curve_data[i - 1] if i - 1 >= 0 else curve_data[-1]
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
    return new_curve_data


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
                curve_data = interpolate(curve_data)
            drawing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_x:
                curve_data = list()
                started = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                started = True

            elif event.key == pygame.K_t: # for testing
                print("test started")

    if drawing:
        curve_data = collect_data(drawing, curve_data)
    if started:
        curve_data = csf(curve_data)
    update_display(screen, curve_data)
pygame.quit()

### IDEAS
# do interpolation before connecting to beginning?
