from OpenGL.GL import *
from OpenGL.GLUT import *
import random as rd
import time

start_time = time.time()

score = 0
r, g, b = 0, .3, 0

game_det = {"gameover": False, "pause": False, "score": 0}
car_det = {"speed": 0.5}

lx , ly = 150, 430
cx, cy = 225, 40

cars = []

class Car:
    global cy, car_det

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = rd.choice([30, 40, 50, 60])

    def draw_obs(self):
        obstacles(self.x, self.y, self.size)

    def update_car(self):
        global car_det, game_det

        if not game_det["pause"] and not game_det["gameover"]:
            self.y -= car_det["speed"]


def car_func():
    c_x = rd.choice([75, 225, 375])
    c_y = 420
    cars.append(Car(c_x, c_y))


def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def pause_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490, 2)
    mpl(240, 450, 240, 490, 2)


def play_button():
    glColor3f(1.0, 1.0, 0.0)
    mpl(210, 450, 210, 490, 2)
    mpl(210, 450, 240, 469, 2)
    mpl(210, 491, 240, 471, 2)


def cancel_button():
    glColor3f(1.0, 0.0, 0.0)
    mpl(400, 450, 435, 490, 2)
    mpl(400, 490, 435, 450, 2)


def restart_button():
    glColor3f(0.0, 0.75, 0.8)
    mpl(15, 470, 50, 470, 2)
    mpl(15, 470, 32.5, 490, 2)
    mpl(15, 470, 32.5, 450, 2)


def draw_lane():
    glColor3f(1.0, 1.0, 1.0)

    mpl(lx, ly, lx, ly - 50, 10)
    mpl(lx + 150, ly, lx + 150, ly - 50, 10)

    mpl(lx, ly - 125, lx, ly - 175, 10)
    mpl(lx + 150, ly - 125, lx + 150, ly - 175, 10)

    mpl(lx, ly - 250, lx, ly - 300, 10)
    mpl(lx + 150, ly - 250, lx + 150, ly - 300, 10)

    mpl(lx, ly - 375, lx, ly - 425, 10)
    mpl(lx + 150, ly - 375, lx + 150, ly - 425, 10)

def draw_car():
    global r, g, b

    glColor3f(0.0, 0.0, 1.0)
    mpl(cx - 30, cy + 35, cx - 30, cy + 25, 10)
    mpl(cx + 30, cy + 35, cx + 30, cy + 25, 10)
    mpl(cx - 30, cy - 35, cx - 30, cy - 25, 10)
    mpl(cx + 30, cy - 35, cx + 30, cy - 25, 10)

    glColor3f(r, g, b)
    mpl(cx, cy, cx, cy, 60)


def obstacles(x, y, s):  # y+s/2-2, y+s/2-5
    glColor3f(0, 1, 1)
    mpl(x - s / 2 + 1, y + s / 2 + 2, x - s / 2 + 1, y + s / 2 - 5, 10)
    mpl(x - s / 2 + 1, y - s / 2 - 2, x - s / 2 + 1, y - s / 2 + 5, 10)
    mpl(x + s / 2 - 1, y + s / 2 + 2, x + s / 2 - 1, y + s / 2 - 5, 10)
    mpl(x + s / 2 - 1, y - s / 2 - 2, x + s / 2 - 1, y - s / 2 + 5, 10)

    glColor3f(1, .5, 0)
    mpl(x, y, x, y, s)

def mpl(x0, y0, x1, y1, s):
    zone = findzone(x0, y0, x1, y1)
    x0, y0 = converttozone0(zone, x0, y0)
    x1, y1 = converttozone0(zone, x1, y1)

    dx = x1 - x0
    dy = y1 - y0

    dne = 2 * dy - 2 * dx
    de = 2 * dy

    dinit = 2 * dy - dx

    while x0 <= x1:
        if dinit >= 0:
            dinit += dne
            x0 += 1
            y0 += 1
        else:
            dinit += de
            x0 += 1

        a, b = converttozoneM(zone, x0, y0)
        draw_points(a, b, s)


def findzone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0

    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        else:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        else:
            zone = 6

    return zone


def converttozone0(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def converttozoneM(zone, x, y):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def specialKeyListener(key, x, y):
    global cx, cy

    if game_det['gameover'] == False and game_det['pause'] == False:
            if key == GLUT_KEY_LEFT:
                if (cx - 150 >= 0):
                    cx -= 150
            elif key == GLUT_KEY_RIGHT:
                if (cx + 150 <= 450):
                    cx += 150

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global game_det, car_det, cx, cy, start_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if 210 <= x <= 240 and 10 <= y <= 50:
            if game_det["gameover"] == False:
                if game_det["pause"] == False:
                    game_det["pause"] = True
                    if game_det["score"] == 0:
                        print('Paused\n')
                    else:
                        print('\nPaused\n')
                else:
                    game_det["pause"] = False
        elif 15 <= x <= 50 and 10 <= y <= 50:
            if game_det["gameover"] == True:
                game_det["gameover"] = False

            if game_det["score"] == 0:
                print('Starting Over\n')
            else:
                print('\nStarting Over\n')
            cars.clear()
            start_time = time.time()

            game_det["score"] = 0
            car_det["speed"] = .5

            cx, cy = 225, 40
        elif 400 <= x <= 435 and 10 <= y <= 50:
            game_det["gameover"] = True

            print('Goodbye! Final Score:', game_det["score"])

            glutLeaveMainLoop()

    glutPostRedisplay()


def animate():
    global game_det, car_det, ly, vehicles, start_time, score, cars, cx, cy, r, g, b

    if game_det["gameover"] == False and game_det['pause'] == False:
        if cars == []:
            car_func()
        else:
            for veh in cars:
                veh.update_car()

        elapsed_time = time.time() - start_time

        if elapsed_time >= 2:
            car_func()
            start_time = time.time()

        ly -= car_det["speed"]

        if (ly - 375) <= 0:
            ly += 125

    glutPostRedisplay()


def playg():
    global cars, score, game_det, car_det, cx, cy, r, g, b

    if game_det["gameover"] == False and game_det["pause"] == False:
        for car in cars:
            if car.y <= 0:
                game_det["score"] += 1
                print(f"Score: {game_det['score']}")
                cars.remove(car)

                if game_det["score"] > 0 and game_det["score"] % 5 == 0:
                    car_det["speed"] += 0.2
                    r = rd.uniform(0.0, 1.0)
                    g = rd.uniform(0.0, 1.0)
                    b = rd.uniform(0.0, 1.0)

                    print("\nSpeed Increased\nCar Colour Changed\n")
                break

            if car.x == cx and (car.y - (car.size / 2)) <= cy + 30:
                game_det["gameover"] = True
                if game_det["score"] > 0:
                    print("\nCrash!\nFinal Score:", game_det["score"])
                else:
                    print("Crash!\nFinal Score:", game_det["score"])
                break


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    animate()
    glColor3f(0.0, 0.0, 0.0)

    if game_det["pause"] == False:
        pause_button()
    else:
        play_button()

    cancel_button()
    restart_button()

    draw_lane()
    draw_car()

    for c in cars:
       c.draw_obs()

    playg()


    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(450, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Circle Shooter Game")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()