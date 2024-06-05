import pygame
import random
import sys

pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.key.set_repeat(1, 1)

# 변수 설정
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
large_font = pygame.font.SysFont('malgungothic', 72)
small_font = pygame.font.SysFont('malgungothic', 36)
p1_score = 0
p2_score = 0
P1_WIN = 1
P2_WIN = 2
game_over = 0
p1_skill_point = 0
p2_skill_point = 0
MAX_SKILL_POINT = 3
p1_skill_active = False
p2_skill_active = False
p1_skill_time = 0
p2_skill_time = 0
SKILL_DURATION = 3000  # 3초
paddle_image = pygame.image.load("pi.png")
ball = pygame.Rect(SCREEN_WIDTH // 2 - 16 // 2, SCREEN_HEIGHT // 2 - 16 // 2, 16, 16)
ball_speed = 5
ball_dx = ball_speed
ball_dy = -ball_speed

p1_paddle = pygame.Rect(0, SCREEN_HEIGHT // 2 - 80 // 2, 16, 80)
p2_paddle = pygame.Rect(SCREEN_WIDTH - 15, SCREEN_HEIGHT // 2 - 80 // 2, 16, 80)


# 총알 관련 변수
bullet_width = 20
bullet_height = 10
bullet_speed = 30
p1_last_bullet_time = pygame.time.get_ticks()  # 플레이어 1의 마지막 총알 발사 시간
p2_last_bullet_time = pygame.time.get_ticks()  # 플레이어 2의 마지막 총알 발사 시간
bullet_cooldown = 3000  # 총알 발사 쿨다운: 3초 (단위: 밀리초)
p1_bullets = []  # 플레이어 1의 총알 리스트
p2_bullets = []  # 플레이어 2의 총알 리스트

#효과음
boom_sound = pygame.mixer.Sound("boom.WAV")
boing_sound = pygame.mixer.Sound("boing.WAV.mp3")
ding_sound = pygame.mixer.Sound("1. 띠링.mp3")
shoot_sound= pygame.mixer.Sound('shoot.WAV.mp3')


# 배경음악 로드 및 재생
pygame.mixer.music.load("배경음악.mp3")
pygame.mixer.music.set_volume(0.5)  # 음량 설정 (0.0 ~ 1.0)
pygame.mixer.music.play(loops=-1)  # 배경음악 반복 재생

exit = True

def draw_text(text, font, color, surface, x, y):
    textobj = large_font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('게임 시작', large_font, WHITE, screen, 230, 250)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # 마우스 클릭 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 300 <= mouse_x <= 500 and 250 <= mouse_y <= 300:
                    return  # 게임 시작 버튼 클릭 시 메인 메뉴 루프를 빠져나옴

        pygame.display.update()


def start_game():
    # 카운트다운 함수 호출
    countdown()

def countdown():
    # 3초 카운트다운 표시
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        draw_text(str(i), large_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.update()
        pygame.time.wait(1000)  # 1초 대기

# 메인 메뉴 호출
main_menu()
# 게임 시작
start_game()

while exit:
    screen.fill(BLACK)

    # 변수 업데이트
    current_time = pygame.time.get_ticks()  # 현재 시간 가져오기
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False
        if event.type == pygame.KEYDOWN:
            # 플레이어 1이 z키를 누르고 총알 발사 쿨다운이 지난 경우에만 총알 생성
            if event.key == pygame.K_z and current_time - p1_last_bullet_time > bullet_cooldown:
                new_bullet = pygame.Rect(p1_paddle.centerx, p1_paddle.centery, bullet_width, bullet_height)
                p1_bullets.append(new_bullet)
                p1_last_bullet_time = current_time  # 총알 발사 시간 업데이트
            # 플레이어 2가 l키를 누르고 총알 발사 쿨다운이 지난 경우에만 총알 생성
            elif event.key == pygame.K_l and current_time - p2_last_bullet_time > bullet_cooldown:
                new_bullet = pygame.Rect(p2_paddle.centerx - bullet_width, p2_paddle.centery, bullet_width, bullet_height)
                p2_bullets.append(new_bullet)
                p2_last_bullet_time = current_time  # 총알 발사 시간 업데이트
            
            # 패들 이동
            if event.key == pygame.K_w:
                p1_paddle.top -= 2
            elif event.key == pygame.K_s:
                p1_paddle.top += 2
            if event.key == pygame.K_UP:
                p2_paddle.top -= 2
            elif event.key == pygame.K_DOWN:
                p2_paddle.top += 2
                
            # 플레이어 1의 스킬 발동
            if event.key == pygame.K_x and p1_skill_active:
                print("Player 1's skill activated!")
                shoot_sound.play()
                p1_skill_time = current_time  # 스킬 사용 시간 기록
                p1_skill_active = False  # 스킬 사용 후 비활성화
                p1_skill_point = 0  # 스킬 포인트 초기화
                
              # 플레이어 1의 스킬 사용 후 4 스킬 포인트가 모일 때 큰 총알 발사
            if event.key == pygame.K_x and p1_skill_active and p1_skill_point >= MAX_SKILL_POINT:
                print("Player 1's big bullet activated!")
                shoot_sound.play()
                p1_skill_active = False  # 스킬 사용 후 비활성화
                p1_skill_point = 0  # 스킬 포인트 초기화
            # 플레이어 2의 스킬 발동
            if event.key == pygame.K_SEMICOLON and p2_skill_active:
                print("Player 2's skill activated!")
                shoot_sound.play()
                p2_skill_time = current_time  # 스킬 사용 시간 기록
                p2_skill_active = False  # 스킬 사용 후 비활성화
                p2_skill_point = 0  # 스킬 포인트 초기화
            
            if event.key == pygame.K_SEMICOLON and p2_skill_active and p2_skill_point >= MAX_SKILL_POINT:
                print("Player 2's big bullet activated!")
                shoot_sound.play()
                p2_skill_active = False  # 스킬 사용 후 비활성화
                p2_skill_point = 0  # 스킬 포인트 초기화

    # 게임 오버 확인
    if game_over == 0:
        if p1_score >= 5:
            game_over = P1_WIN
            pygame.mixer.music.load("승리브금.WAV.wav")
            pygame.mixer.music.set_volume(1.0)  # 음량 설정 (0.0 ~ 1.0)
            pygame.mixer.music.play(loops=1)  # 음악 반복 재생
        if p2_score >= 5:
            game_over = P2_WIN
            pygame.mixer.music.load("승리브금.WAV.wav")
            pygame.mixer.music.set_volume(1.0)  # 음량 설정 (0.0 ~ 1.0)
            pygame.mixer.music.play(loops=1)  # 음악 반복 재생
        ball.left += ball_dx
        ball.top += ball_dy

    # 공의 충돌 처리
    if ball.left < 0:
        p2_score += 1
        ding_sound.play()
        ball.centerx = SCREEN_WIDTH // 2
        ball.centery = SCREEN_HEIGHT // 2
        ball_speed = 5
        ball_dx = ball_speed
        ball_dy = -ball_speed
        pygame.display.update()
        pygame.time.wait(3000)  # 3초 지연

    elif ball.right > SCREEN_WIDTH:
        p1_score += 1
        ding_sound.play()
        ball.centerx = SCREEN_WIDTH // 2
        ball.centery = SCREEN_HEIGHT // 2
        ball_speed = 5
        ball_dx = 5
        ball_dy = -5
        pygame.display.update()
        pygame.time.wait(3000)  # 3초 지연

    #공이 화면에 닿을경우
    if ball.top < 0 or ball.bottom > SCREEN_HEIGHT:
        ball_dy *= -1
        boing_sound.play()

    # 패들 이동 제한
    if p1_paddle.top < 0:
        p1_paddle.top = 0
    elif p1_paddle.bottom > SCREEN_HEIGHT:
        p1_paddle.bottom = SCREEN_HEIGHT

    if p2_paddle.top < 0:
        p2_paddle.top = 0
    elif p2_paddle.bottom > SCREEN_HEIGHT:
        p2_paddle.bottom = SCREEN_HEIGHT

    # 패들과 공의 충돌 처리(속도 up)
    if ball.colliderect(p1_paddle):
        ball_dx = abs(ball_dx)
        if ball.centery <= p1_paddle.right or ball.centery > p1_paddle.bottom or ball.centery > p1_paddle.top:
            boing_sound.play()
            ball_dy *= 1.1
            ball_dx *= 1.1
            ball_speed *= 1.2

        # 플레이어 1의 스킬 사용 후 3초 내에 충돌 시 공 속도 증가
        if current_time - p1_skill_time <= SKILL_DURATION and p1_skill_time > 0:
            ball_speed *= 2
            ball_dx = ball_speed if ball_dx > 0 else -ball_speed
            ball_dy = ball_speed if ball_dy > 0 else -ball_speed
            p1_skill_time = 0  # 스킬 시간 초기화
    #플레이어 2패들 충돌
    if ball.colliderect(p2_paddle):
        ball_dx = -abs(ball_dx)
        if ball.centery <= p2_paddle.left or ball.centery > p2_paddle.bottom or ball.centery > p2_paddle.top:
            boing_sound.play()
            ball_dy *= 1.1
            ball_dx *= 1.1
            ball_speed *= 1.2
        # 플레이어 2의 스킬 사용 후 3초 내에 충돌 시 공 속도 증가
        if current_time - p2_skill_time <= SKILL_DURATION and p2_skill_time > 0:
            ball_speed *= 2
            ball_dx = ball_speed if ball_dx > 0 else -ball_speed
            ball_dy = ball_speed if ball_dy > 0 else -ball_speed
            p2_skill_time = 0  # 스킬 시간 초기화

    # 총알 이동
    for bullet in p1_bullets:
        bullet.x += bullet_speed
        pygame.draw.rect(screen, RED, bullet)
    for bullet in p2_bullets:
        bullet.x -= bullet_speed
        pygame.draw.rect(screen, BLUE, bullet)

    # 총알과 패들의 충돌 처리 및 스킬 포인트 부여
    for bullet in p1_bullets:
        if bullet.colliderect(p2_paddle):
            boom_sound.play()
            p1_skill_point += 1  # 플레이어 1의 스킬 포인트 증가
            p1_bullets.remove(bullet)  # 충돌한 총알 제거
    for bullet in p2_bullets:
        if bullet.colliderect(p1_paddle):
            boom_sound.play()
            p2_skill_point += 1  # 플레이어 2의 스킬 포인트 증가
            p2_bullets.remove(bullet)  # 충돌한 총알 제거

    # 플레이어 1의 스킬 포인트를 화면에 표시
    if p1_skill_point >= MAX_SKILL_POINT: #스킬포 최대치 넘었을 경우
        p1_skill_point_text = small_font.render('MAX', True, YELLOW)
        screen.blit(p1_skill_point_text, (10, SCREEN_HEIGHT - 50))
        p1_skill_active = True
    else: #스킬포 최대치 x
        p1_skill_point_text = small_font.render('스킬 포인트: {}'.format(p1_skill_point), True, YELLOW)
        screen.blit(p1_skill_point_text, (10, SCREEN_HEIGHT - 50))

    # 플레이어 2의 스킬 포인트를 화면에 표시
    if p2_skill_point >= MAX_SKILL_POINT: #스킬포 최대치 넘었을 경우
        p2_skill_point_text = small_font.render('MAX', True, YELLOW)
        screen.blit(p2_skill_point_text, (SCREEN_WIDTH - p2_skill_point_text.get_width() - 10, SCREEN_HEIGHT - 50))
        p2_skill_active = True
    else: #스킬포 최대치 x
        p2_skill_point_text = small_font.render('스킬 포인트: {}'.format(p2_skill_point), True, YELLOW)
        screen.blit(p2_skill_point_text, (SCREEN_WIDTH - p2_skill_point_text.get_width() - 10, SCREEN_HEIGHT - 50))

    # 게임 요소 그리기
    pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2) #공
    pygame.draw.rect(screen, RED, p1_paddle)#패들
    pygame.draw.rect(screen, BLUE, p2_paddle)#패들
    p1_score_image = small_font.render('P1 {}'.format(p1_score), True, YELLOW) #점수판
    screen.blit(p1_score_image, (10, 10))
    p2_score_image = small_font.render('P2 {}'.format(p2_score), True, YELLOW)
    screen.blit(p2_score_image, p2_score_image.get_rect(right=SCREEN_WIDTH - 10, top=10))

    # 게임 종료 표시
    if game_over > 0:
        if game_over == P1_WIN:
            p1_win_image = large_font.render('P1 승리', True, RED)
            screen.blit(p1_win_image, p1_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
        elif game_over == P2_WIN:
            p2_win_image = large_font.render('P2 승리', True, BLUE)
            screen.blit(p2_win_image, p2_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
