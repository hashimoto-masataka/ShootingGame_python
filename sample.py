import pygame# pygameをインポート
from pygame import mixer# 音声を読み込む
import random
import math

pygame.init() # pygameをインポートしたら必ずpygame.init()で初期化する
screen = pygame.display.set_mode((800, 600))# 画面の設定、800は横、600は縦


pygame.display.set_caption('Invaders Game') # windowの表示される名前を設定

# Player
playerImg = pygame.image.load('player.png') # 画像を変数に画像を読み込む,XとYに座標として変数に入れ,screen.blitで画像を差し込む
playerX, playerY= 370 , 480
playerX_change = 0 # 十字キーでplayerの位置を変えたいときにどれくらい変えるのかを指定、０は変化なし

#Enemy
enemyImg = pygame.image.load('enemy.png')
enemyX = random.randint(0, 736) #敵の配置を同じ場所からではなく範囲を決めてランダムな場所から出現させる
enemyY = random.randint(50, 150) #random.randintで任意の範囲の整数を出す。randomはライブラリなのでimportが必要
enemyX_change, enemyY_change = 4,40

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480 #弾はplayerから出るのでY軸はplayerに合わせる
bulletX_change, bulletY_change = 0, 3 #弾は横方向には動かないので０、Yに３ずつ進んでいく
bullet_state = 'ready' 


#Score
score_value = 0

def player(x, y):
    screen.blit(playerImg, (x,y)) # blit（オブジェクト,(X,Y))でオブジェクトをX,Y座標に配置
    #display.updateがあれば画像が表示される

def enemy(x,y):
    screen.blit(enemyImg, (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire' #弾が発射されたらfire_bullet関数が実行されている限りbullet_stateをfireにする
    screen.blit(bulletImg, (x + 16, y + 10)) #弾の大きさが横１６、縦１０の大きさ

def isCollision(enemyX, enemyY, bulletX, bulletY): #衝突したかどうかを計算
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)) 
    #mathで平方根をとって距離を算出
    if distance < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))  # whileでループしているのでループするたびに０,０,０の黒色で上書きしないとループ前の情報が残ってしまう
   
    # screen.blit(message, (20 ,50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # pygame.keydown もし何かキーを押したら
            if event.key == pygame.K_LEFT:
                playerX_change = -1.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 1.5
            if event.key == pygame.K_SPACE:
                 if bullet_state is 'ready':
                     bulletX = playerX #弾のXは０で見えなくしているが打つ時はXがplayerの座標になる
                     fire_bullet(bulletX, bulletY)
                     mixer.Sound('laser.wav').play() # 音声の出力を行う。While分の中に入れるとリピートされる

        if event.type == pygame.KEYUP:
            # pygame.KEYUP もし何かキーを離したら
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    playerX += playerX_change 
    if playerX <= 0: #ifで左端や右端に行った際にそれ以上いって見えなくなることを防ぐ
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #Enemy
    if enemyY > 440: #breakすることでWhileループから向け出す,440を敵が越えるとゲームオーバー
        break
    enemyX += enemyX_change
    if enemyX <= 0: #左端に来たら
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >= 736: #右端に来たら
        enemyX_change = -4 
        enemyY += enemyY_change

    collision = isCollision(enemyX, enemyY, bulletX, bulletY) #isCollisionで衝突したかどうか判断
    if collision: #衝突した場合IF文が実行される
        bulletY = 480 #衝突したらbulletをplayerの高さで再設定
        bullet_state = 'ready'
        score_value += 1 #衝突いたら得点が加算されたのでscoreを＋１する
        enemyX = random.randint(0, 736) #新たに敵の位置を再設定する
        enemyY = random.randint(50, 150)
    
    #bullet movement
    if bulletY <= 0: #bulletの位置が０より小さい＝弾が枠外に行ったら弾を480に再設定
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change #stateがfireになったらYを２６行目で設定している３ずつ進む


    #Score
    font = pygame.font.SysFont(None, 32) #fontの作成
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255)) #scoreの内容を定義
    screen.blit(score, (20,50)) #scoreの位置を指定 

    player(playerX,playerY)
    enemy(enemyX,enemyY)

    pygame.display.update()
    # screen上のものを書き換えた時はupdateする必要がある

