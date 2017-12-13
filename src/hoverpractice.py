import pygame, sys

# really basic proof of concept for a practice tool for lttp hovering.
# you need to press a button for 30 or less frames, then release it for only a single frame before repressing.
# the top bar shows how long you've been pressed, the bottom bar shows how long you've been released.
# the goal is to have a bunch of all-green bars in a row
pygame.display.init()

pygame.display.set_icon(pygame.image.load("boots.png"))
pygame.display.set_caption("Hover Practice")
window_w = 800
window_h = 600
screen = pygame.display.set_mode((window_w, window_h))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont('Arial', 30)

# any button on any joystick can be used
pygame.joystick.init()
for i in range(pygame.joystick.get_count()):
    pygame.joystick.Joystick(i).init()

# a "stripe" contains a "bar" made of "cells". the stripe also has padding around the outside
stripe_width = 40
stripe_height = 400
bar_width = 30
pad_amount = (stripe_width - bar_width) / 2
cell_height = 10
midline_y = window_h / 2

max_top_cells = 30
max_bottom_cells = 10

stripe_in_progress = pygame.Surface((stripe_width, stripe_height))

# we keep a history of the last N button presses to display
history = []
max_history_len = window_w // stripe_width - 1 # one extra for the stripe in progress

min_streak_length = 4 #Number of greens to be considered a streak
min_good_streak_length = 10 #Number of greens to be considered a 'good' streak
rolling_average_size = 50 #How many streaks to average

button_frame_counter = 0
current_streak = 0
last_streaks = []
last_good_streak = 0
best_streak = 0
hold_duration_check_passed = False
red = pygame.Color("#CC1111")
green = pygame.Color("#11CC11")
offwhite = pygame.Color(230, 230, 230)

# first we get what their dash button is, then we poll at 60hz for the status of that specific button.
press_button = font.render("Press your dash button", True, offwhite)
sx,sy = press_button.get_size()
screen.blit(press_button, [window_w/2 - sx/2,window_h/2 - sy/2])
pygame.display.update()

def getDashButton():    
    while True:
        for event in pygame.event.get():                   
            if event is not None:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.JOYBUTTONUP:
                    return event.joy,event.button
        clock.tick(60)
                
joyid, buttonid = getDashButton()

joy = pygame.joystick.Joystick(joyid)
last_button_pressed = 0

# main frame loop
while True:
    for event in pygame.event.get():
        if event is not None:
            if event.type == pygame.QUIT:
                sys.exit()
                
    color = red
    button_pressed = joy.get_button(buttonid)
    broken_streak = True
    if button_pressed:
        if not last_button_pressed:
            button_frame_counter = 1
            history.append(stripe_in_progress)
            # when a stripe scrolls off the left side of the screen, get rid of it
            if len(history) > max_history_len:
                history.pop(0)                
            stripe_in_progress = pygame.Surface((stripe_width, stripe_height))
            
        # button is currently held down, so draw the top bar
        bar_height = min(button_frame_counter, max_top_cells) * cell_height
        if button_frame_counter <= max_top_cells:
            color = green
            broken_streak = False
                
        pygame.draw.rect(stripe_in_progress, color, pygame.Rect(pad_amount, midline_y - bar_height, bar_width, bar_height))    
    else: # button currently not pressed        
        if last_button_pressed:
            button_frame_counter = 1
            
        # draw the bottom bar            
        bar_height = min(button_frame_counter, max_bottom_cells) * cell_height
        if button_frame_counter <= 1:
            color = green
            broken_streak = False
        pygame.draw.rect(stripe_in_progress, color, pygame.Rect(pad_amount, midline_y, bar_width, bar_height))

        
    if broken_streak:
        if current_streak >= min_streak_length:
            last_streaks.append(current_streak)
        if len(last_streaks) > rolling_average_size:
            last_streaks.pop(0)
        current_streak = 0    
    elif button_pressed and not last_button_pressed:
        current_streak += 1
        if current_streak >= min_good_streak_length:
            last_good_streak = current_streak
        best_streak = max(current_streak, best_streak)
    
    last_button_pressed = button_pressed
    button_frame_counter += 1
            
    
    screen.fill([0,0,0])
    idx = 0
    for sface in history:
        screen.blit(sface, (idx * stripe_width,0))
        idx += 1
    if stripe_in_progress:
        screen.blit(stripe_in_progress, (idx * stripe_width,0))
    
    pygame.draw.line(screen, offwhite, [0,midline_y], [window_w,midline_y])
    
    y = stripe_height + 20
    streak_text = font.render("Streak: " + str(current_streak), True, offwhite)
    screen.blit(streak_text, [window_w/2,y])
    y += font.get_height();

    streak_text = font.render("Best: " + str(best_streak) + " -- Last good: " + str(last_good_streak), True, offwhite)
    screen.blit(streak_text, [window_w/2,y])
    y += font.get_height();

    # disabling this for now because what it's doing doesn't actually make any sense. todo do something with an axis where the user "locks in" an attempt
    # if last_streaks:
    #     streak_text = font.render("Avg of last " + str(rolling_average_size) + ": " + '{0:.1f}'.format(sum(last_streaks)/float(len(last_streaks))), True, offwhite)
    #     screen.blit(streak_text, [window_w/2,y])
    #     y += font.get_height();


    pygame.display.update()    
    clock.tick(60)

