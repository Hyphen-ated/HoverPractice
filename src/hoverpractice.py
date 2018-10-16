import pygame, sys, os

class Dust(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.frame = 0
        self.empty = pygame.Surface((0,0))
        self.dusts = []
        for i in range(5):
            img = pygame.image.load(os.path.join("images","dust" + str(i + 1) + ".png"))
            img.convert_alpha()
            self.dusts.append(pygame.transform.scale(img, (64,64)))
        
        self.frames = []
        # these need to be reviewed frame by frame to make sure they're behaving right
        for i in range(4):
            self.frames.append(self.empty)
        for i in range(2):
            self.frames.append(self.dusts[0])
        for i in range(4):
            for j in range(3):
                self.frames.append(self.dusts[i+1])
        self.frames.append(self.empty)

    def tick(self, surface, button_history, x, y):
        if self.frame == 0:
            if button_history[0] and button_history[1]:
                self.frame = 1
                self.x = x
                self.y = y + 20
        else:
            self.frame += 1                        
                
        if self.frame >= len(self.frames):
            self.frame = 0
        
        if self.frame != 0:
            img = self.frames[self.frame]
            surface.blit(img, [self.x, self.y])
        

class Link(object):
    def __init__(self, x, y):
        self.frame = 0
        self.basex = x
        self.x = x
        self.basey = y
        self.y = y        
        self.nextStepAmount = 1
        self.dust = Dust()        
        self.walks = []
        for i in range(8):
            img = pygame.image.load(os.path.join("images","walk" + str(i + 1) + ".png"))
            img.convert_alpha()
            self.walks.append(pygame.transform.scale(img, (64,64)))            
  
        self.stand = pygame.image.load(os.path.join("images", "stand.png"))
        self.stand.convert_alpha()
        self.stand = pygame.transform.scale(self.stand, (64,64))

        self.frames = []
        # maybe this should be read from a datafile. but here is the framedata for starting a dash.
        for i in range(3):
            self.frames.append(self.stand)
        for i in range(6):
            for j in range(2):
                self.frames.append(self.walks[i])
        self.frames.append(self.walks[6])
        self.frames.append(self.walks[7])

        for i in range(4):
            for j in range(8):
                self.frames.append(self.walks[j])
            
    def reset(self):
        self.frame = 0
        self.x = self.basex
        self.y = self.basey
        self.nextStepAmount = 1
        
    def tick(self, surface, button_history, axis_history):        
        # we move on the current frame if the button started being pushed on the frame before last, and they were using axis
        if not button_history[3] and button_history[2] and axis_history[2]: 
            self.y += self.nextStepAmount * 2
            self.nextStepAmount = self.nextStepAmount % 2 + 1 # cycle between 2 and 1

        if button_history[0]:
            self.frame += 1        
        else:
            self.frame = 0
            
        img = self.frames[self.frame]
        surface.blit(img, [self.x, self.y])
        
        self.dust.tick(surface, button_history, self.x, self.y)
            
            
        


        
def main():
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
    
    bg_x, bg_y = 100,420
    link_x, link_y = 140, 390
    
    link = Link(link_x, link_y)
    
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
    red = pygame.Color("#CC1111")
    green = pygame.Color("#11CC11")
    offwhite = pygame.Color(230, 230, 230)

    background = pygame.image.load(os.path.join("images","background.png"))
    background.convert_alpha()
    background = pygame.transform.scale(background, (160,160))
    
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
                    elif event.type == pygame.KEYUP:
                        return -1, event.key
            clock.tick(60)
            
    def getCurrentButtonState(joy, buttonid):
        if joy:
            return joy.get_button(buttonid)
        else:
            return pygame.key.get_pressed()[buttonid]
                    
    joyid, buttonid = getDashButton()
    
    if joyid == -1:
        #keyboard
        joy = None
    else:
        joy = pygame.joystick.Joystick(joyid)
    
    # store a list of what the button state was on the last few frames.
    # the value at 0 is the current frame, 1 is the previous frame, etc.
    input_history_length = 4
    button_history = [0] * input_history_length
    axis_history = [0] * input_history_length

    hat_num = -1
    axis_num = -1
    
    # main frame loop
    while True:
        for event in pygame.event.get():
            if event is not None:
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.JOYHATMOTION:
                    hat_num = event.hat
                    axis_num = -1
                elif event.type == pygame.JOYAXISMOTION and abs(event.value) > 0.1:
                    axis_num = event.axis
                    hat_num = -1
                    
        color = red
        button_history.insert(0, getCurrentButtonState(joy, buttonid))
        del button_history[-1]
        
        if hat_num != -1 and joy:
            (x, val) = joy.get_hat(hat_num)            
            if abs(val) < 0.1:
                val = 0
            axis_history.insert(0, val)
        elif axis_num != -1 and joy:
            val = joy.get_axis(axis_num)
            if abs(val) < 0.1:
                val = 0
            axis_history.insert(0, val)     
        else:
            axis_history.insert(0, 0)
        del axis_history[-1]
        
        broken_streak = True
        if button_history[0]:
            if not button_history[1]:
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
            if button_history[1]:
                button_frame_counter = 1
                
            # draw the bottom bar            
            bar_height = min(button_frame_counter, max_bottom_cells) * cell_height
            if button_frame_counter <= 1:
                color = green
                broken_streak = False
            pygame.draw.rect(stripe_in_progress, color, pygame.Rect(pad_amount, midline_y, bar_width, bar_height))
    
            
        if broken_streak:
            link.reset()
            button_history = [0] * input_history_length
            axis_history = [0] * input_history_length
            if current_streak >= min_streak_length:
                last_streaks.append(current_streak)
            if len(last_streaks) > rolling_average_size:
                last_streaks.pop(0)
            current_streak = 0    
        elif button_history[0] and not button_history[1]:
            current_streak += 1
            if current_streak >= min_good_streak_length:
                last_good_streak = current_streak
            best_streak = max(current_streak, best_streak)
        
        button_frame_counter += 1
                
        
        screen.fill([0,0,0])
        idx = 0
        for sface in history:
            screen.blit(sface, (idx * stripe_width,0))
            idx += 1
        if stripe_in_progress:
            screen.blit(stripe_in_progress, (idx * stripe_width,0))
        
        pygame.draw.line(screen, offwhite, [0,midline_y], [window_w,midline_y])
        
        
        screen.blit(background, (bg_x, bg_y))
        
        link.tick(screen, button_history, axis_history)
        
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



main()