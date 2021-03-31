import random, pygame, sys
from pygame.locals import *

FPS = 10

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20

assert WINDOWWIDTH % CELLSIZE == 0, "ширина окна должна быть кратна размеру ячейки"
assert WINDOWHEIGHT % CELLSIZE == 0, "высота окна должна быть кратна размеру ячейки."

CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

# Установка цветности на все процессы

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARKRED = (155, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0

# ------------- SYSTEM ------------- #
# синтаксический разбор: индекс головы змеи
def main():  # основное название игры
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.fill(GREEN);
    BASICFONT = pygame.font.Font('assets/pixelfont.ttf', 36)
    pygame.display.set_caption('Змейка')
    showStartScreen()

    while True:
        core()
        showGameOverScreen()

def core():  # Запуск игры
    DISPLAYSURF.fill(RED)
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx, 'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Запуск Итема яблока в случайном месте.
    apple = getRandomLocation()
    while True:  # основной игровой цикл
        for event in pygame.event.get():  # цикл обработки событий
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # проверка на столкновение змейки с самим собой.

        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or \
                wormCoords[HEAD]['y'] == CELLHEIGHT:
            return  # Конец Игры
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return  # Конец Игры

        # проверка на то что змейка съедает яблоко
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            apple = getRandomLocation()  # Установить появление яблока в случайном месте
        else:
            del wormCoords[-1]  # удалить хвостовой сегмент змеи
        # перемещение змейки путем добавления сегмента в направлении его перемещения
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords) - 3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():  # прекращение работы
    pygame.quit()
    sys.exit()


def getRandomLocation():  # получение случайного местоположения
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def checkKeyPress(): # проверить нажатую клавишу
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)

    if len(keyUpEvents) == 0:
        return None

    if keyUpEvents[0].key == K_ESCAPE:
        terminate()

    return keyUpEvents[0].key


def drawWorm(wormCoords):  # изображение змеи и её координат
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, YELLOW, wormInnerSegmentRect)


def drawApple(coord):  # изображение яблока
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, DARKRED, appleRect)
    appleInnerRect = pygame.Rect(x + 3, y + 3, CELLSIZE - 6, CELLSIZE - 6)
    pygame.draw.rect(DISPLAYSURF, RED, appleInnerRect)


def drawGrid():  # изображение сетки
    bg = pygame.image.load('assets/grass.png')
    bg = pygame.transform.scale(bg, (WINDOWWIDTH, WINDOWHEIGHT))
    DISPLAYSURF.blit(bg, (0, 0))
    for x in range(0, WINDOWWIDTH, CELLSIZE):  # изображение вертикальных линий
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE):  # изображение горизонтальных линий
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

# ------------- User Interface ------------- #
def showStartScreen():  # запуск главного меню
    # TODO: Переделать стартовый экран
    titleFont = pygame.font.Font('assets/pixelfont.ttf', 212)
    titleSurf1 = titleFont.render('Змейка', True, DARKGRAY)
    degrees1 = 0

    while True:
        bg = pygame.image.load('assets/bg.png')
        bg = pygame.transform.scale(bg, (WINDOWWIDTH, WINDOWHEIGHT))
        DISPLAYSURF.blit(bg, (0, 0))
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT - 100)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        drawStartGameMsg()

        if checkKeyPress():
            pygame.event.get()  # очистить очередь событий
            return

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def drawStartGameMsg():  # изображения поля начала игры
    pressKeySurf = BASICFONT.render('Нажмите A, чтобы начать игру!', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 310, 10)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def showGameOverScreen():  # показать экран проигрыша
    gameOverFont = pygame.font.Font('assets/pixelfont.ttf', 156)
    gameSurf = gameOverFont.render('GAME', True, WHITE)
    overSurf = gameOverFont.render('OVER', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawStartGameMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkKeyPress()  # Очистка нажатия клавиш, о очереди происходимых событий

    while True:

        if checkKeyPress():
            pygame.event.get()  # Очистка очереди событий
            return


def drawScore(score):  # счётчик приложения
    scoreSurf = BASICFONT.render('Счётчик: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


if __name__ == '__main__':
    main()
