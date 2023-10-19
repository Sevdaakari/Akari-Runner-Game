import pygame
from sys import exit
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 =  pygame.transform.scale(pygame.image.load('assets/images/player_walk_1.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        player_walk_2 =  pygame.transform.scale(pygame.image.load('assets/images/player_walk_2.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.transform.scale(pygame.image.load('assets/images/jump.png').convert_alpha(), (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,302))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('assets/audio/punch-1-166694.mp3')
        self.jump_sound.set_volume(0.5)


    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 301:
            self.rect.bottom = 301

    def animation_state(self):
        if self.rect.bottom < 301:
            self.image = self.player_jump    
        else:
            self.player_index += 0.1
            if self.player_index >=len(self.player_walk):
                self.player_index = 0 
            self.image = self.player_walk[int(self.player_index)]           

    def update(self):
        self.player_input()
        self.apply_gravity()  
        self.animation_state()   


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_image_1 = pygame.transform.scale(pygame.image.load('assets/images/Fly1.png').convert_alpha(), (PLAYER_WIDTH*0.9, PLAYER_HEIGHT*0.9))
            fly_image_2 = pygame.transform.scale(pygame.image.load('assets/images/Fly2.png').convert_alpha(), (PLAYER_WIDTH*0.9, PLAYER_HEIGHT*0.9))
            self.frames = [fly_image_1, fly_image_2]
            y_pos = 200
        else:
            fighter_img_1 = pygame.transform.scale(pygame.image.load('assets/images/fighter1.png').convert_alpha(), (PLAYER_WIDTH*0.9, PLAYER_HEIGHT*0.9))
            fighter_img_2 = pygame.transform.scale(pygame.image.load('assets/images/fighter2.png').convert_alpha(), (PLAYER_WIDTH*0.9, PLAYER_HEIGHT*0.9))
            self.frames = [fighter_img_1, fighter_img_2]  
            y_pos = 304   
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]   

    def update(self):
        self.animation_state()
        self.rect.x -= 6   
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()      
            

def display_score():
    current_time = int(pygame.time.get_ticks()/1000 - start_time)
    score_surf = score_font.render(f"SCORE: {current_time}", False, "#EEEEEE") 
    score_rect = score_surf.get_rect(center=(WIDTH/2, 20))
    screen.blit(score_surf, score_rect)
    return current_time
     

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True 


pygame.init()
WIDTH = 800
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Akari Runner")

clock = pygame.time.Clock()
FPS = 60
GAME_IS_ON = False
start_time = 0
score = 0

text_font = pygame.font.Font('assets/fonts/Wallpoet-Regular.ttf', 35)
score_font = pygame.font.Font('assets/fonts/Wallpoet-Regular.ttf', 20)

SKY_IMAGE = pygame.transform.scale(pygame.image.load('assets/images/Sky.png').convert(), (WIDTH, HEIGHT))
START_BG = pygame.image.load('assets/images/start_bg.png').convert()
GROUND_IMAGE = pygame.image.load('assets/images/Ground.png').convert()

bg_music = pygame.mixer.Sound('assets/audio/insen-scale-loop-suitable-for-rap-music-longer-119864.mp3')
bg_music.set_volume(0.2) 
bg_music.play(loops = -1)

PLAYER_WIDTH = 90
PLAYER_HEIGHT = 90
player_stand = pygame.transform.scale(pygame.image.load('assets/images/player_stand.png').convert_alpha(), (PLAYER_WIDTH*2, PLAYER_HEIGHT*2))
player_stand_rect = player_stand.get_rect(center=(WIDTH/2, HEIGHT/2))

game_title = text_font.render("Akari Runner", False, "black") 
game_title_rect = game_title.get_rect(center=(WIDTH/2, HEIGHT/5.5))

instructions = text_font.render("Press space to play", False, "black") 
instructions_rect = instructions.get_rect(center=(WIDTH/2, HEIGHT/1.2))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

fighter_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fighter_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 300)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if GAME_IS_ON:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(['fly', 'fighter', 'fighter', 'fighter'])))
            
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_IS_ON = True
                start_time = int(pygame.time.get_ticks()/1000)

   
    if GAME_IS_ON:
        screen.blit(SKY_IMAGE, (0,0))
        screen.blit(GROUND_IMAGE, (0, 300))    
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        GAME_IS_ON = collision_sprite()

    else:
        screen.blit(START_BG, (0,0))
        screen.blit(player_stand, player_stand_rect)  

        score_msg = text_font.render(f"Your score: {score}", False, ("black"))
        score_msg_rect = score_msg.get_rect(center = (WIDTH/2, HEIGHT/1.2))
        screen.blit(game_title, game_title_rect)   

        if score == 0:
            screen.blit(instructions, instructions_rect) 
        else:
            screen.blit(score_msg, score_msg_rect)


    pygame.display.update()
    clock.tick(FPS)