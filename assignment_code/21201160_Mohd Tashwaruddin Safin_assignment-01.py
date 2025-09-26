# Task - 01
# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random

# rain_drops = []
# rain_speed = 0.01
# rain_angle = 0.0
# bg_color = [0.0, 0.0, 0.0]
# day_step = 0.02

# def initialize_rain():
#     global rain_drops
#     rain_drops = [[random.uniform(-1, 1), random.uniform(0, 1)] for _ in range(100)]
    
# def ground_draw():
#     glColor3f(0.55, 0.27, 0.07)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(-1.0, -1.0)
#     glVertex2f(1.0, -1.0)
#     glVertex2f(1.0, 0.35)
    
#     glVertex2f(-1.0, -1.0)
#     glVertex2f(-1.0, 0.35)
#     glVertex2f(1.0, 0.35)
#     glEnd()
    
# def trees_draw():
#     glColor3f(0.0, 1.0, 0.0)
#     x = -1.0
#     while x < 1.0:
#         glBegin(GL_TRIANGLES)
#         glVertex2f(x, 0.1)
#         glVertex2f(x+0.05, 0.3)
#         glVertex2f(x+0.1, 0.1)
#         glEnd()
#         x += 0.1
    
# def draw_house():
#     glColor3f(1.0, 1.0, 1.0)
    
#     glBegin(GL_TRIANGLES) #house body
#     glVertex2f(-0.4, -0.5)
#     glVertex2f(0.4, -0.5)
#     glVertex2f(0.4, 0.0)
    
#     glVertex2f(-0.4, -0.5)
#     glVertex2f(-0.4, 0.0)
#     glVertex2f(0.4, 0.0)
#     glEnd()
    
    
#     glColor3f(0.2, 0.4, 1.0)
#     glBegin(GL_TRIANGLES) #door
#     glVertex2f(-0.05, -0.5)
#     glVertex2f(0.05, -0.5)
#     glVertex2f(0.05, -0.2)
    
#     glVertex2f(-0.05, -0.5)
#     glVertex2f(-0.05, -0.2)
#     glVertex2f(0.05, -0.2)
#     glEnd()
    
#     glColor3f(0.0, 0.0, 0.0)
#     glBegin(GL_POINTS) #door knob
#     glVertex2f(0.03, -0.35)
#     glEnd()
    
#     def window_draw(x, y):
#         glColor3f(0.2, 0.4, 1.0)
#         glBegin(GL_TRIANGLES)
#         glVertex2f(x-0.1, y-0.05)
#         glVertex2f(x+0.1, y-0.05)
#         glVertex2f(x+0.1, y+0.05)
        
#         glVertex2f(x-0.1, y-0.05)
#         glVertex2f(x-0.1, y+0.05)
#         glVertex2f(x+0.1, y+0.05)
#         glEnd()
        
#         glColor3f(0.0, 0.0, 0.0)
#         glBegin(GL_LINES)
#         glVertex2f(x-0.1, y)
#         glVertex2f(x+0.1, y)
#         glVertex2f(x, y-0.05)
#         glVertex2f(x, y+0.05)
#         glEnd()
        
#     window_draw(-0.25, -0.15)
#     window_draw(0.25, -0.15)
    
#     glColor3f(0.5, 0.0, 0.5)
#     glBegin(GL_TRIANGLES) #roof
#     glVertex2f(-0.45, 0.0)
#     glVertex2f(0.45, 0.0)
#     glVertex2f(0.0, 0.3)
#     glEnd()
    
# def rain_draw():
#     glColor3f(0.4, 0.6, 1.0)
#     glBegin(GL_LINES)
#     for drop in rain_drops:
#         x, y = drop
#         glVertex2f(x, y)
#         glVertex2f(x+rain_angle*0.1, y-0.1)
#     glEnd()

# def rain_update():
#     global rain_drops
#     for drop in rain_drops:
#         drop[0] += rain_speed * rain_angle
#         drop[1] -= rain_speed
#         if(drop[1] < -1.0):
#             drop[1] = random.uniform(1.0, 1.5)
#             drop[0] = random.uniform(-1.0, 1.0)


# def background_change(night_to_day):
#     global bg_color
#     for i in range(3):
#         if(night_to_day):
#             bg_color[i] = min(1.0, bg_color[i] + day_step)
#         else:
#             bg_color[i] = max(0.0, bg_color[i] - day_step)
            
# def display():
#     glClearColor(*bg_color, 1.0)
#     glClear(GL_COLOR_BUFFER_BIT)
#     ground_draw()
#     trees_draw()
#     draw_house()
#     rain_draw()
#     glutSwapBuffers()
    
# def timer(value):
#     rain_update()
#     glutPostRedisplay()
#     glutTimerFunc(16, timer, 0)

# def keyboard(key, x, y):
#     global bg_color
#     if(key == b'd'):
#         background_change(True)
#     elif(key == b'n'):
#         background_change(False)
        
# def special_input(key, x, y):
#     global rain_angle
#     if(key == GLUT_KEY_LEFT):
#         rain_angle -= 0.01
#     elif(key == GLUT_KEY_RIGHT):
#         rain_angle += 0.01 

# glutInit()
# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# glutInitWindowSize(800, 800)
# glutCreateWindow(b"House With RainFall")
# glutDisplayFunc(display)
# glutTimerFunc(0, timer, 0)
# glutKeyboardFunc(keyboard)
# glutSpecialFunc(special_input)
# glPointSize(5.0)
# initialize_rain()
# glutMainLoop()



#Task - 02
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.color = [random.random(), random.random(), random.random()]
        self.speed = 0.01
        self.visible = True
        self.last_blink = time.time()
        

points = []
blinking = False
frozen = False
width, height = 800, 600

def draw_points():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    for point in points:
        if(not frozen):
            point.x += point.dx * point.speed
            point.y += point.dy * point.speed
            
            if(point.x > 1 or point.x < -1):
                point.dx *= -1
            if(point.y > 1 or point.y < -1):
                point.dy *= -1
                
        if(blinking and not frozen):
            current = time.time()
            if(current - point.last_blink >= 0.5):
                point.visible = not point.visible
                point.last_blink = current
        else:
            point.visible = True
            
            
        if(point.visible):
            glColor3f(*point.color)
            glBegin(GL_POINTS)
            glVertex2f(point.x, point.y)
            glEnd()
            
    glutSwapBuffers()
    
    
def update(value):
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)
    

def mouse(button, state, x, y):
    global blinking
    
    if(state != GLUT_DOWN):
        return 
    
    
    gl_x = (x / width) * 2 - 1
    gl_y = - ((y / height) * 2 - 1)
    
    if(button == GLUT_RIGHT_BUTTON):
        points.append(Point(gl_x, gl_y))
        
    elif(button == GLUT_LEFT_BUTTON):
        blinking = not blinking
        
    
def keyboard(key, x, y):
    global frozen
    
    if(key == b' '):
        frozen = not frozen
        
def special_keys(key, x, y):
    for point in points:
        if(key == GLUT_KEY_UP):
            point.speed += 0.01
        elif(key == GLUT_KEY_DOWN):
            point.speed = max(0.01, point.speed - 0.005)
            

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(5.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1, 1, -1, 1)
    
    
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Point Animation")
init()
glutDisplayFunc(draw_points)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(0, update, 0)
glutMainLoop()