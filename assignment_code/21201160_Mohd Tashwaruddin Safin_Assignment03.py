from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
# player and game info
life = 5
score = 0
bullet_miss = 0

enemy_scale = 2
enemy_size_control = 1
enemy_position = []
enemy_speed = 0.5

player_pos = [0, 0]
move_step = 10
player_angle = 90
turn_step = 10
player_dead = False
player_fall_angle = 0
player_falling = False

bullets = []
bullet_speed = 25
bullet_radius = 7

camera_radius = 700
camera_angle = 45
camera_height = 500
first_person_mode = False

cheat_mode = False
cheat_auto_camera = False
cheat_cooldown = 0
cheat_fire_interval = 10
cheat_spin_speed = 2

game_over = False
paused = False

def restart_game():
    global life, score, bullet_miss, game_over
    global player_dead, player_falling, player_fall_angle
    global player_pos, player_angle, bullets, enemy_scale, enemy_size_control
    global cheat_mode, cheat_auto_camera, cheat_cooldown
    global first_person_mode, enemy_position, camera_angle, camera_height, camera_radius

    game_over = False
    player_dead = False
    player_falling = False
    player_fall_angle = 0

    life = 5
    score = 0
    bullet_miss = 0

    player_pos = [0, 0]
    player_angle = 90
    bullets = []

    enemy_scale = 1.0
    enemy_size_control = 1
    enemy_position = []
    create_enemies()

    cheat_mode = False
    cheat_auto_camera = False
    cheat_cooldown = 0
    first_person_mode = False

    camera_radius = 700
    camera_angle = 45
    camera_height = 500

    glutPostRedisplay()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def create_enemies():
    global enemy_position
    enemy_position = []

    for i in range(5):
        x = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        y = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        enemy_position.append((x, y))

def update_enemies():
    global enemy_position, player_pos

    new_positions = []
    for (ex, ey) in enemy_position:
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.sqrt(dx*dx + dy*dy) + 1e-5
        ex += (dx/dist) * enemy_speed
        ey += (dy/dist) * enemy_speed
        new_positions.append((ex, ey))
    enemy_position = new_positions

def bullet_hits_enemy():
    global bullets, enemy_position, score

    new_bullets = []
    new_enemies = []

    for (ex, ey) in enemy_position:
        hit = False
        for b in bullets:
            bx, by, bz, dx, dy = b
            dist = math.sqrt((bx-ex)**2 + (by-ey)**2)
            if dist < 35:  # enemy radius + bullet radius
                hit = True
                score += 1
                break
        if not hit:
            new_enemies.append((ex, ey))

    # remove used bullets
    for b in bullets:
        bx, by, bz, dx, dy = b
        keep = True
        for (ex, ey) in enemy_position:
            dist = math.sqrt((bx-ex)**2 + (by-ey)**2)
            if dist < 35:
                keep = False
                break
        if keep:
            new_bullets.append(b)

    bullets = new_bullets
    enemy_position[:] = new_enemies

    while len(enemy_position) < 5:
        x = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        y = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        enemy_position.append((x, y))

def draw_enemy(x, y):
    global enemy_scale

    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(x, y, 20)
    glScalef(enemy_scale, enemy_scale, enemy_scale)

    # Body
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(0, 0, 60)
    gluSphere(quad, 30, 32, 32)
    glPopMatrix()

    # Head
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0) 
    glTranslatef(0, 0, 95)
    gluSphere(quad, 16, 32, 32)
    glPopMatrix()

    glPopMatrix()


