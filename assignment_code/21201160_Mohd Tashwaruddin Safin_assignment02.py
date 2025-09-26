from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import random

width, height = 600, 700
catcher_pos = [300, 50]
catcher_width, catcher_height = 40, 15
diamond_pos = [random.randint(100, 500), 650]
diamond_speed = 100
diamond_size = 10
diamond_color = [1.0, 1.0, 0.0]
score = 0
paused = False
game_over = False
last_time = time.time()

buttons = {
    'restart' : {'x':30, 'y':640, 'w':40, 'h':40},
    'pause' : {'x':280, 'y':640, 'w':40, 'h':40},
    'exit' : {'x':530, 'y':640, 'w':40, 'h':40}
}

def zoneFind(x1, y1, x2, y2):
    zone = None
    dx = x2 - x1
    dy = y2 - y1
    if(abs(dx) >= abs(dy)):
        if(dx >= 0 and dy >= 0):
            zone = 0
        elif(dx >= 0 and dy < 0):
            zone = 7
        elif(dx < 0 and dy >= 0):
            zone = 3
        elif(dx < 0 and dy < 0):
            zone = 4
    else:
        if(dx >= 0 and dy >= 0):
            zone = 1
        elif(dx >= 0 and dy < 0):
            zone = 6
        elif(dx < 0 and dy >= 0):
            zone = 2
        elif(dx < 0 and dy < 0):
            zone = 5
    return zone

def convertToZone0(x, y, zone):
    xp, yp = 0, 0
    if(zone == 0):
        xp, yp = x, y
    elif(zone == 1):
        xp, yp = y, x
    elif(zone == 2):
        xp, yp = y, -x
    elif(zone == 3):
        xp, yp = -x, y
    elif(zone == 4):
        xp, yp = -x, -y
    elif(zone == 5):
        xp, yp = -y, -x
    elif(zone == 6):
        xp, yp = -y, x
    elif(zone == 7):
        xp, yp = x, -y
        
    return xp, yp

def convertFromZone0(x, y, zone):
    xp, yp = 0, 0
    if(zone == 0):
        xp, yp = x, y
    elif(zone == 1):
        xp, yp = y, x
    elif(zone == 2):
        xp, yp = -y, x
    elif(zone == 3):
        xp, yp = -x, y
    elif(zone == 4):
        xp, yp = -x, -y
    elif(zone == 5):
        xp, yp = -y, -x
    elif(zone == 6):
        xp, yp = y, -x
    elif(zone == 7):
        xp, yp = x, -y
        
    return xp, yp

