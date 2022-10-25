import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int((pygame.time.get_ticks() - start_time)/1000)
    score_surface = font.render('Score: {time}'.format(time = current_time),False,(64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 8
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collision(player, obstacles_list):
    if obstacles_list:
        for obstacle in obstacle_list:
            if player.colliderect(obstacle): return False
        return True
    return True

def player_animation():
    global player_index,player_surface

    if player_rect.bottom == 300:
        player_index += 0.1
        if player_index > len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]
    else:
        player_surface = player_jump

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
start_time = 0
score = 0
game_active = False

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = font.render('Pixle Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = font.render('Press space to start', False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))



snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_index = 0
snails = [snail_1,snail_2]

fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_index = 0
flys = [fly_1,fly_2]


#obstacle
obstacle_list = []

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        if game_active:
            if event.type == obstacle_timer:
                x = randint(0,4)
                if x == 0 or x == 1:
                    obstacle_list.append((snail_surface.get_rect(bottomright = (randint(900,1200),300))))
                elif x == 2:
                    obstacle_list.append((fly_surface.get_rect(bottomright=(randint(900, 1200), 200))))
                else:
                    obstacle_list.append((fly_surface.get_rect(bottomright=(randint(900, 1200), 270))))
            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail_surface = snails[snail_index]
            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly_surface =flys[fly_index]

    if game_active:

        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface, (0, 300))


        #Player
        player_gravity +=1
        player_rect.y += player_gravity
        if player_rect.bottom > 300 : player_rect.bottom = 300


        player_animation()
        screen.blit(player_surface,player_rect)
        score = display_score()

        #obstacle move
        obstacle_list = obstacle_movement(obstacle_list)
        #collisons
        game_active = collision(player_rect,obstacle_list)
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        screen.blit(game_name,game_name_rect)
        player_rect = player_surface.get_rect(midbottom=(80, 300))
        obstacle_list.clear()
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            score_message = font.render(f'Your score is: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center=(400, 330))
            screen.blit(score_message, score_message_rect)
        start_time = pygame.time.get_ticks()

    pygame.display.update()
    clock.tick(60)