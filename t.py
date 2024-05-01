
import pygame
import math
#1. 게임 초기화
pygame.init()
#2. 게임창 옵션 설정
size=[500, 900]
screen=pygame.display.set_mode(size)
title="HANGMAN"
pygame.display.set_caption(title)
#3. 게임 내 필요한 설정
clock=pygame.time.Clock()
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)


def tup_r(tup):
    temp_list=[]
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

drop=False
exit=False
k=0

#4. 메인 이벤트
while not exit:
#.4-1 FPS 설정
    clock.tick(60)
#4-2. 각종 입력 감지
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            exit=True
#4-3. 입력, 시간에 따른 변화
#4-4. 그리기
    screen.fill(black)
    A=tup_r((0,size[1]*2/3))
    B=(size[0], A[1])
    C=tup_r((size[0]/6, A[1]))
    D=(C[0],C[0])
    E=tup_r((size[0]/2,D[1]))
    F=tup_r((E[0],E[1]+size[0]/6))
    pygame.draw.line(screen, white, A,B,3)
    pygame.draw.line(screen, white, C,D,3)
    pygame.draw.line(screen, white, D,E,3)
    pygame.draw.line(screen, white, E,F,3)       
    r_head=round(size[0]/12)
    
    if drop==False:
        pygame.draw.line(screen,white,E,F,3)
    
    if drop==True:
        G=(F[0],F[1]+r_head+k*5)
    else:
        G=(F[0],F[1]+r_head)
    pygame.draw.circle(screen,white,G,r_head,3)
    H=(G[0],G[1]+r_head)
    I=(H[0],H[1]+r_head)             
    pygame.draw.line(screen,white,H,I,3)  
    I_arm=r_head*2
    J=(I[0]-I_arm*math.cos(30*math.pi/180), I[1]+I_arm*math.sin(30*math.pi/180))
    J=tup_r(J)
    pygame.draw.line(screen,white,I,J,3)
    K=(I[0]+I_arm*math.cos(30*math.pi/180),I[1]+I_arm*math.sin(30*math.pi/180))
    pygame.draw.line(screen,white,I,K,3)
    L=(I[0],I[1]+r_head*2.5)
    pygame.draw.line(screen,white,I,L,3)
    I_leg=r_head*3
    N=(L[0]-I_leg*math.cos(60*math.pi/180), L[1]+I_arm*math.sin(60*math.pi/180))
    pygame.draw.line(screen,white,L,N,3)
    M=(L[0]+I_leg*math.cos(60*math.pi/180), L[1]+I_arm*math.sin(60*math.pi/180))
    pygame.draw.line(screen,white,L,M,3)
    B=(L[0]+5,L[1]+11)
    V=(L[0]-5,L[1]+11)
    I_jujy=r_head
    I_bural=r_head/6
    I_balgi=r_head*1.7
    pygame.draw.circle(screen,white,B,I_bural,3)
    pygame.draw.circle(screen,white,V,I_bural,3)
    Q=(L[0],L[1]+I_jujy)
    R=(L[0]+I_leg*math.cos(60*math.pi/180), L[1]-I_arm*math.sin(60*math.pi/180))
    pygame.draw.line(screen,white,L,Q,5)
    pygame.draw.circle(screen,white,L,5,6)
    if drop==False:
        O=tup_r((size[0]/2-size[0]/6, E[1]/2+F[1]/2))
        P=O[0]+k*2,O[1]
        if P[0]>size[0]/2+size[0]/6:
            drop=True
            k=0
        pygame.draw.line(screen,red,O,P,3)
                                              
                                                                                           
#4-5. 업데이트
    pygame.display.flip()
#5. 게임종료
pygame.quit()
        