import pygame
from sys import exit
from random import randint
from random import random

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

        self.type = type  # 장애물 타입
        self.speed = speed  # 속도

        # 장애물 타입에 따라 이미지 및 위치 설정
        if self.type == 'fly':
            fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            self.rect = self.frames[0].get_rect(midtop=(800, 190))  # x: 화면 오른쪽 끝, y: 50 ~ 200 사이
        elif self.type == 'snail':
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            self.rect = self.frames[0].get_rect(midbottom=(800, 300))  # x: 화면 오른쪽 끝, y: 300
        elif self.type == 'hailstone':
            self.image = pygame.image.load('graphics/hailstone.png').convert_alpha()  # 떨어지는 장애물 이미지
            self.rect = self.image.get_rect(midtop=(randint(50, 750), -50))  # y: 화면 위에서 시작
        else:
            self.image = None  # 기본 값

        self.animation_index = 0
        self.image = self.frames[0] if self.type != 'hailstone' else self.image  # 기본 이미지 설정

    def update(self):
        # 장애물 애니메이션 업데이트 (fly, snail만 해당)
        if self.type != 'hailstone':
            self.animation_state()

        # 장애물 이동 (fly, snail은 x축, hailstone은 y축)
        if self.type == 'hailstone':
            self.rect.y += self.speed  # 떨어지는 장애물은 y축으로 이동
        else:
            self.rect.x -= self.speed  # fly와 snail은 x축으로 이동

        self.destroy()

    def animation_state(self):
        # fly와 snail의 애니메이션 업데이트
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        # 화면을 벗어난 장애물은 삭제
        if self.type == 'hailstone' and self.rect.top > 400:  # falling_rock은 화면 아래로 떨어지면 삭제
            self.kill()
        elif self.type != 'hailstone' and self.rect.x <= -100:  # fly, snail은 화면 왼쪽으로 벗어나면 삭제
            self.kill()

def display_score(start_time):
    #current_time = int(pygame.time.get_ticks() / 1000) - start_time
    #score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    total_score = current_time + global_score  # 총 점수 계산
    score_surf = test_font.render(f'Score: {total_score}', False, (64, 64, 64))
    
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    #return current_time
    return total_score

def collision_sprite(player, obstacle_group):
    # 플레이어와 장애물이 충돌하면 게임 오버 처리
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        # 게임 오버 시 점수와 속도 초기화
        reset_game()
        return False
    else:
        return True

def reset_game():
    global game_active, character_selected, start_time, global_score, obstacle_speed, current_background_index, last_speed_increase_time
    # 초기화할 변수들
    game_active = False
    character_selected = False
    start_time = 0
    global_score = 0  # 점수 초기화
    obstacle_speed = 6  # 장애물 속도 초기화
    current_background_index = 0
    last_speed_increase_time = pygame.time.get_ticks()
    
    # 그룹 초기화
    obstacle_group.empty()
    coin_group.empty()

    # 배경과 캐릭터 선택 화면을 다시 표시
    player.empty()  # 플레이어를 초기화
    # 캐릭터 선택 화면으로 돌아가기 위해서 다시 캐릭터 선택 화면을 보여줘야 함


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
global_score = 0

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

# 배경 이미지 리스트 (각 속도에 맞는 배경 추가)
backgrounds = [
    pygame.image.load('graphics/morning.png').convert(),  # 배경 1 (최초 속도)
    pygame.image.load('graphics/evening.png').convert(),  # 배경 2 (속도 증가 1)
    pygame.image.load('graphics/midnight.png').convert(),  # 배경 3 (속도 증가 2)
    pygame.image.load('graphics/hell.png').convert()   # 배경 4 (속도 증가 3)
]

current_background_index = 0  # 초기 배경 인덱스

# 장애물 속도 초기 설정
obstacle_speed = 6
speed_increase_interval = 30000  # 30초마다 속도 증가
last_speed_increase_time = pygame.time.get_ticks()  # 마지막 속도 증가 시간 기록

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
                    # 'falling rock' 생성 확률을 추가
                    obstacle_type = random()
                    if obstacle_type < 0.33:  # 약 1/3 확률로 FallingRock 생성
                        obstacle_group.add(Obstacle('hailstone', obstacle_speed))
                    else:
                        # fly와 snail 생성 확률을 50%로 설정
                        obstacle_type = 'fly' if random() < 0.5 else 'snail'
                        obstacle_group.add(Obstacle(obstacle_type, obstacle_speed))
            
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
        screen.blit(backgrounds[current_background_index], (0, 0))  # 배경을 업데이트
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
            if pygame.sprite.collide_rect(coin, player.sprite):  # Rect 충돌 확인
                coin.kill()  # 코인을 제거
                global_score += 1  # 점수 추가

        game_active = collision_sprite(player, obstacle_group)

        # 30초마다 속도 증가 및 배경 변경
        current_time = pygame.time.get_ticks()
        if current_time - last_speed_increase_time >= speed_increase_interval:
            # 속도 증가
            obstacle_speed += 1
            # 배경 변경
            current_background_index += 1
            if current_background_index >= len(backgrounds):
                current_background_index = len(backgrounds) - 1  # 더 이상 배경이 없으면 마지막 배경 유지
            last_speed_increase_time = current_time  # 마지막 시간 업데이트

    else:
        # Game over screen
        screen.fill((94, 129, 162))
        
        # 선택된 캐릭터의 스탠드 이미지로 업데이트
        player_stand = pygame.image.load(f'graphics/Player/{character_choice}/stand.png').convert_alpha()
        player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
        player_stand_rect = player_stand.get_rect(center=(400, 200))
        
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
