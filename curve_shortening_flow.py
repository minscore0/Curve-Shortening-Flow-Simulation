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
global ds, dt
ds = 5 # difference in arc length (used in parameterization)
dt = 10 # difference in time (used in csf calculation)


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


def curve_and_normal(point_1, point_2, point_3): # calculates curvature and normal vector at point_2
    # tangent vectors
    tan_1 = (point_3[0]-point_2[0], point_3[1]-point_2[1])
    tan_2 = (point_2[0]-point_1[0], point_2[1]-point_1[1])

    # lenghs of tangent vectors
    tan_1_norm = math.dist((0, 0), tan_1)
    tan_2_norm = math.dist((0, 0), tan_2)

    # unit tangent vectors
    tan_1 = (tan_1[0]/tan_1_norm, tan_1[1]/tan_1_norm)
    tan_2 = (tan_2[0]/tan_2_norm, tan_2[1]/tan_2_norm)

    normal = [tan_1[1]+tan_2[1], -(tan_1[0]+tan_2[0])]
    normal[0] /= math.dist((0, 0), normal)
    normal[1] /= math.dist((0, 0), normal)

    curvature = 2 * (tan_1[0]*tan_2[1] - tan_1[1]*tan_2[0]) / (tan_1_norm + tan_2_norm)

    return curvature, normal


def csf(curve_data): # updates curve data according to curve shortening flow

    curvatures = list()
    normals = list()

    for i in range(len(curve_data)):
        point_2 = curve_data[i]
        point_1 = curve_data[i - 1]
        point_3 = curve_data[(i + 1) % len(curve_data)]
    
        K, N = curve_and_normal(point_1, point_2, point_3)
        curvatures.append(K)
        normals.append(N)

    for i in range(len(curve_data)):
        K = curvatures[i]
        N = normals[i]
        curve_data[i][0] += dt * K * N[0]
        curve_data[i][1] += dt * K * N[1]

    # feature scaling for colorization (using min-max normalization)
    abs_curvature = [abs(x) for x in curvatures]
    scaled_curvature = [(x - min(abs_curvature))/(max(abs_curvature)-min(abs_curvature)) for x in abs_curvature]

    return interpolate(curve_data), scaled_curvature


def draw_curve(screen, curve_data, scaled_curvature): # draws the curve
    if len(curve_data) < 2:
        return
    if scaled_curvature is not None:
        for i in range(len(curve_data)):
            pygame.draw.aaline(screen, ((1/.7)*max((0, scaled_curvature[i]-0.3))*255, 0, 0), curve_data[i], curve_data[(i+1)%len(curve_data)])
    else:
        for i in range(len(curve_data)):
            pygame.draw.aaline(screen, "black", curve_data[i], curve_data[(i+1)%len(curve_data)])
    return


def draw_buttons(screen, font, button_data):
    text1 = font.render("Pause simulation", True, (0, 0, 0))
    text2 = font.render("Maintain arc length", True, (0, 0, 0))
    text1_rect = text1.get_rect()
    text1_rect.center = (125, 42)
    text2_rect = text2.get_rect()
    text2_rect.center = (135, 87)
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

    for i in range(2):
        if button_data[i] == True:
            pygame.draw.polygon(screen, (15, 191, 62), [(30, 30 + i*45), (30, 50 + i*45), (50, 50 + i*45), (50, 30 + i*45)])
            pygame.draw.polygon(screen, (64, 64, 64), [(30, 30 + i*45), (30, 50 + i*45), (50, 50 + i*45), (50, 30 + i*45)], 2)
        else:
            pygame.draw.polygon(screen, (200, 200, 200), [(30, 30 + i*45), (30, 50 + i*45), (50, 50 + i*45), (50, 30 + i*45)])
            pygame.draw.polygon(screen, (64, 64, 64), [(30, 30 + i*45), (30, 50 + i*45), (50, 50 + i*45), (50, 30 + i*45)], 2)


def update_display(screen, curve_data, button_data, font, scaled_curvature=None): # update display
    screen.fill("white")
    draw_curve(screen, curve_data, scaled_curvature)
    draw_buttons(screen, font, button_data)
    pygame.display.flip()
    return


# variables
started = False
running = True
drawing = False
curve_data = list()
scaled_curvature = None
button_data = [False, False]

font1 = pygame.font.Font("freesansbold.ttf", 16)
test = font1.render("Pause simulation", True, (255, 255, 255))

while running:
    
    clock.tick(80)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not drawing:
                if math.dist(pygame.mouse.get_pos(), (40, 40)) <= 15:
                    button_data[0] = not button_data[0]
                elif math.dist(pygame.mouse.get_pos(), (40, 85)) <= 15:
                    button_data[1] = not button_data[1]
                elif not started:
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
                scaled_curvature = None
                started = False
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                started = True

    if drawing:
        curve_data = collect_data(drawing, curve_data)
    if started and not button_data[0]:
        if len(curve_data) <= 3:
            curve_data = list()
            scaled_curvature = None
            started = False
            continue
        curve_data, scaled_curvature = csf(curve_data)
    update_display(screen, curve_data, button_data, font1, scaled_curvature)
pygame.quit()