def pixelDraw(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def drawLine(x1, y1, x2, y2):
    if(x1 > x2 and y1 > y2):
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    zone = zoneFind(x1, y1, x2, y2)
    x3, y3 = convertToZone0(x1, y1, zone)
    x4, y4 = convertToZone0(x2, y2, zone)
    
    dy = y4 - y3
    dx = x4 - x3
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    dinit = 2 * dy - dx
    
    x, y = x3, y3
    while(x <= x4):
        px, py = convertFromZone0(x, y, zone)
        pixelDraw(px, py)
        
        if(dinit > 0):
            y += 1
            dinit += dNE
        else:
            dinit += dE
        x += 1
        
def diamondDraw(x, y, size):
    drawLine(x, y+size, x+size, y)
    drawLine(x+size, y, x, y-size)
    drawLine(x, y-size, x-size, y)
    drawLine(x-size, y, x, y+size)
    
def catcherDraw(x, y, w, h):
    drawLine(x-w, y+h, x+w, y+h)  #top
    drawLine(x-w, y+h, x-w//2, y) #left
    drawLine(x+w, y+h, x+w//2, y) #right
    drawLine(x-w//2, y, x+w//2, y) #bottom
    
    
def triangleDraw(x, y, dir):
    if(dir == 'left'): #restart
        drawLine(x+30, y+5, x+10, y+20)
        drawLine(x+10, y+20, x+50, y+20)
        drawLine(x+10, y+20, x+30, y+35)
    elif(dir == 'right'): #play icon
        drawLine(x+10, y+10, x+30, y+20)
        drawLine(x+30, y+20, x+10, y+30)
        drawLine(x+10, y+30, x+10, y+10)
    elif(dir == 'pause'): #pause icon
        drawLine(x+10, y+10, x+10, y+30)
        drawLine(x+20, y+10, x+20, y+30)
    elif(dir == 'cross'): #exit
        drawLine(x+10, y+10, x+30, y+30)
        drawLine(x+30, y+10, x+10, y+30)
        
def buttonDraw():
    glColor3f(0.0, 1.0, 1.0)
    triangleDraw(buttons['restart']['x'], buttons['restart']['y'], 'left')
    glColor3f(1.0, 1.0, 0.0)
    if(paused):
        triangleDraw(buttons['pause']['x'], buttons['pause']['y'], 'right') # play shape
    else:
        triangleDraw(buttons['pause']['x'], buttons['pause']['y'], 'pause') # pause shape
    glColor3f(1.0, 0.0, 0.0)
    triangleDraw(buttons['exit']['x'], buttons['exit']['y'], 'cross')
    
def mouseClick(button, state, x, y):
    global paused, game_over, diamond_color, score, diamond_pos, catcher_pos, last_time, diamond_speed
    if(state != GLUT_DOWN):
        return
    
    y = height - y
    for name, b in buttons.items():
        if(b["x"] <= x <= (b["x"] + b["w"]) and b["y"] <= y <= (b["y"] + b["h"])):
            if(name == 'restart'):
                print('Starting Over')
                score = 0
                game_over = False
                paused = False
                diamond_speed = 100
                catcher_pos = [300, 50]
                diamond_color = [1.0, 1.0, 0.0]
                diamond_pos = [random.randint(100, 500), 650]
                last_time = time.time()
            elif(name == 'pause'):
                paused = not paused
                if(paused):
                    print('Paused')
                else:
                    print('Resume')
            elif(name == 'exit'):
                print(f"Goodbye! Final Score: {score}")
                glutLeaveMainLoop()
    glutPostRedisplay()
                
def special_input(key, x, y):
    if(game_over or paused):
        return
    if(key == GLUT_KEY_LEFT):
        catcher_pos[0] = max(catcher_width, catcher_pos[0]-20)
    elif(key == GLUT_KEY_RIGHT):
        catcher_pos[0] = min(width-catcher_width, catcher_pos[0]+20)
        
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    if(not game_over):
        glColor3f(1.0, 1.0, 1.0)
        catcherDraw(catcher_pos[0], catcher_pos[1], catcher_width, catcher_height)
        glColor3f(*diamond_color)
        diamondDraw(diamond_pos[0], diamond_pos[1], diamond_size)
    else:
        glColor3f(1.0, 0.0, 0.0)
        catcherDraw(catcher_pos[0], catcher_pos[1], catcher_width, catcher_height)
        
    buttonDraw()
    glutSwapBuffers()
    
def update():
    global diamond_color, diamond_pos, last_time, score, game_over, diamond_speed
    if(paused or game_over):
        return 
    
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    diamond_pos[1] -= diamond_speed * dt
    
    # collision logic
    if(catcher_pos[0] - catcher_width < diamond_pos[0] < catcher_pos[0] + catcher_width and catcher_pos[1] - catcher_height < diamond_pos[1] < catcher_pos[1] + catcher_height):
        score += 1
        print(f"Score: {score}, Speed: {diamond_speed: .2f}")
        diamond_pos = [random.randint(100, 500), 650]
        diamond_speed += 10
        diamond_color = [random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0)]
    
    if(diamond_pos[1] < 0):
        game_over = True
        print(f"Game Over!! Final Score: {score}")
        
    glutPostRedisplay()
    
    
def init():
    glClearColor(0, 0, 0, 1)
    glPointSize(2)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Catch the Diamonds")
init()
glutDisplayFunc(display)
glutSpecialFunc(special_input)
glutMouseFunc(mouseClick)
glutIdleFunc(update)
glutMainLoop()