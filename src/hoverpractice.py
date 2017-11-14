import pygame, sys

# really basic proof of concept for a practice tool for lttp hovering.
# you need to press a button for 30 or less frames, then release it for only a single frame before repressing.
# the top bar shows how long you've been pressed, the bottom bar shows how long you've been released.
# the goal is to have a bunch of all-green bars in a row
pygame.init()
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

stripe_in_progress = pygame.Surface((stripe_width, stripe_height))

# we keep a history of the last N button presses to display
history = []
max_history_len = window_w // stripe_width

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
# frame loop
while True:
    color = red
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            # they've just pressed a button. now we draw a bar onto the stripe showing how long the button was released.
            # then we put the stripe into the history, which will get it drawn onscreen.
            bar_height = button_frame_counter * cell_height
            broken_streak = False
            if button_frame_counter <= 1:
                color = green
                if hold_duration_check_passed:
                    current_streak += 1
                    if current_streak >= min_good_streak_length:
                        last_good_streak = current_streak
                    best_streak = max(current_streak, best_streak)
                else:
                    broken_streak = True
            else:
                broken_streak = True

            if broken_streak:
                if current_streak >= min_streak_length:
                    last_streaks.append(current_streak)
                if len(last_streaks) > rolling_average_size:
                    last_streaks.pop(0)
                current_streak = 0

            pygame.draw.rect(stripe_in_progress, color, pygame.Rect(pad_amount, midline_y, bar_width, bar_height))
            history.append(stripe_in_progress)
            # when a stripe scrolls off the left side of the screen, get rid of it
            if len(history) > max_history_len:
                history.pop(0)
            button_frame_counter = 0               
        elif event.type == pygame.JOYBUTTONUP:
            # they just released a button. now we're going to make a new stripe and draw a bar onto it showing how long
            bar_height = button_frame_counter * cell_height
            hold_duration_check_passed = False
            if button_frame_counter <= 30:
                color = green
                hold_duration_check_passed = True
            stripe_in_progress = pygame.Surface((stripe_width, stripe_height))
            pygame.draw.rect(stripe_in_progress, color, pygame.Rect(pad_amount, midline_y - bar_height, bar_width, bar_height))
            button_frame_counter = 0

    button_frame_counter += 1
    
    screen.fill([0,0,0])
    idx = 0
    for sface in history:
        screen.blit(sface, (idx * stripe_width,0))
        idx += 1

    pygame.draw.line(screen, offwhite, [0,midline_y], [window_w,midline_y])
    
    y = stripe_height + 20
    streak_text = font.render("Streak: " + str(current_streak), True, offwhite)
    screen.blit(streak_text, [window_w/2,y])
    y += font.get_height();

    streak_text = font.render("Best: " + str(best_streak) + " -- Last: " + str(last_good_streak), True, offwhite)
    screen.blit(streak_text, [window_w/2,y])
    y += font.get_height();

    if last_streaks:
        streak_text = font.render("Avg of last " + str(rolling_average_size) + ": " + '{0:.1f}'.format(sum(last_streaks)/float(len(last_streaks))), True, offwhite)
        screen.blit(streak_text, [window_w/2,y])
        y += font.get_height();


    pygame.display.update()    
    clock.tick(60)

