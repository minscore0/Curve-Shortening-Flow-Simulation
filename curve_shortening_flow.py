import pygame

# pygame setup
pygame.init()
pygame.display.set_caption("Curve Shortening Flow Simulation")
screen = pygame.display.set_mode((1500, 900), pygame.RESIZABLE)
clock = pygame.time.Clock()
screen.fill("white")

# constants

def collect_data(drawing, curve_data):
    if drawing:
        curve_data.append(pygame.mouse.get_pos())
    return curve_data


def draw_curve(screen, curve_data):
    if len(curve_data) == 0:
        return
    for point in range(len(curve_data)-1):
        pygame.draw.aaline(screen, "black", curve_data[point], curve_data[point+1])
    pygame.draw.aaline(screen, "black", curve_data[0], curve_data[-1])
    return

def update_display(screen, curve_data):
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
            drawing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q: # quit program
                running = False

            elif event.key == pygame.K_DELETE or event.key == pygame.K_x:
                print("pressed x")
                curve_data = []
            
            elif (event.key == pygame.K_RETURN or event.key == pygame.K_s) and not started: # start simulation
                pass

            elif event.key == pygame.K_t: # for testing
                print("test started")

    curve_data = collect_data(drawing, curve_data)
    update_display(screen, curve_data)
pygame.quit()
