import os
import random
import turtle
from playsound import playsound
import time
import pygame
import pygame.mixer
from distlib.compat import raw_input



# Initialize pygame
pygame.init()
# set the animation speed to the maximum
turtle.speed(0)
#change window title
turtle.title("SpaceWar")
# Change the backgrouund color
turtle.bgcolor("black")
#Change background image
turtle.bgpic('D:/Visual code/CSS_in_one_video_with_notes/Chapter 0/moon.gif')
# Hide the default turtle
turtle.ht()
# This save the memory
turtle.setundobuffer(1)
# this speeds up drawing
turtle.tracer(0.7)
laser = pygame.mixer.Sound('D:/Visual code/CSS_in_one_video_with_notes/Chapter 0/laser.mp3')
explosion = pygame.mixer.Sound('D:/Visual code/CSS_in_one_video_with_notes/Chapter 0/explosion.mp3')

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, straty):
        turtle.Turtle.__init__(self, shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        # self.fd(0)
        self.goto(startx, straty)
        self.move_distance = 1
        self.speed_value = 1 #add a speed value attribute

    def move(self):
        self.fd(self.speed_value) #use the speed value attribute

        #Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)
    
    def is_collision(self, other):
        if (self.xcor() >= (other.xcor() - 20)) and \
        (self.xcor() <= (other.xcor() + 20)) and \
        (self.ycor() <= (other.ycor() + 20)) and \
        (self.ycor() >= (other.ycor() - 20)):
            return True
        else:
            return False
        
class Player(Sprite):
    def __init__(self, spriteshape, color, startx, straty):
        Sprite.__init__(self, spriteshape, color, startx, straty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed_value = 4
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed_value += 1

    def deaccelerate(self):
        self.speed_value -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, straty):
        Sprite.__init__(self, spriteshape, color, startx, straty)
        self.speed_value = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, straty):
        Sprite.__init__(self, spriteshape, color, startx, straty)
        self.speed_value = 8
        self.setheading(random.randint(0, 360))

    def move(self):
        # self.fd(self.move_distance)
        # self.fd(self.speed())
        self.fd(self.speed_value) #use the speed value attribute

        #Boundary detection
        if self.xcor() > 290:
            self.setx(290)
            self.lt(60)
        
        if self.xcor() < -290:
            self.setx(-290)
            self.lt(60)
        
        if self.ycor() > 290:
            self.sety(290)
            self.lt(60)
        
        if self.ycor() < -290:
            self.sety(-290)
            self.lt(60)
        
        
class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, straty):
        Sprite.__init__(self, spriteshape, color, startx, straty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed_value = 20
        self.status = "ready"
        self.goto(-1000, 1000)


    def fire(self):
        if self.status == "ready":
            #play missile sound
            laser.play()
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"
        
    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
             
        if self.status == "firing":
            self.fd(self.speed_value)

        #Border check 
        if self.xcor() < -290 or self.xcor() > 290 or \
            self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, straty):
        Sprite.__init__(self, spriteshape, color, startx, straty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000,-1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0,360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1

        if self.frame > 20:
            self.frame = 0
            self.goto(-1000, -1000)

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state= "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
    def draw_border(self):
        #Draw border
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300) 
        self.pen.pendown()
        for side in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()

    def show_status(self):
        self.pen.undo()
        msg = "Score: %s" %(self.score)
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.write(msg, font=("Arial", 16, "normal"))


#create the game object
game=Game()

#Draw the game border
game.draw_border()

#Show the game status
game.show_status()

# Create my sprites
player = Player("triangle", "white", 0, 0)
# enemy = Enemy("circle","red", -100, 0)
missile = Missile("triangle", "yellow", 0,0)
# ally = Ally("square", "blue", 0, 0)

enemies = []
for i in range(6):
    enemies.append(Enemy("circle","red", -100, 0))
allies = []
for i in range(6):
    allies.append(Ally("star", "blue", 0, 0))

particles = []
for i in range(20):
    particles.append(Particle("circle","orange", 0, 0))

#keyboard binding
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.deaccelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# main game loop
while True:
    turtle.update()
    time.sleep(0.02)
    player.move()
    # enemy.move()
    missile.move()
    # ally.move()

    for enemy in enemies:
        enemy.move()

        #Check foe a collision with the player
        if player.is_collision(enemy):
            #play explosion sound
            explosion.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()

        #Check for a collision between the missile and the enemy
        if missile.is_collision(enemy):
            #play explosion sound
            explosion.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            #Increase the score
            game.score += 100
            game.show_status()
            #do the explosion
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())

    for ally in allies:
        ally.move()

        #Check for a collision between the missile and the ally
        if missile.is_collision(ally):
            explosion.play()
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            #Decrease the score
            game.score -= 50
            game.show_status()

    for particle in particles:
        particle.move()


delay = raw_input("Press enter to finish. >")