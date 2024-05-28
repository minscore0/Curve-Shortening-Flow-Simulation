import numpy as np
import pygame
from scipy.interpolate import splprep, splev

# Original points
points = [(702, 522), (697, 522), (675, 522), (634, 522), (590, 522), (547, 522), 
          (509, 519), (488, 514), (476, 507), (469, 500), (464, 491), (462, 478), 
          (461, 465), (461, 450), (461, 432), (461, 413), (464, 396), (472, 376), 
          (486, 355), (505, 331), (552, 289), (575, 274), (597, 264), (620, 258), 
          (644, 254), (669, 253), (719, 257), (746, 266), (770, 278), (791, 292), 
          (806, 304), (817, 316), (825, 328), (832, 342), (836, 360), (838, 380), 
          (837, 402), (832, 422), (820, 443), (807, 460), (793, 473), (778, 486), 
          (761, 498), (746, 506), (732, 511), (721, 514), (713, 516), (710, 516), 
          (702, 522)]

# Separate x and y coordinates
x = np.array([point[0] for point in points])
y = np.array([point[1] for point in points])

# Compute arc length
arc_lengths = np.zeros(len(points))
for i in range(1, len(points)):
    arc_lengths[i] = arc_lengths[i - 1] + np.sqrt((x[i] - x[i - 1]) ** 2 + (y[i] - y[i - 1]) ** 2)

# Normalize arc length to [0, 1]
normalized_arc_lengths = arc_lengths / arc_lengths[-1]

# Parametric interpolation using normalized arc length
tck, u = splprep([x, y], u=normalized_arc_lengths, s=0)

# Define the parameter values for interpolation
new_t = np.linspace(0, 1, 100)

# Interpolate x and y coordinates separately
new_x, new_y = splev(new_t, tck)

# Print some of the coordinates for debugging
print("Original Coordinates (x, y):")
for i in range(len(x)):
    print(f"({x[i]}, {y[i]})")

print("\nInterpolated Coordinates (x, y):")
for i in range(len(new_x)):
    print(f"({new_x[i]}, {new_y[i]})")

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1000, 800  # Adjust based on your actual plotting range
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Interpolated Curve")

# Convert coordinates to Pygame's coordinate system
# Pygame's origin (0,0) is at the top-left corner
pygame_coords = [(int(x), height - int(y)) for x, y in zip(new_x, new_y)]

# Print converted coordinates for debugging
print("\nConverted Coordinates for Pygame (x, y):")
for coord in pygame_coords:
    print(coord)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the original points (optional, for comparison)
    for x, y in points:
        pygame.draw.circle(screen, (0, 0, 255), (x, height - y), 5)  # Blue circles

    # Draw the interpolated curve
    if len(pygame_coords) > 1:
        pygame.draw.lines(screen, (255, 0, 0), False, pygame_coords, 2)  # Red line for the interpolated curve

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