def draw_shapes():
    #draw the player
    quad = gluNewQuadric()
    glPushMatrix()
    glTranslatef(0, 0, 20)

    # Head
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 136)
    gluSphere(quad, 16, 32, 32)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(0.33, 0.42, 0.18)
    glTranslatef(0, 0, 80)
    glScalef(1.5, 0.7, 2.0)
    glutSolidCube(40)
    glPopMatrix()

    # Hands
    glColor3f(1.0, 0.8, 0.6)  # skin color

    # Left hand
    glPushMatrix()
    glTranslatef(-15, 5, 110)
    glRotatef(-90, 1, 0, 0)   # rotate so cylinder points outward
    gluCylinder(quad, 8, 5, 30, 16, 16)
    glPopMatrix()

    # Right hand
    glPushMatrix()
    glTranslatef(15, 5, 110)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 8, 5, 30, 16, 16)
    glPopMatrix()

    # Legs
    glColor3f(0.5, 0.0, 0.5) 

    # Left leg
    glPushMatrix()
    glTranslatef(-15, 0, 45)
    glRotatef(180, 1, 0, 0)
    gluCylinder(quad, 7, 7, 40, 16, 16)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(15, 0, 45)
    glRotatef(180, 1, 0, 0)
    gluCylinder(quad, 7, 7, 40, 16, 16)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glColor3f(0.75, 0.75, 0.75) 
    glTranslatef(0, 5, 110)   # in between hands
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 4, 4, 60, 16, 16)
    glPopMatrix()

    glPopMatrix()

def enemy_player_collision():
    global player_falling, life, enemy_position, player_pos, player_dead, game_over
    
    if(game_over):
        return

    new_positions = []
    for (ex, ey) in enemy_position:
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 50:  # enemy touches player
            life -= 1
            print(f"Remaining Life of the player: {life}")
            if(life <= 0 and not player_falling and not player_dead):
                game_over = True
                player_falling = True
        else:
            new_positions.append((ex, ey))

    if(bullet_miss >= 10):
        game_over = True
    enemy_position = new_positions
    while len(enemy_position) < 5:
        x = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        y = random.randint(-GRID_LENGTH+80, GRID_LENGTH-80)
        enemy_position.append((x, y))


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global player_pos, player_angle, game_over, paused

    # # Reset the game if R key is pressed
    if key == b'r':
        restart_game()

    if key == b'p':
        paused = not paused
        if(paused):
            print("Game Paused")
        else:
            print("Game Resumed")

    if(game_over):
        return

    # # Move forward (W key)
    if key == b'w': 
        player_pos[0] += move_step * math.cos(math.radians(player_angle))
        player_pos[1] += move_step * math.sin(math.radians(player_angle))

    # # Move backward (S key)
    elif key == b's':
        player_pos[0] -= move_step * math.cos(math.radians(player_angle))
        player_pos[1] -= move_step * math.sin(math.radians(player_angle))

    # # Rotate gun left (A key)
    elif key == b'a':
        player_angle += turn_step

    # # Rotate gun right (D key)
    elif key == b'd':
        player_angle -= turn_step

    # # Toggle cheat mode (C key)
    elif key == b'c':
        global cheat_mode
        cheat_mode = not cheat_mode

    # # Toggle cheat vision (V key)
    elif key == b'v':
        global cheat_auto_camera
        cheat_auto_camera = not cheat_auto_camera


    player_pos[0] = max(-GRID_LENGTH+50, min(GRID_LENGTH-50, player_pos[0]))
    player_pos[1] = max(-GRID_LENGTH+50, min(GRID_LENGTH-50, player_pos[1]))


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_radius, camera_angle, camera_height
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        camera_height += 10

    # # Move camera down (DOWN arrow key)
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10

    # moving camera left (LEFT arrow key)
    elif key == GLUT_KEY_LEFT:
        camera_angle += 2.5  # Small angle decrement for smooth movement

    # moving camera right (RIGHT arrow key)
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 2.5  # Small angle increment for smooth movement



