from random import random
from signal import signal
import pygame
from time import time
from random import *
import random
# from goto import goto, comefrom, label

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
LIME = (124, 255, 0)

# Initialize the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1245, 636))
class Signal:
    def __init__(self, isRed, road_no, coors):
        self.coors = coors
        self.isRed = isRed
        self.road_no = road_no
        self.wait_time = 0
        self.number_of_cars = 0


class Car:
    def __init__(self, coorX, coorY, direction, color, signal_no):
        # Current coordinates of the car
        self.coorX = coorX
        self.coorY = coorY

        # the direction in which the car is moving
        self.direction = direction

        # flag to stop the car when the signal is red
        self.stop = False

        # whether the car has passed the padding region
        self.toChange = False

        # if it has crossed the padding region then in which direction it should move
        self.nextDirection = "?"

        # if it has crossed the padding region then after what distance the direction should change
        self.nextChangeDistance = 0

        # the color of the car
        self.color = color

        # in which signal the car is standing
        self.signal_no= signal_no
        
        # number of signal after the direction is changed 
        self.next_signal_no = -1

def draw_lines(lines):
    for line in lines:
        pygame.draw.line(screen, (0, 0, 0), line[0], line[1], 2)

class Padding:
    def __init__(self, fPoint, sPoint, padDist, directionList):
        self.fPoint = fPoint
        self.sPoint = sPoint
        self.padDist = padDist
        self.directionList = directionList
        # self.road_no = self.road_no

    def __str__(self) -> str:
        return str(self.fPoint) + str(self.sPoint) + str(self.padDist) + str(self.directionList)

    def draw_hori_padding(self):
        pygame.draw.line(screen, CYAN, self.fPoint, self.sPoint)
        nfPoint = (self.fPoint[0], self.fPoint[1]+self.padDist)
        nsPoint = (self.sPoint[0], self.sPoint[1] + self.padDist)
        pygame.draw.line(screen, CYAN, nfPoint, nsPoint)

    def draw_veri_padding(self):
        pygame.draw.line(screen, CYAN, self.fPoint, self.sPoint)
        nfPoint = (self.fPoint[0] + self.padDist , self.fPoint[1])
        nsPoint = (self.sPoint[0] + self.padDist , self.sPoint[1])
        pygame.draw.line(screen, CYAN, nfPoint, nsPoint)


pygame.display.set_caption("Space Invaders")

placed_cars = []

# what should be the speed of the cars
speed = 1

horizontal_paddings = []
vertical_paddings = []


def initialize_padding():
    global horizontal_paddings, vertical_paddings
    # padding lines
    # horizontal padding
    hori_padding = [
        # down paddings
        [(75, 170), (105, 170), (("R", 3), ("R", 3)), 40],
        [(451, 170), (480, 170), (("R", 5), ("R", 5)), 40],
        [(948, 170), (1005, 170), (("R", 0), ("D", 7)), 40],
        [(273, 413), (310, 413), (("R", 14), ("R", 14)), 21],
        [(948, 515), (1007, 515), (("R", 0), ("D", 0)), 40],
        # upp paddings
        [(274, 260), (234, 260), (("L", 0), ("L", 0)), -40],
        [(663, 260), (623, 260), (("L", 11), ("L", 11)), -40],
        [(948, 260), (885, 260), (("L", 9), ("U", 0)), -40],
        [(663, 468), (628, 468), (("L", 17), ("U", 10)), -25],
        [(130, 468), (94, 468), (("L", 0), ("L", 0)), -25]
    ]

    veri_paddings = [
        # Right paddings
        [(44, 214), (44, 170), (("U", 0), ("R", 3)), 20],
        [(417, 214), (417, 170), (("U", 0), ("R", 5)), 20],
        [(894, 214), (894, 170), (("U", 0), ("R", 0)), 40],
        [(238, 438), (238, 410), (("U", 12), ("U", 12)), 20],
        [(627, 439), (627, 411), (("U", 10), ("U", 10)), 20],
        # Left paddings
        [(307, 264), (307, 217), (("D", 16), ("L", 0)), -20],
        [(696, 264), (696, 217), (("D", 0), ("L", 11)), -20],
        [(1001, 264), (1001, 217), (("D", 7), ("L", 9)), -40],
        [(1001, 578), (1001, 550), (("D", 0), ("D", 0)), -20],
        [(162, 471), (162, 440), (("D", 0), ("L", 0)), -20]
    ]
    for line in hori_padding:
        horizontal_paddings.append(
            Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))
    for line in veri_paddings:
        vertical_paddings.append(
            Padding(fPoint=line[0], sPoint=line[1], padDist=line[3], directionList=line[2]))

signals = []

def initialize_signals():
    coordinates = [
        [(36, 192)],
        [(92, 154)],
        [(395, 193)],
        [(467, 146)],
        [(865, 193), (1020, 230)],
        [(977, 156), (924, 272)],
        [(977, 480)],
        [(1030, 568)],
        [(715, 236)],
        [(648, 280)],
        [(332, 236)],
        [(254, 288)],
        [(645, 500)],
        [(608, 425)],
        [(209, 425)],
        [(293, 387)],
        [(189, 457)],
        [(115, 497)]
    ]
    cnt = 0
    signals.append(Signal(isRed=False, road_no=0, coors=((-5, -5), (-5, -5))))
    for cnt in range(1, len(coordinates)+1):
        signals.append(Signal(isRed=cnt%2==1, road_no=cnt, coors=coordinates[cnt-1]))

def render_signals():
    # print("Hello");
    for sig in signals:
        if sig == "Srikanth":
            continue
        for i in sig.coors:
            # print(i)
            if sig.isRed:
                pygame.draw.circle(screen, RED, i, 20, 10)
            else:
                pygame.draw.circle(screen, GREEN, i, 20, 10)

