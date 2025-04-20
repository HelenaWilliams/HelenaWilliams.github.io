import pygame
import time
import random
import asyncio

pygame.init()
clock = pygame.time.Clock()
fps = 100

screen_width = 600
screen_height = 400
bg_color = (0, 150, 150)
screen = pygame.display.set_mode((screen_width, screen_height))

player_pos = 270
ai_pos = 270
ball_x = 300
ball_y = 200

speed = 1
multiplier = 1
mult_x = 1
mult_y = 1
player_up = False
player_down = False
just_scored = False

p_debounce = time.time()
ai_debounce = time.time()

def draw_paddles():
    ai_paddle = pygame.Rect(30, ai_pos, 10, 60) #left, top, width, height
    pygame.draw.rect(screen, (255, 100, 0), ai_paddle)
    player_paddle = pygame.Rect(560, player_pos, 10, 60) #left, top, width, height
    pygame.draw.rect(screen, (255, 100, 0), player_paddle)

def draw_ball():
    global just_scored
    pygame.draw.circle(screen, (255, 255, 255), (ball_x, ball_y), 15)
    if just_scored:
       just_scored = False
       pygame.time.wait(1000)

def easy_mode():
    global ai_pos, multiplier
    ai_pos += (speed * multiplier)
    if ai_pos > 340:
        multiplier = -1
    if ai_pos < 0:
        multiplier = 1

def medium_mode():
    global ai_pos, ball_y
    if abs(ai_pos - ball_y) > 10:
        if ai_pos+30 > ball_y and ai_pos > 0:
            ai_pos -= speed
        if ai_pos+30 < ball_y and ai_pos < 340:
            ai_pos += speed
    
def event_catcher():
    global player_pos, player_up, player_down
    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            player_down = True
        else:
            player_down = False
        if pygame.key.get_pressed()[pygame.K_UP]:
            player_up = True
        else:
            player_up = False
        #print(player_up, player_down)

def player_move():
    global player_up, player_down, player_pos
    #print(player_pos)
    if player_up == True and player_pos > 0:
        player_pos -= speed+0.5
    elif player_down == True and player_pos < 340:
        player_pos += speed+0.5

def ball_move():
    global ball_x, ball_y, mult_x, mult_y, player_pos, just_scored, p_debounce, ai_debounce
    ball_x += (speed) * mult_x
    ball_y += (speed) * mult_y

    # Top and bottom ricochet
    if ball_y < 15 or ball_y > 385:
        mult_y *= -1

    spd_inc = -1.1
    # Player ricochets
    if time.time() - p_debounce > 1:
        if (ball_x > 545 and ball_x < 550) and (ball_y > player_pos-15 and ball_y < player_pos+60):
            print("A")
            mult_x *= spd_inc
            p_debounce = time.time()
        elif (ball_x > 545 and ball_x < 575) and (ball_y > player_pos and ball_y < player_pos+15):
            print("B")
            mult_x *= spd_inc
            mult_y *= spd_inc
            p_debounce = time.time()
        elif (ball_x > 545 and ball_x < 560) and (ball_y > player_pos + 45 and ball_y < player_pos+60):
            print("C")
            mult_x *= spd_inc
            mult_y *= spd_inc
            p_debounce = time.time()

        # AI ricochet
        if time.time() - ai_debounce > 1:
            if (ball_x < 50 and ball_x > 30) and (ball_y > ai_pos and ball_y < ai_pos+60):
                mult_x *= spd_inc
                ai_debounce = time.time()
            elif (ball_x < 45 and ball_x > 35) and (ball_y > ai_pos and ball_y < ai_pos+15):
                mult_x *= spd_inc
                mult_y *= spd_inc
                ai_debounce = time.time()
            elif (ball_x < 40 and ball_x > 30) and (ball_y > ai_pos + 45 and ball_y < ai_pos + 60):
                mult_x *= spd_inc
                mult_y *= spd_inc
                ai_debounce = time.time()

def score():
    global ball_x, ball_y, just_scored, mult_x, mult_y, player_pos, ai_pos
    if ball_x > 600 or ball_x < 0:
        ball_x = 300
        ball_y = 200
        player_pos = 270
        ai_pos = 270
        mult_x = 1.5 - random.random()
        mult_y = 1.5 - random.random()
        # randomize ball start
        if random.randint(0, 1) == 0:
            mult_x *= -1
        if random.randint(0, 1) == 0:
            mult_y *= -1
        just_scored = True

async def main():
    while True:
        screen.fill(bg_color)
        half_court = pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(295, 0, 10, 400))
        draw_paddles()
        draw_ball()
        #easy_mode()
        medium_mode()
        score()
        event_catcher()
        player_move()
        ball_move()
        clock.tick(fps)
        pygame.display.flip()
        await asyncio.sleep(0)

asyncio.run(main())