def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    global bullets, player_pos, player_angle, first_person_mode
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gun_offset = 65
        gun_height = 130

        dx = math.cos(math.radians(player_angle))
        dy = math.sin(math.radians(player_angle))

        bx = player_pos[0] + dx * gun_offset
        by = player_pos[1] + dy * gun_offset
        bz = gun_height

        bullets.append([bx, by, bz, dx, dy])
        print("Bullet Fired!!!")

        # # Right mouse button toggles camera tracking mode
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    global enemy_position, cheat_mode, cheat_auto_camera, camera_radius, camera_angle, camera_height, first_person_mode, player_falling

    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if(not first_person_mode):
        cam_x = camera_radius * math.cos(math.radians(camera_angle))
        cam_y = camera_radius * math.sin(math.radians(camera_angle))
        cam_z = camera_height

        gluLookAt(cam_x, cam_y, cam_z,
                0, 0, 0,
                0, 0, 1)
    else:
        head_height = 140
        dx = math.cos(math.radians(player_angle))
        dy = math.sin(math.radians(player_angle))

        local_x = dx * 15
        local_y = dy * 15
        local_z = head_height

        if player_falling:
            fall_rad = math.radians(player_fall_angle)
            rotated_y = local_y * math.cos(fall_rad) - local_z * math.sin(fall_rad)
            rotated_z = local_y * math.sin(fall_rad) + local_z * math.cos(fall_rad)
            local_y, local_z = rotated_y, rotated_z

        cam_x = player_pos[0] + local_x
        cam_y = player_pos[1] + local_y
        cam_z = local_z + 10

        look_x = cam_x + dx * 100
        look_y = cam_y + dy * 100
        look_z = cam_z - 5

        if(cheat_mode and cheat_auto_camera):
            if(enemy_position):
                cam_x = player_pos[0] + dx * 15
                cam_y = player_pos[1] + dy * 15
                cam_z = head_height + 50
                ex, ey = min(enemy_position, key=lambda e: (e[0]-player_pos[0])**2 + (e[1]-player_pos[1])**2)
                look_x, look_y, look_z = ex, ey, 90

        gluLookAt(cam_x, cam_y, cam_z,
                  look_x, look_y, look_z,
                  0, 0, 1)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global paused, life, game_over, cheat_cooldown, player_angle, bullets, enemy_scale, enemy_size_control, bullets, bullet_miss, player_dead, player_fall_angle, player_falling

    if(paused):
        return

    if(game_over):
        if(not player_dead and not player_falling):
            player_falling = True
        
        if(player_falling):
            if(player_fall_angle < 90):
                player_fall_angle += 2
            else:
                player_fall_angle = 90
                player_falling = False
                player_dead = True

        glutPostRedisplay()
        return
    
    if(not game_over):
        if(enemy_size_control == 1):
            enemy_scale += 0.005
            if(enemy_scale > 1.3):
                enemy_size_control = -1
        else:
            enemy_scale -= 0.005
            if(enemy_scale <= 0.8):
                enemy_size_control = 1

        for b in bullets:
            b[0] += b[3] * bullet_speed
            b[1] += b[4] * bullet_speed

        new_bullets = []
        for b in bullets:
            if(-GRID_LENGTH <= b[0] <= GRID_LENGTH and -GRID_LENGTH <= b[1] <= GRID_LENGTH):
                new_bullets.append(b)
            else:
                bullet_miss += 1
                print(f"Bullet Missed: {bullet_miss}")
        bullets = new_bullets

        if(bullet_miss >= 10 and not game_over):
            game_over = True
            player_falling = True
            glutPostRedisplay()
            return

        update_enemies()
        bullet_hits_enemy()
        enemy_player_collision()

        if cheat_mode and life > 0:
        # Spin the whole player
            player_angle = (player_angle + cheat_spin_speed) % 360

            dx = math.cos(math.radians(player_angle))
            dy = math.sin(math.radians(player_angle))

            # Look for enemy in front
            for (ex, ey) in enemy_position:
                vx, vy = ex - player_pos[0], ey - player_pos[1]
                dist = math.sqrt(vx*vx + vy*vy) + 1e-5

                #angle between player forward and enemy direction
                vx /= dist
                vy /= dist
                dot = dx*vx + dy*vy

                if dot > 0.95: 
                    if cheat_cooldown <= 0:
                        # Fire bullet
                        gun_offset = 60
                        gun_height = 130
                        bx = player_pos[0] + dx * gun_offset
                        by = player_pos[1] + dy * gun_offset
                        bz = gun_height
                        bullets.append([bx, by, bz, dx, dy])
                        cheat_cooldown = cheat_fire_interval
                    break

            if cheat_cooldown > 0:
                cheat_cooldown -= 1

    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    global player_falling
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    tiles_per_side = 13
    tiles_size = (GRID_LENGTH * 2) / tiles_per_side
    
    for i in range(tiles_per_side):
        for j in range(tiles_per_side):
            x = -GRID_LENGTH + i * tiles_size
            y = -GRID_LENGTH + j * tiles_size
            
            if((i + j) % 2 == 0):
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
                
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x+tiles_size, y, 0)
            glVertex3f(x+tiles_size, y+tiles_size, 0)
            glVertex3f(x, y+tiles_size, 0)
            glEnd()
    
    # borders around the floor
    WALL_HEIGHT = 70
    WALL_THICKNESS = 10

    def draw_box(x1, y1, x2, y2, height, color):
        glColor3f(*color)
        glBegin(GL_QUADS)
        
        # Bottom
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y1, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x1, y2, 0)
        
        # Top
        glVertex3f(x1, y1, height)
        glVertex3f(x2, y1, height)
        glVertex3f(x2, y2, height)
        glVertex3f(x1, y2, height)
        
        # Front
        glVertex3f(x1, y1, 0)
        glVertex3f(x2, y1, 0)
        glVertex3f(x2, y1, height)
        glVertex3f(x1, y1, height)
        
        # Back
        glVertex3f(x1, y2, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x2, y2, height)
        glVertex3f(x1, y2, height)
        
        # Left
        glVertex3f(x1, y1, 0)
        glVertex3f(x1, y2, 0)
        glVertex3f(x1, y2, height)
        glVertex3f(x1, y1, height)
        
        # Right
        glVertex3f(x2, y1, 0)
        glVertex3f(x2, y2, 0)
        glVertex3f(x2, y2, height)
        glVertex3f(x2, y1, height)
        
        glEnd()

    half = GRID_LENGTH
    t = WALL_THICKNESS
    h = WALL_HEIGHT

    # Top wall (blue)
    draw_box(-half - t, half, half + t, half + t, h, (0, 0, 1))
    # Bottom wall (white)
    draw_box(-half - t, -half - t, half + t, -half, h, (1, 1, 1))
    # Left wall (green)
    draw_box(-half - t, -half, -half, half, h, (0, 1, 0))
    # Right wall (cyan)
    draw_box(half, -half, half + t, half, h, (0, 1, 1))

    # Display game info text at a fixed screen position
    if(paused):
        draw_text(400, 670, "Game Paused")
        draw_text(400, 640, "Click P again to resume game.")
    
    if(game_over):
        draw_text(10, 670, f"Game is Over!!! Your Score is {score}")
        draw_text(10, 640, "Press R to Restart")
    else:
        draw_text(10, 670, f"Player Life Remaining: {life}")
        draw_text(10, 640, f"Game Score: {score}")
        draw_text(10, 610, f"Player Bullet Missed: {bullet_miss}")

    #player
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 0)

    if(player_dead or player_falling):
        glRotatef(player_fall_angle, 1, 0, 0)  
    else:
        glRotatef(player_angle-90, 0, 0, 1)

    draw_shapes()
    glPopMatrix()

    for (x, y) in enemy_position:
        draw_enemy(x, y)

    for (bx, by, bz, dx, dy) in bullets:
        glPushMatrix()
        glTranslatef(bx, by, bz)
        glColor3f(1, 0, 0)
        glutSolidCube(7)
        glPopMatrix()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    create_enemies()
    print(f"Remaining Life of the player: {life}")

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
