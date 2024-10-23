import pygame as py
import sys
import math
import random

py.init()

WIDTH = 1080
HEIGHT = 720

WIN = py.display.set_mode((WIDTH, HEIGHT))

py.display.set_caption("Pong")
py.display.set_icon(py.image.load("Assets\paddle.png"))

clock = py.time.Clock()

run = True

game = False 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

score_font = py.font.Font("Assets\Press_Start_2P.ttf" , 75)
title_font = py.font.Font("Assets\Press_Start_2P.ttf" , 200)
button_font = py.font.Font("Assets\Press_Start_2P.ttf" , 30)
credits_font = py.font.Font("Assets\Press_Start_2P.ttf" , 20)

ai_player = True

endless = 0

sound = True

class Paddle:

    def __init__(self,side):
        if side == "left":
            self.rect = py.rect.Rect(20, 285, 25, 150)
        elif side == "right":
            self.rect = py.rect.Rect(WIDTH - 70, 285, 25, 150)
        self.side = side
    
    def update(self):
        keys = py.key.get_pressed()
        if self.side == "left":
            if keys[py.K_w]:
                if self.rect.top > 0:
                    self.rect.y -= 5
                else:
                    self.rect.top = 0
            if keys[py.K_s]:
                if self.rect.bottom < HEIGHT:
                    self.rect.y += 5
                else:
                    self.rect.bottom = HEIGHT
        
        elif self.side == "right" and not ai_player:
            if keys[py.K_UP]:
                if self.rect.top >= 0:
                    self.rect.y -= 5
                else:
                    self.rect.top = 0
            if keys[py.K_DOWN]:
                if self.rect.bottom <= HEIGHT:
                    self.rect.y += 5
                else:
                    self.rect.bottom = HEIGHT
        else:
            if self.rect.top >= 0 and self.rect.bottom <= HEIGHT:
                if ball.rect.centery > self.rect.centery:
                    self.rect.centery += 5
                elif ball.rect.centery < self.rect.centery:
                    self.rect.centery -= 5
            if self.rect.top < 0:
                    self.rect.top = 0
            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT
            

class PongBall:

    def __init__(self):
        self.rect = py.rect.Rect(250,335,25,25)
        self.deg = (180-random.randrange(120,240))
    
    def respawn(self,side):
        if side == "left":
            self.rect.x = 250
            self.rect.y = left_paddle.rect.centery
            self.deg = (180-random.randrange(120,240))
        if side == "right":
            self.rect.x = WIDTH - 250
            self.rect.y = right_paddle.rect.centery
            self.deg = random.randrange(120,240)

    def update(self):
        
        self.update_bounce()
        self.update_score()
        self.update_move()
    
    def update_move(self):
        self.rect.x += 15 * math.cos(math.radians(self.deg))
        self.rect.y -= 15 * math.sin(math.radians(self.deg))
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def update_bounce(self):
        if self.rect.top == 0 or self.rect.bottom == HEIGHT:
            self.deg = -self.deg + 1
        elif self.rect.colliderect(left_paddle.rect):
            self.deg = 180 - self.deg
            self.rect.left = left_paddle.rect.right + 1
        elif self.rect.colliderect(right_paddle.rect):
            self.deg = 180 - self.deg
            self.rect.right = right_paddle.rect.left - 1
    
    def update_score(self):
        
        if self.rect.right <= 0:
            player2_score.score += 1
            self.respawn("left")
        elif self.rect.left >= 1080:
            player1_score.score += 1
            self.respawn("right")

class Score:
    def __init__(self,side):
        self.score = 0
        self.side = side
    
    def update(self):
        self.text = score_font.render(str(self.score), True, WHITE)
        if self.side == "left":
            self.rect = self.text.get_rect(topright = (500, 20))
        elif self.side == "right":
            self.rect = self.text.get_rect(topleft = (560, 20))

class Button:
    def __init__(self, x, y, pad, text, rect_color, text_color, func, arg):
        self.func = func
        self.arg = arg
        self.rect_color = rect_color
        self.text_color = text_color
        self.text = button_font.render(text, True, self.text_color)
        self.rect = self.text.get_rect(center = (x,y))
        self.box = py.rect.Rect(self.rect.x - pad/2, self.rect.y - pad/2, self.rect.width + pad, self.rect.height + pad)
    
    def render(self):
        py.draw.rect(WIN, self.rect_color, self.box)
        WIN.blit(self.text, self.rect)
    
    def click(self):
        button = py.mouse.get_pressed()
        if button[0]:
            if self.box.collidepoint(py.mouse.get_pos()):
                self.func(self.arg)

def start_game(ai):
    global ai_player, game
    if ai:
        ai_player = True
    else:
        ai_player = False
    game = True
        
    

        

left_paddle = Paddle("left")
right_paddle = Paddle("right")
ball = PongBall()
player1_score = Score("left")
player2_score = Score("right")


title_text = title_font.render("Pong", True, WHITE)
title_rect = title_text.get_rect(midtop = (540, 20))
player1_button = Button(WIDTH/2 -200 , HEIGHT/2, 10, "1 Player", WHITE, BLACK, start_game, True)
player2_button = Button(WIDTH/2 + 200 , HEIGHT/2, 10, "2 Players", WHITE, BLACK, start_game, False)
credits_text = credits_font.render("Created By: LouieLewis, Adapted from Atari, Inc.", True, WHITE)
credits_rect = credits_text.get_rect(midtop = (540, 500))

def update():
    WIN.fill(BLACK)

    if not game:
        WIN.blit(title_text,title_rect)
        player1_button.render()
        player2_button.render()
        WIN.blit(credits_text, credits_rect)

        player1_button.click()
        player2_button.click()


    if game:
        for i in range(15, 720, 55):
            center_rect = py.rect.Rect(510,i,30,30)
            py.draw.rect(WIN, WHITE, center_rect)

        left_paddle.update()
        right_paddle.update()
        ball.update()
        player1_score.update()
        player2_score.update()
    


        py.draw.rect(WIN, WHITE, left_paddle.rect)
        py.draw.rect(WIN, WHITE, right_paddle.rect)
        py.draw.circle(WIN, WHITE, ball.rect.center,ball.rect.width/2)
        WIN.blit(player1_score.text, player1_score.rect)
        WIN.blit(player2_score.text, player2_score.rect)


    

while run:
    for event in py.event.get():
        if event.type == py.QUIT:
            run = False
            py.quit()
            sys.exit()
                 
    
    update()
    py.display.update()

    clock.tick(60)