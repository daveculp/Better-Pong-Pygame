import pygame
import random
import time
import math
import sys

def check_pygame_events():
	global player1_speed, player2_speed, game_state
	
	keys = pygame.key.get_pressed()
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		pygame.quit()
		sys.exit()
		
	if keys[pygame.K_t] and game_state == GAME_STATE_WON:
		game_state = GAME_STATE_TITLE
	if keys[pygame.K_SPACE] and game_state == GAME_STATE_TITLE:
		game_state = GAME_STATE_RUNNING
	if keys[pygame.K_ESCAPE]:
		pygame.quit()
		sys.exit()
	if keys[pygame.K_DOWN]:
		player2_speed = 8
	if keys[pygame.K_UP]:
		player2_speed = -8
	if keys[pygame.K_s]:
		player1_speed = 8
	if keys[pygame.K_w]:
		player1_speed = -8
	return		
		
def move_objects():
	global player1, player2, ball
	global player2_speed, player1_speed
	
	#first move the players
	player2.y += player2_speed
	player1.y += player1_speed

	#reset players speed to 0
	player1_speed = player2_speed = 0
	
	#move the ball
	ball.x = ball.x + ball_delta_x
	ball.y = ball.y + ball_delta_y	
	
	return   
	       
def check_bounds():
	global player1, player2, ball_delta_y, ball 
	
	#check if the right most paddle has tried to move too far up or down
	if player2.top < 0:
		player2.top = 0
	elif player2.bottom > SCREEN_HEIGHT:
		player2.bottom = SCREEN_HEIGHT
		
	#check if the right most paddle has tried to move too far up or down		
	if player1.top < 0:
		player1.top = 0
	elif player1.bottom > SCREEN_HEIGHT:
		player1.bottom = SCREEN_HEIGHT
		
	#check if the ball has hit the top or bottom edges
	if ball.top <= 0:
		ball.top = 1 
		ball_delta_y = -ball_delta_y
	elif ball.bottom >= SCREEN_HEIGHT:
		ball.bottom = SCREEN_HEIGHT-1
		ball_delta_y = -ball_delta_y
		
	return
	
def check_collisions():
	global ball_delta_x, ball_delta_y,ball 
	
	#check collisions with player 1
	if ball.colliderect(player1):
		pygame.mixer.Sound.play(pong_sound)
		ball.left = player1.right + 2 #move the ball to just outside the paddle
		hit_loc = player1.centery - ball.y #where did we hit the paddle at (40 to -40)
		normalize_hit = hit_loc/(PADDLE_HEIGHT/2) #covert to -1 to 1
		bounce_angle = normalize_hit * (5*math.pi/12) #get the bounce angle in radians
		ball_delta_x = BALL_SPEED*math.cos(bounce_angle)
		ball_delta_y = BALL_SPEED*-math.sin(bounce_angle)
		
	#check collisions with player 2
	elif ball.colliderect(player2):
		pygame.mixer.Sound.play(pong_sound)
		ball.right = player2.left + 2
		hit_loc = player2.centery - ball.y
		normalize_hit = hit_loc/(PADDLE_HEIGHT/2)
		bounce_angle = normalize_hit * MAX_ANGLE
		ball_delta_x = BALL_SPEED*-math.cos(bounce_angle)
		ball_delta_y = BALL_SPEED*-math.sin(bounce_angle)
	return

def check_miss():
	global player1_score, player2_score, ball 

	if ball.right<player1.left:
		player2_score+=1
		time.sleep(3)
		reset_ball()
		return
		
	if ball.left>player2.right:
		player1_score+=1
		time.sleep(3)
		reset_ball()
		return
		
def reset_ball():
	global ball_delta_x, ball_delta_y, ball 
	
	ball.x = SCREEN_HEIGHT//2
	ball.y = SCREEN_WIDTH//2
	
	direction = random.uniform(-1,1)
	angle = direction * MAX_ANGLE
	ball_delta_x = BALL_SPEED*math.cos(angle)
	ball_delta_y = BALL_SPEED*-math.sin(angle)
	
	return

	
