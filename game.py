import pygame
import os
import sys
import random
import time
from pygame.locals import *
pygame.init()
W_WID=600
W_HEI=800
BASE=730
START_FONT=pygame.font.SysFont("comicsans",50)

WIN=pygame.display.set_mode(size=(700,900))
pygame.display.set_caption("FLAPPY BIRD GAME")

welcome_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","message.png")).convert_alpha())
pipe_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
bg_img=pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(),(700,800))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
game_over=pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","gameover.png")).convert_alpha())
SOUNDS={}#deepanshu add the sounds 
class Bird:
	ROTATION=25
	IMGS=bird_images
	VELOCITY=17
	ANIMATION_DELAY=5

	def __init__(self,x,y):
		self.x= x
		self.y= y
		self.tilt=0
		self.tick_count=0  
		self.vel=0 
		self.height= self.y
		self.img_count=0
		self.img=self.IMGS[0]

	def jump(self):
		self.vel = -8
		self.tick_count=0
		self.height= self.y
	def move(self):
		self.tick_count +=1
		displacement=self.vel*(self.tick_count)+0.5*(3)*(self.tick_count)**2
		#terminal velocity
		if displacement>=16:
			displacement=(displacement/abs(displacement))*16
		if displacement <0:
			displacement -=2
		self.y=self.y+displacement
		if displacement < 0 or self.y <self.height+50:
			if self.tilt<self.ROTATION:
				self.tilt=self.ROTATION
		else:
			if self.tilt>-90:
				self.tilt -= self.VELOCITY
	def draw(self,win):
		self.img_count+=1
		if self.img_count <= self.ANIMATION_DELAY:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIMATION_DELAY*2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_DELAY*3:
			self.img = self.IMGS[2]
		elif self.img_count <= self.ANIMATION_DELAY*4:
			self.img = self.IMGS[1]
		elif self.img_count == self.ANIMATION_DELAY*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0
		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_DELAY*2
		blitRotateCenter(win,self.img,(self.x,self.y),self.tilt)
	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Pipe():
	GAP =250 
	VEL=5
	def __init__(self,x):
		self.x=x
		self.height=0
		self.top=0
		self.bottom=0
		self.PIPE_TOP=pygame.transform.flip(pipe_img, False, True)
		self.PIPE_BOTTOM=pipe_img
		self.passed=False
		self.set_height()
	def set_height(self):
		self.height=random.randrange(50,450)
		self.top=self.height-self.PIPE_TOP.get_height()
		self.bottom=self.height+self.GAP
	def move(self):
		self.x-=self.VEL
	def draw(self,win):
		win.blit(self.PIPE_TOP,(self.x,self.top))
		win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))
	def collide(self,bird):
		bird_mask=bird.get_mask()
		top_mask=pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask=pygame.mask.from_surface(self.PIPE_BOTTOM)
		top_offset=(self.x-bird.x,self.top-round(bird.y))
		bottom_offset=(self.x-bird.x,self.bottom-round(bird.y))
		b_point=bird_mask.overlap(bottom_mask,bottom_offset)
		t_point=bird_mask.overlap(top_mask,top_offset)
		if b_point or t_point:
			return True
		return False

class Base: 
	VEL=5  
	WIDTH=base_img.get_width()
	IMG=base_img  
	def __init__(self,y):    
		self.y=y
		self.x1=0
		self.x2=self.WIDTH 
	def move(self): 
		self.x1-=self.VEL
		self.x2-=self.VEL 
		if self.x1+self.WIDTH<0:
			self.x1=self.x2+self.WIDTH
		if self.x2+self.WIDTH<0:
			self.x2=self.x1+self.WIDTH
	def draw(self,win):
		win.blit(self.IMG,(self.x1,self.y))
		win.blit(self.IMG,(self.x2,self.y))
	def collide(self,bird):
		bird_mask=bird.get_mask()
		baseMask=pygame.mask.from_surface(self.IMG)
		base_offset=(0-bird.x,self.y-round(bird.y))
		b_point=bird_mask.overlap(baseMask,base_offset)
		if b_point:
			return True
		return False

def blitRotateCenter(surf,image,topleft,angle):
	rotated_image=pygame.transform.rotate(image, angle)
	new_rect=rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
	surf.blit(rotated_image,new_rect.topleft)

def draw_window(win,bird,pipes,base,score):
	win.blit(bg_img,(0,0))
	for pipe in pipes:
		pipe.draw(win)
	base.draw(win)
	bird.draw(win)
	score_label=START_FONT.render("Score: "+str(score),1,(255,255,255))
	win.blit(score_label,(W_WID-score_label.get_width()-15,10))
	pygame.display.update()

def main_game():
	global WIN 
	win=WIN
	bird=Bird(230,350)
	base=Base(BASE)
	pipes=[Pipe(1000)]
	score=0
	clock=pygame.time.Clock() 
	run=True
	# time.sleep(3)
	while run:
		clock.tick(30) 
		bird.move()
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				print("your score is : ",score)
				pygame.quit() 
				sys.exit()
			if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
				SOUNDS['wing'].play()
				bird.jump()
		base.move()
		if base.collide(bird) or bird.y<-5:
			SOUNDS['die'].play()
			print("your score is : ",score)
			return
		rem=[]
		add_pipe=False

		for pipe in pipes:
			pipe.move()
			if pipe.collide(bird):
				SOUNDS['die'].play()
				print("your score is : ",score)
				return
			if pipe.x+pipe.PIPE_TOP.get_width()<0:
				rem.append(pipe)
			if not pipe.passed and pipe.x<bird.x:
				pipe.passed=True
				add_pipe=True
		if add_pipe:
			score+=1
			SOUNDS['point'].play()
			pipes.append(Pipe(W_WID+100))
		for r in rem:
			pipes.remove(r)
		draw_window(WIN,bird,pipes,base,score)

def welcomeScreen():
	global WIN
	win=WIN

	while True:
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
				SOUNDS['swoosh'].play()
				return
			else:
				win.blit(bg_img,(0,0))
				win.blit(base_img,(0,BASE))
				win.blit(base_img,(672,BASE))
				win.blit(welcome_img,(180,150))
				pygame.display.update()

if __name__=='__main__':
	SOUNDS['die']=pygame.mixer.Sound('audio/die.wav')
	SOUNDS['hit']=pygame.mixer.Sound('audio/hit.wav')
	SOUNDS['point']=pygame.mixer.Sound('audio/point.wav')
	SOUNDS['wing']=pygame.mixer.Sound('audio/wing.wav')
	SOUNDS['swoosh']=pygame.mixer.Sound('audio/swoosh.wav')
	while True:
		welcomeScreen()
		main_game()
		WIN.blit(game_over,(100,200))
		pygame.display.update()
		time.sleep(1)