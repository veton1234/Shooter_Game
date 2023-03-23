from pygame import *
from random import randint
from time import time as timer

font.init()
font1 = font.Font(None,46)
score = 0
max_lost = 3
goal = 20
life = 3
win = font1.render('Winner!',1,(0,255,0))
lost = 0
lose = font1.render('Loser!',1,(255,0,0))
class Game(sprite.Sprite):
    def __init__(self,imazh,px,py,pw,ph,speed):
        super().__init__()
        self.image = transform.scale(image.load(imazh),(ph,pw))
        self.pw = pw
        self.ph = ph
        self.speed = speed
        
        self.rect = self.image.get_rect() 
        self.rect.x = px
        self.rect.y = py
   
    def reset(self):
        wind.blit(self.image,(self.rect.x, self.rect.y))
        
class Player(Game):
    def update(self):
        keys = key.get_pressed()
        if keys [K_LEFT] and self.rect.x > 5: 
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < 600: 
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15,15,15)
        bullets.add(bullet)

class Enemy(Game):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > wh:
            self.rect.x = randint(80, ww-80)
            self.rect.y = 0
            lost = lost + 1
class Bullet(Game):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

          

ww = 700
wh = 500
wind = display.set_mode((700,500))
display.set_caption('abc')
back = transform.scale(image.load('background.jpg'), (ww,wh))
player = Player('hunter.png',5,wh-80,80,70,15)

enemies = sprite.Group()
for i in range(1,6):
    enemy = Enemy('ufo.png',randint(80, ww - 80), -40, 80, 90, randint(1, 10))
    enemies.add(enemy)

bullets = sprite.Group()

finish = False

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png',randint(80, ww - 80),-40,80,90,randint(1,5)) 
    asteroids.add(asteroid)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

game = True
clock = time.Clock() 
FPS = 60
reltime = False
num_fire = 0


while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 5 and reltime == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and reltime == False:
                    last = timer()
                    reltime = True


    if not finish:
        wind.blit(back,(0,0)) 
        text = font1.render('Score: '+ str(score),1,(0,0,0))
        wind.blit(text,(10,10))
        text_lose = font1.render('Missed: '+ str(lost),1,(0,0,0))
        wind.blit(text_lose,(10,50))
        player.update()
        enemies.update()
        bullets.update()
        asteroids.update()
        player.reset()
        bullets.draw(wind)
        enemies.draw(wind)
        asteroids.draw(wind)
    
        if reltime == True:
            now = timer()
            if now - last < 3:
                rel = font1.render('Reloading',1,(255,0,0))
                wind.blit(rel,(260,460))
            else:
                num_fire = 0
                reltime = False

        collides = sprite.groupcollide(enemies,bullets,True,True)
        for c in collides:
            score = score + 1
            enemy = Enemy('ufo.png',randint(80, ww - 80), -40, 80, 90, randint(1, 5))
            enemies.add(enemy)

        if sprite.spritecollide(player,enemies,False) or sprite.spritecollide(player, asteroids,False):
            sprite.spritecollide(player,enemies,True)
            sprite.spritecollide(player,asteroids,True)
            life = life - 1

        if life == 0 or lost >= max_lost:
            finish = True
            wind.blit(lose,(200,200))

        if sprite.spritecollide(player,enemies,False) or sprite.spritecollide(player,asteroids,False) or lost >= max_lost:
            finish = True
            wind.blit(lose,(200,200))
        if score >= goal:
            finish = True
            wind.blit(win,(200,200))  
        if life == 3:
            life_col = (0,150,0)
        if life == 2:
            life_col = (150,150,0)
        if life == 1:
            life_col = (150,0,0)
    
        textlife = font1.render(str(life),1,life_col)
        wind.blit(textlife,(650,10))

    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for e in enemies:
            e.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            enemy = Enemy('ufo.png',randint(80, ww - 80), -40, 80, 90, randint(1,5))
            enemies.add(enemy)
        for i in range(1,3):
            asteroid = Enemy('asteroid.png',randint(80, ww - 80),-40,80,90,randint(1,7)) 
            asteroids.add(asteroid) 

    

    time.delay(50)     
    display.update() 