def draw_screen():
	screen.fill( BLACK ) #paint the background in black
	
	#draw the player paddles
	pygame.draw.rect(screen, RED, player1)
	pygame.draw.rect(screen, GREEN, player2)
	pygame.draw.ellipse(screen, BLUE, ball)
	
	score2_text = font.render(str(player2_score), 1, GREEN)
	screen.blit(score2_text,(SCREEN_WIDTH-100, 10) )
	
	score1_text = font.render(str(player1_score), 1, RED)
	screen.blit(score1_text,(100, 10))
	
	#draw the centerline 
	pygame.draw.line(screen, WHITE, (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2, SCREEN_HEIGHT))

def title_screen():
	player1_score = player2_score = 0
	screen.fill( RED ) #paint the background in black
	pong_text = title_font.render("PONG",True, BLACK)
	pong_rect = pong_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
	screen.blit(pong_text,pong_rect)

	press_text = font.render("Press SPACE to begin!",True, BLACK)
	press_rect = press_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-200))
	screen.blit(press_text,press_rect)

def check_win():
	global game_state
	
	if player1_score >= WIN_SCORE or player2_score >= WIN_SCORE:
		game_state = GAME_STATE_WON
		
def win_screen():
	global player1_score, player2_score
	
	screen.fill( BLACK ) #paint the background in black
	over_text = title_font.render("GAME OVER!",True, RED)
	over_rect = over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
	screen.blit(over_text,over_rect)

	print(player1_score, player2_score)
	if player1_score > player2_score:
		winner_text = "Player 1 is the WINNER!"
	else:
		winner_text = "Player 2 is the WINNER!"
	
	win_text = font.render(winner_text,True, RED)
	win_rect = win_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-200))
	screen.blit(win_text,win_rect)	
		
	press_text = font.render("Press T to start again or ESC to quit!",True, RED)
	press_rect = press_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
	screen.blit(press_text,press_rect)	
	
#======================================================================
#                       Gloabls and Constants area                    =
#======================================================================
#Our screen width and height
SCREEN_WIDTH = 1024 
SCREEN_HEIGHT= 768

BALL_SPEED = 8
MAX_ANGLE = 5*math.pi/12 #75 degrees in radians

#define some colors
BLACK = 0,0,0
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
WHITE = 255,255,255

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80

WIN_SCORE = 7 #max score to play to

ball_radius = 5
ball_delta_x = 0
ball_delta_y = 0
ball = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,ball_radius*2,ball_radius*2)

player1_x = 30
player1_y = SCREEN_HEIGHT//2
player1_score = 0
player1_speed = 7
player1 = pygame.Rect( 30, SCREEN_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

player2_x = SCREEN_WIDTH - (PADDLE_WIDTH+30)
player2_y = SCREEN_HEIGHT//2
player2_score = 0
player2_speed = 7
player2 = pygame.Rect( player2_x, player2_y, PADDLE_WIDTH, PADDLE_HEIGHT)

#constants to track game state
GAME_STATE_TITLE = 0
GAME_STATE_RUNNING = 1
GAME_STATE_WON = 2

#======================================================================
#                       Initilizations area                           =
#======================================================================

pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
pygame.init()
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF )
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

#setup our font
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 136)

#load sounds
pong_sound = pygame.mixer.Sound('blip.ogg')

game_state = GAME_STATE_TITLE
reset_ball()

#======================================================================
#                       Main Game Loop                                =
#======================================================================
while True:
	check_pygame_events()
	if game_state == GAME_STATE_RUNNING:
		move_objects()
		check_bounds() #make sure ball and paddles have not moved off screen
		check_collisions()
		check_miss() #did a player miss hitting the ball
		check_win() #has a player won?
		draw_screen()
	elif game_state == GAME_STATE_TITLE:
		title_screen()
	elif game_state == GAME_STATE_WON:
		win_screen()
		
	pygame.display.flip()
	clock.tick(60) 
