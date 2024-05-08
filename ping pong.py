import pygame #파이 게임 모듈 임포트

pygame.init() #파이 게임 초기화
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #화면 크기 설정
clock = pygame.time.Clock() 
pygame.key.set_repeat(1, 1)

#변수

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

ball = pygame.Rect(SCREEN_WIDTH // 2 - 16 // 2, SCREEN_HEIGHT // 2 - 16 // 2, 16, 16)
ball_dx = 5
ball_dy = -5

p1_paddle = pygame.Rect(0, SCREEN_HEIGHT // 2 - 80 // 2, 16, 80)

p2_paddle = pygame.Rect(SCREEN_WIDTH - 15, SCREEN_HEIGHT // 2 - 80 // 2, 16, 80)

#pygame.mixer.init()
#pygame.mixer.music.load('music.mid') #배경 음악
#pygame.mixer.music.play(-1) #-1: 무한 반복, 0: 한번
#bounce_sound = pygame.mixer.Sound('bounce.wav') #사운드
#p1_win_sound = pygame.mixer.Sound('p1_win.wav')
#p2_win_sound = pygame.mixer.Sound('p2_win.wav')
exit=True


while exit: #게임 루프
    screen.fill(BLACK) #단색으로 채워 화면 지우기

    #변수 업데이트
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                p1_paddle.top -= 1
            elif event.key==pygame.K_s:
                p1_paddle.top += 1
            if event.key==pygame.K_UP:
                p2_paddle.top -= 1
            elif event.key==pygame.K_DOWN:
                p2_paddle.top += 1
        
    
    if game_over == 0:
        if p1_score >= 5:
            game_over = P1_WIN

        if p2_score >= 5:
            game_over = P2_WIN


        ball.left += ball_dx
        ball.top  += ball_dy    

    
    if ball.left < 0:
        p2_score += 1
        ball.centerx = SCREEN_WIDTH // 2
        ball.centery = SCREEN_HEIGHT // 2
        ball_dx = 5
        ball_dy = -5
    elif ball.right > SCREEN_WIDTH:
        p1_score += 1
        ball.centerx = SCREEN_WIDTH // 2
        ball.centery = SCREEN_HEIGHT // 2
        ball_dx = 5
        ball_dy = -5
    if ball.top < 0 or ball.bottom > SCREEN_HEIGHT:
        ball_dy *= -1

    if p2_paddle.top < 0:
        p2_paddle.top = 0
    elif p2_paddle.bottom > SCREEN_HEIGHT:
        p2_paddle.bottom = SCREEN_HEIGHT
    if ball.colliderect(p1_paddle):
        ball_dx = ball_dx * -1
        if ball.centery <= p1_paddle.top or ball.centery > p1_paddle.bottom:
            ball_dy = ball_dy * -1
    if ball.colliderect(p2_paddle):
        ball_dx = ball_dx * -1
        if ball.centery <= p2_paddle.top or ball.centery > p2_paddle.bottom:
            ball_dy = ball_dy * -1


    #화면 그리기

    if game_over == 0:
        pygame.draw.circle(screen, WHITE, (ball.centerx, ball.centery), ball.width // 2)

    pygame.draw.rect(screen, BLUE, p1_paddle)

    pygame.draw.rect(screen, BLUE, p2_paddle)

    p1_score_image = small_font.render('P1 {}'.format(p1_score), True, YELLOW)
    screen.blit(p1_score_image, (10, 10))

    p2_score_image = small_font.render('P2 {}'.format(p2_score), True, YELLOW)
    screen.blit(p2_score_image, p2_score_image.get_rect(right=SCREEN_WIDTH - 10, top=10))

    if game_over > 0: 
        if game_over == P1_WIN:
            p1_win_image = large_font.render('P1 승리', True, RED)
            screen.blit(p1_win_image, p1_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))
        elif game_over == P2_WIN:
            p2_win_image = large_font.render('P2 승리', True, RED)
            screen.blit(p2_win_image, p2_win_image.get_rect(centerx=SCREEN_WIDTH // 2, centery=SCREEN_HEIGHT // 2))

    pygame.display.update() #모든 화면 그리기 업데이트
    clock.tick(30) #30 FPS (초당 프레임 수) 를 위한 딜레이 추가, 딜레이 시간이 아닌 목표로 하는 FPS 값
    pygame.display.flip()

pygame.quit() 
