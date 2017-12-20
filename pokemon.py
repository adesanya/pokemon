from tkinter import *
import time
import serial
from PIL import ImageTk,Image
from PIL.ImageTk import PhotoImage
import math
import random

class air_glove:
    def __init__(self):
        self.port=''
        self.x=0
        self.y=0
        self.z=0
        self.paired=False
        self.lastCoordinates=''
    

    #step1
    def pair_glove(self):
        self.port= serial.Serial('/dev/cu.wchusbserial1410', 9600)
        #self.port= serial.Serial('/dev/tty.HC-06-DevB', 9600)
        print('connected via USB')
        self.paired=True
      
    def read_position(self):
        if self.paired==True:
            try:
                coordinates=self.port.readline().decode('utf-8')
                x=int(re.search('x:[+,-]*(\d)*',coordinates).group(0).strip('x:'))
                y=int(re.search('y:[+,-]*(\d)*',coordinates).group(0).strip('y:'))
                z=int(re.search('z:[+,-]*(\d)*',coordinates).group(0).strip('z:'))
                coordinates=[x,y,z]
                return coordinates
            except :
                print("crash")
                #return self.lastCoordinates
                return [0,0,0]
        else:
            return [0,0,0]


class Throw:
    def __init__(self):
        self.throwCount=0

    def resetThowCount(self):
        self.throwCount=0

    def incrementthrowcount(self):
        self.throwCount+=1
        
    def can_throw_ball(self):
        if self.throwCount==0:
            return True
        else:
            return False
           
        
        
class air_mouse:
    def __init__(self):
        self.points=0
        self.attempts=0
        self.glove=air_glove()
        #self.glove.pair_glove()
        self.root=Tk()
        self.canvas=Canvas(master=self.root, width=1200,height=750, background='white')
        self.canvas.grid(row=0,column=0)
        self.x=500
        self.y=500
        self.z=0
        self.angle=90
        self.target_pokemon = PhotoImage(file="pikachu.gif")
        self.ball = PhotoImage(file="pokemonball.gif")
        self.score=PhotoImage(file="movingball.gif")
        self.movingball=PhotoImage(file="movingball.gif")
        self.canvas.bind('<Button-1>',self.coordinates)
        self.throw=Throw()
        self.next()

    def coordinates(self,event):
        coord='x:{} y:{}'.format(event.x,event.y)
        print(coord)

    def draw_circle(self,x,y,tag=''):
        radius=50
        self.point=self.canvas.create_oval(x,y,x+radius,y+radius,fill='red', tags=tag)
        self.canvas.create_image(self.x,self.y, anchor=NW, image=self.movingball)
        
    def throw_power(self):
        force=230-self.z
        if force>=230:
            force=force-90
        self.canvas.create_rectangle(1030,30, 1040, 290, fill="yellow",outline="white")
        air_mouse.draw_circle(self,1010,force)
        
    def player_throw(self,x,y):
        if y>=560:
            self.throw. incrementthrowcount()
            return True
        else:
            return False

    def throw_ball(self,x,y,distance=0):

        if y<=40:
            self.throw.resetThowCount()
            if x>=445 and x<=735:
                self.drop_ball(x,y)
            if x>=540 and x<=625 and y<112:
                self.points+=1
        elif y>=40:
            y-=20
            air_mouse.draw_circle(self,x,y,"ball")
            self.root.after(1,self.throw_ball,x,y)

    def drop_ball(self,x,y):
        if y<=285:
            y+=20
            air_mouse.draw_circle(self,x,y,"ball")
            self.root.after(1,self.drop_ball,x,y)
    
            
    def  update_c(self):
        self.canvas.delete(ALL)
        air_mouse.game_stats(self)
        self.throw_power()
        self.canvas.create_image(10,10, anchor=NW, image=self.score)
        self.canvas.create_line(297, 235, 89, 515, fill="black")
        self.canvas.create_line(892, 235, 1084, 518, fill="black")
        self.canvas.create_image(450,7, anchor=NW, image=self.target_pokemon)
        if  self.player_throw(self.x,self.y) and self.throw.throwCount<2:
            self.throw_power()
            self.throw_ball(self.x,self.y,500)
            self.attempts+=1
        self.canvas.create_image(self.x,self.y, anchor=NW, image=self.ball)


    def bounding_box(self,x,y):
         if x<=0:
             x=0
         if x>=1200-50:
             x=1200-50
         if y<=550:
            y=550
         if y>=750-50:
             y=750-50
         return (x,y)

    def glove_control(self):
        coord=self.glove.read_position()
        x=coord[0]+ self.x
        y=coord[1]+ self.y
        x_y_=air_mouse.bounding_box(self,x,y)
        self.x=x_y_[0]
        self.y=x_y_[1]
        self.z=coord[2]
        self.angle=math.degrees(math.atan2(coord[2],coord[1]))
        #print("Angle:",self.angle)

    def game_stats(self):
        score_display='    Shots: {}'.format(self.points)
        self.canvas.create_text(31,130,text=score_display,tags='score')
        attempts_display='    Attempts: {}'.format(self.attempts)
        self.canvas.create_text(40,150,text=attempts_display,tags='attempts')
        
    def next(self):
        air_mouse.glove_control(self)
        air_mouse.update_c(self)
        self.root.after(1,air_mouse.next,self )

if __name__=='__main__':        
    test=air_mouse()
    test.glove.pair_glove()
    test.root.mainloop()
    

