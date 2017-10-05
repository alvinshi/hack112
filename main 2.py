####################################\
# player 1
import math
import string
import copy
import random
from tkinter import *

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

class Weapon(object):
    def __init__(self):
        n=random.randint(0,2)
        weaponType=['pine','torch','pinetorch']
        attackPoint={'pine':1,'torch':2,'pinetorch':4}
        attackMass={'pine':15,'torch':17,'pinetorch':17}
        self.type=weaponType[n]
        self.x=100
        self.y=200
        self.mass=attackMass[self.type]
        self.atkPoint=attackPoint[self.type]
        self.speedX=None
        self.speedY=None
        
    def checkOut(self,data):
        if self.y>=data.height or self.x>=data.width or self.x<=0:
            return True
        return False
    def hold(self,x,y):
        if x>=self.x-25 and x<self.x+25 and y>=self.y-30 and y<=self.y+30:
            return True
        return False

    def drawWeapon(self,canvas, data):
        canvas.create_image(self.x,self.y,image = data.photo[self.type][data.rota])


    def getInitSpeed(self,force,origX,origY,releaseX,releaseY):
        acceler=force//self.mass*10
        if origX!=releaseX:
            angle=math.atan((releaseY-origY)/abs(releaseX-origX))
        else:
            angle=math.pi/2
        initSpeed=acceler
        self.speedX=initSpeed*math.cos(angle)
        self.speedY=initSpeed*math.cos(angle)
        if releaseY<origY:
            self.speedY=(-1)*self.speedY

    def moveInAir(self):
        self.x+=self.speedX
        tempSpeedY=self.speedY
        self.speedY-=10
        self.y-=tempSpeedY+0.5*10