def check_point_on_hor_line(line, point):
    x1 = min(line[0][0], line[1][0])
    x2 = max(line[0][0], line[1][0])
    if point[0] >= x1 and point[0] <= x2 and point[1] == line[0][1]:
        return True
    return False


def check_point_on_ver_line(line, point):
    y1 = min(line[0][1], line[1][1])
    y2 = max(line[0][1], line[1][1])
    if point[1] >= y1 and point[1] <= y2 and point[0] == line[0][0]:
        return True
    return False



def render_existing_cars():
    global placed_cars
    new_placed = []
    for car in placed_cars:
        # if not car.signal_no ==0:
        if not signals[car.signal_no].isRed:
            if car.direction == 'U' or car.direction == 'D':
                for padding in horizontal_paddings:
                    if check_point_on_hor_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                        car.toChange = True
                        tt = random.choice(padding.directionList)
                        car.nextDirection = tt[0]
                        car.next_signal_no = tt[1]
                        car.nextChangeDistance = randint(3, abs(padding.padDist))
            else:
                for padding in vertical_paddings:
                    if check_point_on_ver_line((padding.fPoint, padding.sPoint), (car.coorX, car.coorY)):
                        car.toChange = True
                        tt = random.choice(padding.directionList)
                        car.nextDirection = tt[0]
                        car.next_signal_no = tt[1]
                        car.nextChangeDistance = randint(3, abs(padding.padDist))
        x = car.coorX
        y = car.coorY
        if car.toChange:
            if car.nextChangeDistance == 0:
                car.direction = car.nextDirection
                car.signal_no = car.next_signal_no
                car.nextDirection = "?"
                car.nextChangeDistance = 0
                car.toChange = False
                car.next_signal_no = 0
            else:
                car.nextChangeDistance -= speed
        # if not car.signal_no == 0:
        if not signals[car.signal_no].isRed:
            if car.direction == 'R':
                x += speed
            elif car.direction == 'L':
                x -= speed
            elif car.direction == 'D':
                y += speed
            else:
                y -= speed
        car.coorX, car.coorY = x, y
        if x > 1245 or x < 0 or y > 636 or y < 0:
            continue
        new_placed.append(car)
        pygame.draw.circle(screen, car.color, (x, y), 5, 5)
    placed_cars = new_placed


valid_points_to_generate = [
    # points where cars can generate added padding
    [(0, 174), (0, 210), "R", 1],
    [(78, 2), (103, 2), "D", 2],
    [(2, 412), (2, 435), "R", 15],
    [(102, 625), (125, 625), "U", 18],
    [(456, 41), (477, 41), "D", 4],
    [(955, 41), (996, 41), "D", 6],
    [(1231, 221), (1231, 256), "L", 5],
    [(1234, 550), (1233, 573), "L", 8],
    [(633, 625), (657, 628), "U", 13],
    [(895, 630), (940, 630), "U", 18]
]


def rand_car():
    idx = randint(0, len(valid_points_to_generate) - 1)
    line = valid_points_to_generate[idx]
    x, y = -1, -1
    if line[2] == "V":
        x = line[0][0]
        y = randint(min(line[0][1], line[1][1]), max(line[0][1], line[1][1]))
    else:
        y = line[0][1]
        x = randint(min(line[0][0], line[1][0]), max(line[0][0], line[1][0]))
    placed_cars.append(Car(coorX=x, coorY=y, direction=line[2], color=BLUE, signal_no=line[3]))


def draw_valid_points():
    for i in valid_points_to_generate:
        pygame.draw.line(screen, CYAN, i[0], i[1])


def draw_road():
    road = [
        [(0, 170), (42, 170), "H"],
        [(42, 0), (42, 170)],
        [(0, 260), (240, 260)],
        [(0, 410), (240, 410)],
        [(106, 170), (106, 0)],
        [(106, 170), (415, 170)],
        [(415, 0), (415, 170)],
        [(480, 0), (480, 170)],
        [(480, 170), (890, 170)],
        [(890, 170), (890, 0)],
        [(1000, 170), (1000, 0)],
        [(1000, 170), (1240, 170)],
        [(1000, 260), (1240, 260)],
        [(1000, 520), (1240, 520)],
        [(1000, 580), (1240, 580)],
        [(1000, 580), (1000, 630)],
        [(1000, 260), (1000, 520)],
        [(700, 260), (890, 260)],
        [(890, 260), (890, 630)],
        [(700, 260), (700, 630)],
        [(625, 260), (625, 410)],
        [(625, 410), (303, 410)],
        [(303, 410), (303, 260)],
        [(0, 410), (237, 410)],
        [(237, 410), (237, 260)],
        [(237, 260), (0, 260)],
        [(307, 260), (625, 260)],
        [(0, 470), (100, 470)],
        [(100, 470), (100, 630)],
        [(160, 470), (160, 630)],
        [(160, 470), (630, 470)],
        [(630, 470), (630, 630)]
    ]
    for line in road:
        pygame.draw.line(screen, LIME, line[0], line[1])


running = True
image = pygame.image.load(r'mywork/road.png')
car = pygame.image.load(r'car_1.png')
start_time = time()

initialize_padding()
initialize_signals()

def flip_signal():
    for idx in range(1, len(signals)):
        signals[idx].isRed ^= True

timer = 1

while running:
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    render_existing_cars()
    render_signals()
    for padding in horizontal_paddings:
        padding.draw_hori_padding()
    now_time = time()
    if(now_time - start_time > 1):
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        rand_car()
        timer += 1
        start_time = now_time
    if timer % 10 == 0:
        flip_signal()
        timer = 1
    pygame.display.update()
