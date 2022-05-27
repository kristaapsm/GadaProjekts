import time
import random
import pygame

CUSTOM_PLAYBACK_EVENT = pygame.USEREVENT + 1


def queue_next_event(event_list, event_index):
    """Set a timer for the next playback event"""
    if event_index == 0:
        timer_duration = 100  # effectively immediate
    else:
        elapsed_time = event_list[event_index][1] - event_list[event_index - 1][1]
        timer_duration = round(elapsed_time * 1000)  # convert to milliseconds
    pygame.time.set_timer(CUSTOM_PLAYBACK_EVENT, timer_duration)
    print(f"{time.time()} Set timer for {timer_duration} ms")


class Block(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = pygame.Surface([size[0], size[1]])
        self.image.fill(pygame.color.Color("blueviolet"))
        self.rect = self.image.get_rect()
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]
        # initially stationary
        self.speedx = 0
        self.speedy = 0

    def update(self):
        """Move, but stay within window bounds"""
        width, height = screen.get_size()
        if not (self.size[0] // 2) < self.rect.center[0] < (width - self.size[0] // 2):
            self.speedx *= -1  # reverse direction
        self.rect.x += self.speedx

        if not (self.size[1] // 2) < self.rect.center[1] < (height - self.size[1] // 2):
            self.speedy *= -1  # reverse direction
        self.rect.y += self.speedy

    def draw(self, screen):
        # Add this draw function so we can draw individual sprites
        screen.blit(self.image, self.rect)

    def handle_event(self, event):
        # update speeds based one keypress
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.speedx -= 1
            elif event.key == pygame.K_RIGHT:
                self.speedx += 1
            elif event.key == pygame.K_UP:
                self.speedy -= 1
            elif event.key == pygame.K_DOWN:
                self.speedy += 1
            elif event.key == pygame.K_SPACE:
                self.speedx = 0
                self.speedy = 0
            else:
                pass


# initialise screen
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE | pygame.NOFRAME)
pygame.init()
sprite_list = pygame.sprite.Group()

# create a cube at a random position
cube = Block((80, 80), (random.randint(100, 700), random.randint(100, 700)))
clock = pygame.time.Clock()
# variables for recording
recording = False
playback = False
playback_index = 0
recorded_events = []

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                # handle the event
                cube.handle_event(event)
                if recording:
                    # save the event and the time
                    recorded_events.append((event, time.time()))  # event
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                recording = not recording  # toggle recording
            elif event.button == 3:  # Right click toggles playback
                playback = not playback
                if playback:
                    if recorded_events:
                        playback_index = 0  # always start playback at zero
                        queue_next_event(recorded_events, playback_index)
                    else:
                        playback = False  # can't playback no events
                else:  # disable playback timer
                    pygame.time.set_timer(CUSTOM_PLAYBACK_EVENT, 0)
        elif event.type == CUSTOM_PLAYBACK_EVENT:
            pygame.time.set_timer(CUSTOM_PLAYBACK_EVENT, 0)  # disable playback timer
            # post the next event
            pygame.event.post(recorded_events[playback_index][0])
            playback_index += 1
            if playback_index < len(recorded_events):
                queue_next_event(recorded_events, playback_index)
            else:
                playback = False
    # clear the screen
    screen.fill(pygame.Color("white"))
    # update sprites
    cube.update()
    # draw sprites
    cube.draw(screen)
    # refresh display
    pygame.display.update()
    clock.tick(60)  # limit to 60 FPS

pygame.quit()