####################################
# player 2
class Grid(object):
    # take in the width and height of the canvas
    def __init__(self, w, h):
        # x and y are the top left corner of the grid
        self.x = w * 3 // 4
        self.y = h // 6
        self.rows = 8
        self.cols = 4
        self.w = w - self.x - 30
        self.h = h - self.y
        self.bricks = [[0] * self.cols for i in range(self.rows)]
        self.cellw = self.w // self.cols
        self.cellh = self.h // self.rows
        # self.brickType = [None, "iceBrick", "woodBrick", "brick", "ironBrick"]
        self.brick_falling = False
        self.won = False

    def get_brick(self):
        return random.randint(1, 4)

    def clicked(self, x, y):
        if (x < self.x or x > self.x + self.w or y < self.y or y > self.y + self.h):
            return False
        row = int((y - self.y) // self.cellh)
        col = int((x - self.x) // self.cellw)
        if (self.bricks[row][col] != 0 or 
            (row < self.rows - 1 and self.bricks[row + 1][col] == 0)): return False
        self.bricks[row][col] = self.get_brick()
        if (row == 0): self.won = True
        return True 

    def brick_collide(self, x, y, w, h, r, c):
        x1, y1 = self.brick_pos(r, c)
        w1, h1 = self.cellw, self.cellh
        if (x <= x1 + w1 and x + w >= x1 and y <= y1 + h1 and y + h >= y1):
            return True
        return False
 
    def collide(self, weapon):
        # determine whether the weapon hits the bricks and
        # then eliminate the bricks hit
        attack = weapon.atkPoint
        for r in range(self.rows):
            for c in range(self.cols):
                if (self.brick_collide(weapon.x, weapon.y, 40, 40, r, c)):
                    if (self.bricks[r][c] == 0): return False
                    elif (self.bricks[r][c] - attack <= 0):
                        self.make_brick_fall(r, c)
                        self.break_brick(r, c)
                    else: self.bricks[r][c] -= attack
                    return True
        return False

    def make_brick_fall(self, row, col):
        self.brick_falling = True
        bricks = []
        for r in range(row - 1, -1, -1):
            if (self.bricks[r][col] > 0): 
                bricks = [self.bricks[r][col]] + bricks
                self.falling_bricks_r = r
        self.falling_bricks_c = col
        self.falling_bricks = bricks
        self.falling_counts = 0

    def break_brick(self, row, col):
        # delete the hit brick and those above it
        for r in range(row, -1, -1):
          self.bricks[r][col] = 0

    # need to be called in timerfired
    def update(self):
        # move the falling bricks if necessary
        if (self.brick_falling and self.falling_counts == 3):
            self.return_bricks()
            self.brick_falling = False
        if (self.brick_falling):
            self.falling_counts += 1
        # for c in range(self.cols):
        #     r = self.col_needs_update(col)
        #     # r is the row number of the top brick that needs to drop down
        #     if (r != None): 
        #         self.bricks[r][c] = 0
        #         for i in range(r + 1, self.rows):
        #             self.bricks[i][c] = 1;

    def return_bricks(self):
        n = len(self.falling_bricks)
        i = 0
        for r in range(self.falling_bricks_r + 1, self.falling_bricks_r + n + 1):
            self.bricks[r][self.falling_bricks_c] = self.falling_bricks[i]
            i += 1

    def col_needs_update(self, col):
        top = False
        for row in range(self.rows):
            if ((not top) and self.bricks[row][col] == 1):
              x = row
              top = True
            elif (top and self.bricks[row][col] == 0):
              return x
        return None

    def brick_pos(self, r, c):
        x1 = self.x + self.cellw * c
        y1 = self.y + self.cellh * r
        return x1, y1

    # def draw(self, canvas, data):
    #     if (self.brick_falling):
    #         for i in range(len(self.falling_bricks)):
    #             a, b = self.brick_pos(self.falling_bricks_r + i, self.falling_bricks_c)
    #             b += self.falling_counts * (self.cellh // 3)
    #             if self.brickType[self.falling_bricks[i]]!=None:
    #                 canvas.create_image(a, b, anchor=NW, image=data.photo[self.brickType[self.falling_bricks[i]]])
    #             else:canvas.create_rectangle(x1, y1, x1 + self.cellw, y1 + self.cellh)
    #     for r in range(self.rows):
    #         for c in range(self.cols):
    #             x1, y1 = self.brick_pos(r, c)
    #             if self.brickType[self.bricks[r][c]]!=None:
    #                 canvas.create_image(x1, y1, anchor=NW, image=data.photo[self.brickType[self.bricks[r][c]]])
    #             else:canvas.create_rectangle(x1, y1, x1 + self.cellw, y1 + self.cellh)
        
####################################
# customize these functions
####################################
def initLoading(data):
    data.photo["loading"] = PhotoImage(file = "loading.gif")
    data.timerDelay = 10
    data.timer = 3
    
def initGame(data):
    data.timerDelay = 100
    data.currentPlayer = 'player1'
    data.rota=0
    data.weaponSelected = 'pine'
    data.hasWeapon = True
    data.player1 = Weapon()
    initGamePhoto(data)
    data.launch  = False
    data.hold = False
    data.flying = False
    data.p = False

    data.player2 = Grid(data.width, data.height)

# def initGamePhoto(data):
#     data.photo["pine"]=[PhotoImage(file="oie_DfHiFP65R6Le_3_.gif"),PhotoImage(file="pine1.gif"),
#                         PhotoImage(file="pine2.gif"),PhotoImage(file="pine3.gif")]
#     data.photo["torch"]=[PhotoImage(file='oie_07HQDZLOOBc2.gif'),PhotoImage(file='torch1.gif'),
#                             PhotoImage(file='torch2.gif'),PhotoImage(file='torch3.gif')]
#     data.photo["pinetorch"]=[PhotoImage(file='oie_trans.gif'),PhotoImage(file='oie_trans1.gif'),
#                             PhotoImage(file='oie_trans2.gif'),PhotoImage(file='oie_trans3.gif')]
#     data.photo['iceBrick']=PhotoImage(file='icebrick.gif')
#     data.photo['woodBrick']=PhotoImage(file='woodbrick.gif')
#     data.photo['brick']=PhotoImage(file='brick.gif')
#     data.photo['ironBrick']=PhotoImage(file='ironbrick.gif')

def init(data):
    data.pause = False
    data.mode = 'welcome'
    data.timerDelay = 100
    data.photo = {}

#####################################
def mousePressedPlayer1(event, data):
    if data.hold == False:
        if data.player1.hold(event.x, event.y)==True:
            data.hold = True
    elif data.hold == True:
        data.tempx=data.player1.x
        data.tempy=data.player1.y
        data.player1.x = event.x
        data.player1.y = event.y
        data.force=((data.tempx-data.player1.x)**2+(data.tempy-data.player1.y)**2)**0.5
        data.launch = True
        data.hold=False

def mousePressedPlayer2(event, data):
    if data.player2.clicked(event.x, event.y):
        data.currentPlayer = 'player1'
        
    
def mousePressedGame(event, data):
    if data.currentPlayer == 'player1':
        mousePressedPlayer1(event, data)
    else:
        mousePressedPlayer2(event, data)

def mousePressed(event, data):
    if data.mode == 'welcome':
        pass
        #mousePressedWelcome(event, data)
    elif data.mode == 'game':
        mousePressedGame(event, data)
    elif data.mode == 'end':
        mousePressedEnd(event, data)

#####################################
def keyPressedGame(event, data):
    if event.char == "l":
        print(data.player2.bricks)
    if event.char == "p":
        data.p = True
        
def keyPressedWelcome(event, data):
    if event.char == "s":
        initGame(data)
        data.mode = 'game'
    else:
        initLoading(data)
        data.mode = 'loading'

def keyPressed(event, data):
    if data.mode == 'welcome':
        keyPressedWelcome(event, data)
    elif data.mode == 'game':
        keyPressedGame(event, data)

#####################################
def timerFiredLoading(data):
    data.timer -= 0.01
    if data.timer <= 0:
        initGame(data)
        data.mode = "game"

# def timerFiredGame(data):
#     if data.currentPlayer == 'player2':
#         data.player2.update()
#     elif data.currentPlayer == 'player1':
#         if data.player1==None:
#             data.player1=Weapon()
#         else:
#             if data.player1.checkOut(data)==True:
#                 data.player1=None
#                 data.flying=False
#                 data.currentPlayer = "player2"
#                 data.rota=0
#             if data.launch==True:
#                 data.player1.getInitSpeed(data.force,data.tempx,data.tempy,data.player1.x,data.player1.y)
#                 data.launch=False
#                 data.flying=True
#             if data.flying==True:
#                 data.player1.moveInAir()
#                 data.rota+=1
#                 if data.rota>3:
#                     data.rota=0
#                 if data.player2.collide(data.player1):
#                     data.player1 = None
#                     data.flying=False
#                     data.currentPlayer = "player2"
#                     data.rota=0
        
def timerFired(data):
    if data.mode == 'game':
        timerFiredGame(data)
    elif data.mode == 'loading':
        timerFiredLoading(data)

#####################################
def redrawWelcome(canvas, data):
    data.photo["welcome_background"] = PhotoImage(file = "poster.gif")
    canvas.create_rectangle(0,0,640,320,fill = rgbString(155, 183, 194), width = 0)
    canvas.create_image(200,0,anchor=NW,image=data.photo["welcome_background"])
    canvas.create_text(data.width//2, data.height - 23, text = "Press any key to Start",font = "YuppySC 15", fill = "White")
    canvas.create_text(data.width//2, data.height - 24, text = "Press any key to Start",font = "YuppySC 15", fill = "Black")

def redrawLoading(canvas,data):
    canvas.create_rectangle(0,0, 640, 320, fill = rgbString(21, 88, 141), width = 0)
    canvas.create_image(0,data.timer*400/3-400,anchor = NW, image=data.photo["loading"])
    canvas.create_text(data.width//2, data.height -53, text = "L O A D I N G . . .", font = "Impact 25", fill = "Black")
    canvas.create_text(data.width//2, data.height -55, text = "L O A D I N G . . .", font = "Impact 25", fill = "White")
    
    
def redrawGame(canvas, data):
    data.player2.draw(canvas, data)
    if data.player1!=None:
        data.player1.drawWeapon(canvas, data)
        
def redrawAll(canvas, data):
    if data.mode == 'welcome':
        redrawWelcome(canvas, data)
    elif data.mode == 'loading':
        redrawLoading(canvas, data)
    elif data.mode == 'game':
        redrawGame(canvas, data)
    elif data.mode == 'end':
        redrawEnd(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=640, height=360):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(640, 320)
