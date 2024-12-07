import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, character="character1"):
        super().__init__()
        self.character = character
        self.load_character_assets()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0
        self.sliding = False

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
        self.speed = 5

    def load_character_assets(self):
        if self.character == "character1":
            self.load_character1_assets()
        elif self.character == "character2":
            self.load_character2_assets()
        elif self.character == "character3":
            self.load_character3_assets()

    def load_character1_assets(self):
        player_walk_1 = pygame.image.load('graphics/Player/character1/walk1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/character1/walk2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/character1/jump.png').convert_alpha()
        self.player_slide = pygame.image.load('graphics/Player/character1/slide.png').convert_alpha()
        self.player_index = 0

    def load_character2_assets(self):
        player_walk_1 = pygame.image.load('graphics/Player/character2/walk1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/character2/walk2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/character2/jump.png').convert_alpha()
        self.player_slide = pygame.image.load('graphics/Player/character2/slide.png').convert_alpha()
        self.player_index = 0

    def load_character3_assets(self):
        player_walk_1 = pygame.image.load('graphics/Player/character3/walk1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/character3/walk2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_jump = pygame.image.load('graphics/Player/character3/jump.png').convert_alpha()
        self.player_slide = pygame.image.load('graphics/Player/character3/slide.png').convert_alpha()
        self.player_index = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and not self.sliding:
            self.gravity = -20
            self.jump_sound.play()

        if keys[pygame.K_LEFT] and not self.sliding:
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0

        if keys[pygame.K_RIGHT] and not self.sliding:
            self.rect.x += self.speed
            if self.rect.right > 800:
                self.rect.right = 800

        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.sliding = True
        else:
            self.sliding = False

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.sliding:
            previous_midbottom = self.rect.midbottom
            self.image = self.player_slide
            self.rect = self.image.get_rect(midbottom=previous_midbottom)
        elif self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            previous_midbottom = self.rect.midbottom
            self.image = self.player_walk[int(self.player_index)]
            self.rect = self.image.get_rect(midbottom=previous_midbottom)

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('graphics/coin.png').convert_alpha()
            self.rect = self.image.get_rect(midbottom=(randint(50, 700), 300))  # x범위: 50 < x < 700, y: 260
            self.time_to_live = 5000  # 코인 5초 후 사라짐
            self.spawn_time = pygame.time.get_ticks()  # 코인 생성 시간 기록

        def update(self):
            if pygame.time.get_ticks() - self.spawn_time > self.time_to_live:
                self.kill()  # 시간이 지나면 코인 삭제

        def collision(self, player):
            if pygame.sprite.collide_rect(self, player):
                self.kill()
                return True
            return False

class Obstacle(pygame.sprite.Sprite):
    
    def __init__(self, type, speed):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 221
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        self.speed = speed

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score(start_time):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def character_selection_screen():
    screen.fill((94, 129, 162))
    title = test_font.render("Select Your Character", False, (255, 255, 255))
    title_rect = title.get_rect(center=(400, 50))
    screen.blit(title, title_rect)

    char1 = pygame.image.load('graphics/Player/character1/stand.png').convert_alpha()
    char2 = pygame.image.load('graphics/Player/character2/stand.png').convert_alpha()
    char3 = pygame.image.load('graphics/Player/character3/stand.png').convert_alpha()

    char1_rect = char1.get_rect(topleft=(100, 100))
    char2_rect = char2.get_rect(topleft=(200, 100))
    char3_rect = char3.get_rect(topleft=(300, 100))

    screen.blit(char1, char1_rect)
    screen.blit(char2, char2_rect)
    screen.blit(char3, char3_rect)

    select_message = test_font.render("Press 1, 2, or 3 to Choose", False, (255, 255, 255))
    select_message_rect = select_message.get_rect(center=(400, 350))
    screen.blit(select_message, select_message_rect)

    pygame.display.update()
    
    return char1_rect, char2_rect, char3_rect

# Pygame Initialization
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Pixel Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Game State Variables
game_active = False
character_selected = False
character_choice = "character1"
start_time = 0
score = 0

# Background Music
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.3)

# Groups
player = pygame.sprite.GroupSingle()
obstacle_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

# Graphics
sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('graphics/Player/character1/stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press SPACE to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

speed_increase_timer = pygame.USEREVENT + 2
pygame.time.set_timer(speed_increase_timer, 10000)  # 장애물 속도 10초마다 증가

coin_timer = pygame.USEREVENT + 3  # 코인 생성 타이머
pygame.time.set_timer(coin_timer, 1000)  # 1초마다 코인 생성

obstacle_speed = 6  # 초기 장애물 속도

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not character_selected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    character_choice = "character1"
                    character_selected = True
                elif event.key == pygame.K_2:
                    character_choice = "character2"
                    character_selected = True
                elif event.key == pygame.K_3:
                    character_choice = "character3"
                    character_selected = True

        if character_selected and not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                player = pygame.sprite.GroupSingle(Player(character_choice))

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(randint(0, 1), obstacle_speed))
            
            if event.type == speed_increase_timer:
                obstacle_speed += 1
                
            # 코인 생성
            if event.type == coin_timer:
                coin_group.add(Coin())

    if not character_selected:
        # Show character selection screen
        char1_rect, char2_rect, char3_rect = character_selection_screen()

    elif game_active:
        # Game is running
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score(start_time)

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        coin_group.draw(screen)
        coin_group.update()

        # 플레이어와 코인 충돌 확인
        for coin in coin_group:
            if coin.collision(player.sprite):
                score += 1  # 점수 추가


        game_active = collision_sprite(player, obstacle_group)

    else:
        # Game over screen
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)