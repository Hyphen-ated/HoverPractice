import pygame

#really basic proof of concept for a practice tool for lttp hovering.
#you need to press a button for 30 or less frames, then release it for only a single frame before repressing.
#the top bar shows how long you've been pressed, the bottom bar shows how long you've been released.
#the goal is to have a bunch of all-green bars in a row
pygame.init()
#pygame.display.set_icon(pygame.image.load(path))
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joy = joysticks[0]
joy.init()


surf = pygame.Surface((40, 400))
history = []
maxlen = 20
cell_height = 10
cell_width = 30
button_frame_counter = 0
down_frames = 0
red = pygame.Color("#CC1111")
green = pygame.Color("#11CC11")
drawit = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.JOYBUTTONDOWN:
            up_size = button_frame_counter * cell_height
            color = red
            if button_frame_counter <= 1:
                color = green
            pygame.draw.rect(surf, color, pygame.Rect(5, 300, cell_width, up_size))
            history.append(surf)
            if len(history) > maxlen:
                history.pop(0)
            button_frame_counter = 0                
        elif event.type == pygame.JOYBUTTONUP:
            down_frames = button_frame_counter                       
            surf = pygame.Surface((40, 400))
            color = red
            if button_frame_counter <= 30:
                color = green
            up_size = down_frames * cell_height
            pygame.draw.rect(surf, color, pygame.Rect(5, 300-up_size, cell_width, up_size))
            button_frame_counter = 0

    button_frame_counter += 1
    
    screen.fill([0,0,0])
    idx = 0
    for sface in history:
        screen.blit(sface, (idx * 40,0))
        idx += 1

    pygame.draw.line(screen, [230,230,230], [0,300], [800,300])
    pygame.display.update()
    
    clock.tick(60)
    