# tiek importētas nepieciešamas bibliotēkas programmai
import pygame
import random


from db import Database


# inizalize tetri un nosaka screen vertibu
pygame.init()


#Ekrāna vērtība
SCREEN = WIDTH, HEIGHT = 600,600
win = pygame.display.set_mode(SCREEN)



f = open('temp.txt', 'w')

# FPS
clock = pygame.time.Clock()
FPS = 60

# noteiktas vērtības kāda būs spēļu laukums un viena kvadrāta lielums
CELLSIZE = 35
ROWS = (HEIGHT-25) // CELLSIZE
COLS = (WIDTH - 250) // CELLSIZE

# COLORS
BLACK = (0,0,0)
BLUE = (31,25,76)
RED = (252,91,122)
WHITE = (255,255,255)
GRAY = (220,220,220)




# BLOCKS 

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



# FONTS
font = pygame.font.Font('Fonts/FontsFree-Net-Tetris.ttf',50)
font2 = pygame.font.SysFont('cursive',25)


class Tetramino:

    # mainīgie kas nodrošina spēles funckionalitāti
    running = True
    counter = 0
    can_move = True   
    increaseGravity = False
     
    # matrix
    # 0   1   2   3
    # 4   5   6   7
    # 8   9   10  11
    # 12  13  14  15
    
# pieminet to ka figuras un tas rotacijas ir veidotas pec noteikumiem
#Figūru masīvs
    FIGURES = {
        'I' : [[1, 2, 5, 6]],
        'S' : [[1, 2, 5, 6]],
        'Z' : [[1, 2, 5, 6]],
        'O' : [[1, 2, 5, 6]],
        'T' : [[1, 2, 5, 6]],
        'L' : [[1, 2, 5, 6]],
        'J' : [[1, 2, 5, 6]]   
        
    }
