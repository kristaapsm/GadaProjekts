import pygame
import random

pygame.init()
SCREEN = WIDTH, HEIGHT = 600,600
win = pygame.display.set_mode(SCREEN)

clock = pygame.time.Clock()
FPS = 60

CELLSIZE = 35
ROWS = (HEIGHT-25) // CELLSIZE
COLS = (WIDTH - 250) // CELLSIZE


BLACK = (0,0,0)
BLUE = (31,25,76)
RED = (252,91,122)
WHITE = (255,255,255)
GRAY = (220,220,220)

img1 = pygame.image.load('Assets/11.png')
img2 = pygame.image.load('Assets/22.png')
img3 = pygame.image.load('Assets/33.png')
img4 = pygame.image.load('Assets/44.png')

Assets = {
    1: img1,
    2: img2,
    3: img3,
    4: img4
}

class Tetramino:
    # matrix
    # 0   1   2   3
    # 4   5   6   7
    # 8   9   10  11
    # 12  13  14  15

    FIGURES = {
    'I' : [[1, 5, 9, 13], [4, 5, 6, 7]],
        'S' : [[6, 7, 9, 10], [1, 5, 6, 10]],
        'Z' : [[4, 5, 9, 10], [2, 6, 5, 9]],
        'O' : [[1, 2, 5, 6]],
        'T' : [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        'L' : [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        'J' : [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]]    
        
    }
    TYPES = ['I', 'S', 'Z', 'O', 'T', 'L', 'J']
    

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = random.choice(self.TYPES)
        self.shape = self.FIGURES[self.type]
        self.color = random.randint(1,4)
        self.rotation = 0
# atgriež shape un tas rotācijas vērtību
    def image(self):
        return self.shape[self.rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shape)
        

class Tetris:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.level = 1
        self.score = 0
        self.board = [[0 for j in range(cols)] for i in range(rows)]
        self.gameover = False
        self.newFigure()
        self.next = None
        
    def drawGrid(self):    
            # Izveido rindiņas ievērjoto arī cellsize
        for i in range(self.rows+1):
            pygame.draw.line(win,GRAY,(0, CELLSIZE*i),(WIDTH,CELLSIZE*i),1)

        # Izveido kollonas ievērjoto arī cellsize
        for j in range(self.cols+1):
            pygame.draw.line(win,GRAY,(CELLSIZE*j,0),(CELLSIZE*j,HEIGHT),1)
    
    def newFigure(self):
        if not self.next:
            self.next = Tetramino(5,0)
        self.figure = self.next
        self.next = Tetramino(5,0)
        
    def gravity(self):
        self.figure.y += 1   
        if self.intersect():
            self.figure.y -= 1
            self.freeze()
    
    def instant(self):
        while not self.intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def xMovement(self,dx):
        self.figure.x += dx
        if self.intersect():
            self.figure.x -= dx
        
    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
    
    def intersect(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.rows - 1 or \
                        j + self.figure.x > self.cols - 1 or \
                        j + self.figure.x < 0 or \
                        self.board[i+self.figure.y][j+self.figure.x]> 0:
                            intersection = True
        
        return intersection
    # parbauda katru rindu vai viņa nav pilna, ja ir pilna tad viņu izdzēsīs un pievienos jaunu rindu spēles augšā
    def destroy_line(self):
        rerun = False
        for y in range(self.rows-1,0,-1):
            is_full = True
            # parbauda vai ir pilna
            for x in range(0,self.cols):
                if self.board[y][x] == 0:
                    is_full = False
            
            if is_full:
                del self.board[y]
                self.board.insert(0,[0 for i in range(self.cols)])
                self.score += 1
                if self.score % 10 == 0:
                    self.level += 1
                rerun = True
                   
        if rerun:
            self.destroy_line()
            
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.destroy_line()
        self.newFigure()
        
        if self.intersect():
            self.gameover = True            
    
counter = 0
increaseGravity = False

tetris = Tetris(ROWS, COLS)


running = True
while running: 
    win.fill(BLACK)
    
    counter += 1
    if counter >= 10000:
        counter = 0
    
    if counter % (FPS // (tetris.level * 2)) ==0 or increaseGravity:
        if not tetris.gameover:
            tetris.gravity()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False          

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                tetris.xMovement(-1)
            
            if event.key == pygame.K_RIGHT:
                tetris.xMovement(1)
                
            if event.key == pygame.K_UP:
                tetris.rotate()
            
            if event.key == pygame.K_DOWN:
                increaseGravity = True
            
            if event.key == pygame.K_SPACE:
                tetris.instant()
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                increaseGravity = False
                

    tetris.drawGrid()
    # display board
    for x in range(ROWS):
        for y in range(COLS):
            if tetris.board[x][y]> 0:
                val = tetris.board[x][y]>0
                win.blit(img, (y*CELLSIZE,x*CELLSIZE))

    
    # display shape independet of board
    for i in range(4):
        for j in range(4):
            if i * 4 + j in tetris.figure.image():
                img = Assets[tetris.figure.color]
                x = CELLSIZE * (tetris.figure.x + j)
                y = CELLSIZE * (tetris.figure.y + i)
                win.blit(img,(x,y))
                #pygame.draw.rect(win,RED, (x,y,CELLSIZE-1,CELLSIZE-1))

    #HUD
    
    
        
    # Rāmji 
    pygame.draw.rect(win, BLUE,(WIDTH - 249, 0,HEIGHT, 600))   
    pygame.draw.rect(win, BLUE,(0, HEIGHT-39, WIDTH,120))   
    pygame.draw.rect(win, BLACK,(0, 0, WIDTH, HEIGHT),2)  
    
    clock.tick(FPS)
    pygame.display.update()
            
pygame.quit()
            
            
            
            
            
            