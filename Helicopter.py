import random
import pygame
pygame.init()  # Initializes every functionality that has to do with pygame

# SETS UP THE CANVAS
HEIGHT, WIDTH = 600, 1000
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Helicopter Game")
ICON = pygame.image.load('ICON.png')
pygame.display.set_icon(ICON)
font = pygame.font.Font(None, 20)
TIMER = pygame.time.Clock()
playerX = 100
playerY = 300
flying = False    
gravity = 3.8 # This si because it is a suitable value 
y_speed = 0
score = 0
highscore = 0
map_speed = 10
active = True
heli = pygame.transform.scale(pygame.image.load('helicopter.png'), (60, 60))

#-----------------------------------------------GENERATING A NEW MAP------------------------------------------------------
rect_width = 10
total_rects = WIDTH // rect_width
spacer = 10
map_rects = []

# This function is responsible for the logic of drawing rectangles
def generate_new():
    rects = []
    top_height = random.randint(0, 300)  # a 300 pixel gap between the top rectangle and bottom rectangle
    for i in range(total_rects):
        top_height = random.randint(top_height - spacer, top_height + spacer)  # make the path look curved and continuous
        if top_height < 0:
            top_height = 0
        elif top_height > 300:
            top_height = 300  # These conditions prevent rectangles going off SCREEN

        # Define top and bottom rectangles
        top_rect = pygame.Rect(i * rect_width, 0, rect_width, top_height)
        bottom_rect = pygame.Rect(i * rect_width, top_height + 300, rect_width, HEIGHT - top_height - 300)

        # Append rectangles to the list
        rects.append(top_rect)
        rects.append(bottom_rect)
    
    return rects

# This function is to actually draw the rectangles on the board
def draw_map(rects):
    for rect in rects:
        pygame.draw.rect(SCREEN, 'green', rect)
    pygame.draw.rect(SCREEN, "dark green", [0, 0, WIDTH, HEIGHT], 12)  # This makes a border on the SCREEN

def move_rects(rects):
    global score
    for i in range(len(rects)):
        rects[i] = (rects[i][0] - map_speed, rects[i][1], rect_width, rects[i][3])
        if rects[i][0] + rect_width < 0:
            rects.pop(1)
            rects.pop(0)
            top_height = random.randint(rects[-2][3] - spacer, rects[-2][3] + spacer)
            if top_height < 0:
                top_height = 0
            elif top_height > 300:
                top_height = 300
            rects.append((rects[-2][0] + rect_width, 0, rect_width, top_height))
            rects.append((rects[-2][0] + rect_width, top_height + 300, rect_width, HEIGHT))
            score += 1
    return rects

#------------------------------------------------PLAYER LOGIC-------------------------------------------------------
def draw_player():
    # draw player hit box as circle, and player helicopter image
    player = pygame.draw.circle(SCREEN, 'black', (playerX, playerY), 20)
    SCREEN.blit(heli, (playerX - 40, playerY - 30))
    return player


def move_player(y_pos, speed, fly):
    if fly:
        speed += gravity
    else:
        speed -=gravity
    y_pos -= speed
    return y_pos, speed

def check_collision(rects, circle, act):
    global playerY
    for rect in rects:
        # Convert tuple to pygame.Rect
        rect_obj = pygame.Rect(rect)
        if circle.colliderect(rect_obj):
            act = False
            if rect_obj.top == 0:  # Hit the top rectangle
                playerY = rect_obj.height + 30
            elif rect_obj.bottom == HEIGHT:  # Hit the bottom rectangle
                playerY = rect_obj.bottom - 30
    return act



#--------------------------------------------GAME LOOP--------------------------------------------------
FPS = 60
RUN = True
while RUN:
    SCREEN.fill('black')
    TIMER.tick(FPS)

    # Generate or move map and update player position if needed
    if not map_rects:
        map_rects = generate_new()  # Generate map initially or if it's empty

    draw_map(map_rects)
    player_circle = draw_player()
    if active:
        playerY, Y_speed = move_player(playerY, y_speed, flying)
        map_rects = move_rects(map_rects)
    active = check_collision(map_rects, player_circle, active)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flying  = True
            if event.key == pygame.K_RETURN:
                if not active:
                    new_map = True
                    active = True
                    y_speed = 0
                    map_speed = 10
                    if score > highscore:
                        high_score = score
                    score = 0
                    playerY = 300 # reset to initial value
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                flying = False

    map_speed = 2 + score//50
    spacer = 10 + score//100

    SCREEN.blit(font.render(f'Score: {score}', True, 'red'), (20, 15))
    SCREEN.blit(font.render(f'High Score: {highscore}', True, 'red'), (20, 565))
    if not active:
        SCREEN.blit(font.render('Press Enter to Restart', True, 'red'), (300, 15))
        SCREEN.blit(font.render('Press Enter to Restart', True, 'red'), (300, 565))

    pygame.display.flip()

pygame.quit()