# Tipu masīvs
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
        self.nextFigure = None
        self.gameover = False
        self.newFigure()
        
        
    def drawGrid(self):    
        # Izveido rindiņas ievērjoto arī cellsize
        for i in range(self.rows+1):
            pygame.draw.line(win,GRAY,(0, CELLSIZE*i),(WIDTH,CELLSIZE*i),1)
        # Izveido kollonas ievērjoto arī cellsize
        for j in range(self.cols+1):
            pygame.draw.line(win,GRAY,(CELLSIZE*j,0),(CELLSIZE*j,HEIGHT),1)
    
        #Izveidot 2 jaunas figūras lai varētu spēlētājam padot tālāk kāda figurā būs nakamā
    def newFigure(self):
        if not self.nextFigure:
            self.nextFigure = Tetramino(5, 0)           
        self.figure = self.nextFigure
        self.nextFigure = Tetramino(5, 0)
        
        # Gravitācijas metode
    def gravity(self):
        self.figure.y += 1   
        if self.intersect():
            self.figure.y -= 1
            self.freeze()

        # Instant metode kas liek figurāi uzreiz nokrist uz zemes
    def instant(self):
        while not self.intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

        # Kustības uz sāniem
    def xMovement(self,dx):
        self.figure.x += dx
        if self.intersect():
            self.figure.x -= dx
        
        #Rotācija
    def rotate(self):
        rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersect():
            self.figure.rotation = rotation
    
        # Intersect metode kas pārbauda vai 4x4 matricā nav citas figūras vai spēles robeža ja ir tad intersection paliek true
    def intersect(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.rows -1 or \
                        j + self.figure.x > self.cols  -1 or \
                        j + self.figure.x < 0 or \
                        self.board[i+self.figure.y][j+self.figure.x]> 0:
                            intersection = True
        return intersection
    
    # parbauda katru rindu vai viņa nav pilna, ja ir pilna tad viņu izdzēsīs un pievienos jaunu rindu spēles laukuma augšā
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
      
    # pirmie divi cikli uzģenerē šo 4x4 matricu un par cik figūras ir nekas vairāk kā tikai 4x4 matrica ar aizpildītām vērtībam ši funckija         
    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.board[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.destroy_line()
        self.newFigure()
        if self.intersect():
            self.gameover = True       
#Spēlētaju kustības metode                       
    def handle_event(self,event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.xMovement(-1)    
                type = str(tetris.figure.type)
                            
                mov = " a\n"
                time = str(pygame.time.get_ticks())
                e = type + "," + time + "," + mov 
                
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.xMovement(1)
                type = str(tetris.figure.type)
                r = " d\n"
                time = str(pygame.time.get_ticks())
                e = type + "," + time + "," + r
                f.writelines(str(e))
                

                
            if event.key == pygame.K_UP or event.key == pygame.K_u:
                self.rotate()
                
                print(tetris.figure.type)
                u = " w\n"
                time = str(pygame.time.get_ticks())
                type = str(tetris.figure.type)
                e = type + "," + time + "," + u 
                f.writelines(str(e))
                
            if event.key == pygame.K_DOWN:
                Tetramino.increaseGravity = True
                u = " s\n"
                time = str(pygame.time.get_ticks())
                type = str(tetris.figure.type)
                e = type + "," + time + "," + u 
                f.writelines(str(e))
                
                
            if event.key == pygame.K_SPACE and not  self.gameover:
                self.instant()
                u = " space\n"
                time = str(pygame.time.get_ticks())
                type = str(tetris.figure.type)
                e = type + "," + time + "," + u 
                f.writelines(str(e))
                
                
            if event.key == pygame.K_p:
                print("Pause")
                can_move = not can_move
                
                u = " p\n"
                time = str(pygame.time.get_ticks())
                e = type + "," + time + "," + u 
                f.writelines(str(e))
                
            if event.key== pygame.K_r:
                print("gameover")
                Database.connect_and_save()
                self.__init__(ROWS,COLS)

            
                
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                Tetramino.running = False 
                  
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                Tetramino.increaseGravity = False



tetris = Tetris(ROWS, COLS)
Database.connect_and_execute()

'''
temp1 = 3
getLastCreatedGame = 'SELECT * FROM gamecount ORDER BY ID DESC LIMIT 1'
addToGamecountTable= 'insert into gamecount(gamecount) value ("',(int(getLastCreatedGame[1])+1),'")'
'''

while Tetramino.running:
        
    win.fill(BLACK)
    
    Tetramino.counter += 1
    if Tetramino.counter >= 10000:
        Tetramino.counter = 0
        
    if Tetramino.can_move :
        if Tetramino.counter % (FPS // (tetris.level * 2)) == 0 or Tetramino.increaseGravity:
            if not tetris.gameover:
                tetris.gravity()
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Tetramino.running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                Tetramino.running = False
            else:
                # handle the event
                tetris.handle_event(event)
    
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
# Rāmji 
    pygame.draw.rect(win, BLUE,(WIDTH - 249, 0,HEIGHT, 600))   
    pygame.draw.rect(win, BLUE,(0, HEIGHT-39, WIDTH,120))   
    pygame.draw.rect(win, BLACK,(0, 0, WIDTH, HEIGHT),2)    
    

        
    #HUD
    if tetris.nextFigure:
        for i in range(4):
            for j in range(4):
                if i * 4 + j in tetris.nextFigure.image():
                    x = 400 + CELLSIZE * (tetris.nextFigure.x + j - 4)
                    y = 100 + CELLSIZE * (tetris.nextFigure.y + i)
                    img = Assets[tetris.nextFigure.color]
                    win.blit(img, (x,y)) 
    
    
    scoreimg = font.render(f'{tetris.score}', True, WHITE)
    levelimg = font2.render(f'Level : {tetris.level}', True, WHITE)
    
    win.blit(scoreimg,(400 - scoreimg.get_width()//2,HEIGHT - 110))
    win.blit(levelimg,(400 - levelimg.get_width()//2,HEIGHT - 30)) 
     
      
        #GAMEOVER
    if tetris.gameover:
        
        rect = pygame.Rect(50,140,WIDTH-190, HEIGHT - 350)
        pygame.draw.rect(win,BLACK, rect)
        pygame.draw.rect(win,RED,rect,2)
        
        over = font2.render('Gameover', True , WHITE)
        msg1 = font2.render('Press r to restart', True , WHITE)
        msg2 = font2.render('Press q to quit', True , WHITE)
        
        win.blit(over, (rect.centerx - over.get_width()//2, rect.y+20))
        win.blit(msg1, (rect.centerx - msg1.get_width()//2, rect.y+80))
        win.blit(msg2, (rect.centerx - msg2.get_width()//2, rect.y+110))
        
        
    clock.tick(FPS)
    pygame.display.update()
            
pygame.quit()
            
            
            
            
            
            