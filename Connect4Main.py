import numpy  as np
import pygame
import sys
import math
import random

pygame.init()

ROWS = 6
COLUMNS = 7
BLUE = (74, 134, 232, 100)
RED = (204, 0, 0)
YELLOW = (241, 194, 50)
GRAY = (67, 67, 67)
SoundOn=1
TimerOn=1

pygame.mixer.init()#start the music and play it constantly
pygame.mixer.music.load("Connect4Music.mp3")   
pygame.mixer.music.play(-1)  

def CreateBoard():#create the 2D array for the board
    board = np.zeros((ROWS, COLUMNS))#use numpy to create 6x7 2D array
    return board

#player vs player main game
def PlayPVP():
    global SoundOn, TimerOn
    pygame.display.set_caption("Pygame Player vs Player")
    screen = pygame.display.set_mode((750,780))
    screen.fill(BLUE)

    board = CreateBoard()
    turn = 1

    SQUARESIZE = 100
    SCREEN_WIDTH = COLUMNS * SQUARESIZE+50 #750
    SCREEN_HEIGHT = (ROWS+1) * SQUARESIZE+80 #780
    CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
    MainFont = pygame.font.SysFont("arial", 90)
    SmallerFont = pygame.font.SysFont("arial", 30)      
    homeImg = pygame.image.load("home.png")
    homeImg = pygame.transform.scale(homeImg,(55, 60))#change size of home icon


    game_state = "running"


    def ColumnFullCheck(board, column):#check if the top row of the column that the player chose is full
            if board[ROWS-1][column] == 0:
                    return True
            return False

    def ValidRowCheck(board, column):#for the column that the player chose, check what is the next open row from the bottom to top
            for r in range(ROWS):
                    if board[r][column] == 0:
                            return r

    def DropPiece(board, row, column, turn):#Drop the piece in the board using the column they chose and the next open row as coordinates
            board[row][column] = turn

    def WinCheck(board, turn):
            # Check horizontal win
            for c in range(COLUMNS-3):
                    for r in range(ROWS):
                            if board[r][c] == turn and board[r][c+1] == turn and board[r][c+2] == turn and board[r][c+3] == turn:
                                    return True
            # Check vertical win
            for c in range(COLUMNS):
                    for r in range(ROWS-3):
                            if board[r][c] == turn and board[r+1][c] == turn and board[r+2][c] == turn and board[r+3][c] == turn:
                                    return True
            # Check positive slope
            for c in range(COLUMNS-3):
                    for r in range(ROWS-3):
                            if board[r][c] == turn and board[r+1][c+1] == turn and board[r+2][c+2] == turn and board[r+3][c+3] == turn:
                                    return True
            # Check negative slope
            for c in range(COLUMNS-3):#start at 3 because its not possible to have a negative slope that goes down from the 3rd row because you need at least 4
                    for r in range(3, ROWS):
                            if board[r][c] == turn and board[r-1][c+1] == turn and board[r-2][c+2] == turn and board[r-3][c+3] == turn:
                                    return True
            
    def TieCheck(board):
            #Check tie
            for c in range(COLUMNS):
                    for r in range(ROWS):
                            if board[r][c] == 0:
                                    return False
            return True
    def DrawBoard(board):
            board = np.flip(board, 0)#flip the board so the (0,0) index starts at bottom left corner instead of top left
            screen.blit(homeImg, (25, 8)) #display the home icon image
            if SoundOn == 1: #if sound is on, load the volume on img, and if its off load the volume off image
                volumeImg = pygame.image.load("volume.png")
                volumeImg = pygame.transform.scale(volumeImg,(55, 60)) 
            else:
                volumeImg = pygame.image.load("volumeoff.png")
                volumeImg = pygame.transform.scale(volumeImg,(55, 60))
            screen.blit(volumeImg, (95, 8)) #display the volume image

            #initial rendering of the timer, or else it would take 1 second for the timer to load in after you open the game
            if TimerOn == 1:
                minutes = counter1 // 60  # Calculate minutes
                seconds = counter1 % 60  # Calculate seconds
                text1 = f"{minutes:02d}:{seconds:02d}"  # Format the text
                screen.fill(BLUE, (580, 20, 200, 45))
                screen.blit(TimerFont.render(text1, True, (0, 0, 0)), (580, 20))

            for c in range(COLUMNS): #draw 42 squares with a circle in each one to make the 6x7 board.
                    for r in range(ROWS):
                            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE+SQUARESIZE/4, r*SQUARESIZE+SQUARESIZE+80, SQUARESIZE, SQUARESIZE))

            for c in range(COLUMNS):
                    for r in range(ROWS):
                            if board[r][c] == 0: #draw different colored circles based on what piece is placed in the coordinate. If there is none, make it gray
                                    pygame.draw.circle(screen, GRAY, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)
                            elif board[r][c] == 1:
                                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)
                            else:
                                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)

            if game_state == "win":
                    DisplayWin(winner)

    def DisplayWin(winner):#create a square overlay which says the player who won and gives the options to quit game or replay
            pygame.draw.rect(screen, BLUE, pygame.Rect(0, 0, 750, 780))
            if winner == "Tie":
                    label = MainFont.render("It's a tie!", 1, RED)
                    screen.blit(label, (SCREEN_WIDTH/2-150, SCREEN_HEIGHT/2-100))
            elif winner == "Time":
                label = MainFont.render("Time's Up.", 1, RED)
                screen.blit(label, (SCREEN_WIDTH/2-190, SCREEN_HEIGHT/2-200))
                label = MainFont.render("It's a tie!.", 1, RED)
                screen.blit(label, (SCREEN_WIDTH/2-170, SCREEN_HEIGHT/2-100))
            else:
                    label = MainFont.render(f"{winner} wins!", 1, RED)
                    screen.blit(label, (SCREEN_WIDTH/2-280, SCREEN_HEIGHT/2-100))
            # Create "Play Again" button
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 + 20, 160, 50))#create a rectangle for the button, and display the text over it
            play_again_label = SmallerFont.render("Play Again", 1, BLUE)
            screen.blit(play_again_label, (SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 + 30))
            # Create "Quit" button
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH/2 - 60, SCREEN_HEIGHT/2 + 90, 120, 50))
            quit_label = SmallerFont.render("Quit", 1, BLUE)
            screen.blit(quit_label, (SCREEN_WIDTH/2 - 35, SCREEN_HEIGHT/2 + 100))

    def AnimateFallingPiece(column, turn): #animation of dropping the piece
            if row is not None: #check if the selected column is NOT full
                    starting_y = 80 #where the circle starts to drop from
                    ending_y = (ROWS - row) * SQUARESIZE - 50
                    current_y = starting_y
                    while current_y <= ending_y: #loop to check if the current y of the circle is less than the ending y(where the circle should stop moving)
                            screen.fill(BLUE, (0, 70, 800, 800))
                            DrawBoard(board)
                            if turn == 1:
                                    pygame.draw.circle(screen, RED, (int(column*SQUARESIZE+70), int(current_y+110)), CIRCLE_RADIUS)
                            else:
                                    pygame.draw.circle(screen, YELLOW, (int(column*SQUARESIZE+70), int(current_y+110)), CIRCLE_RADIUS)
                            pygame.display.update()
                            current_y = current_y + 4 
                            #this animation works by incremeenting the y position of the circle, which allows it to move downwards. The board redraws and the screen updaates until the current y reaches the ending y.
    
    is_paused1 = False  # Variable to track the timer's state
    counter1, text1 = 120, '02:00'
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Timer set to 1 second
    TimerFont = pygame.font.SysFont('Consolas', 45)   


    while True:
        DrawBoard(board)
        for event in pygame.event.get():  #pygame quit loop
            if event.type == pygame.QUIT:
                sys.exit()

            if game_state == "running": #what happens if a game is currently being played(no winner yet)
                if event.type == pygame.USEREVENT and not is_paused1 and TimerOn == 1:     
                    minutes = counter1 // 60  # Calculate minutes
                    seconds = counter1 % 60  # Calculate seconds
                    text1 = f"{minutes:02d}:{seconds:02d}"  # Format the text
                    counter1 -= 1
                    screen.fill(BLUE, (580, 20, 200, 45))
                    screen.blit(TimerFont.render(text1, True, (0, 0, 0)), (580, 20))                                                                        
                    if counter1 < 0:
                        winner= "Time"
                        game_state= "win"

                if event.type == pygame.MOUSEMOTION:  #moving your cursor around to move the circle at the top
                    Xpos, Ypos = event.pos #position of the cursor in the pygame window
                    if Ypos < 70: #check if the cursor is less than 200 because the top of the screen is for the home button
                        continue 
                    if turn == 1: #display a yellow or red circle in the top rectangle based on whose turn it is
                        pygame.draw.rect(screen, BLUE, (0, 65, SCREEN_HEIGHT, SQUARESIZE)) #make a rectangle where there is a circle displaying where the player is going to drop the circle
                        pygame.draw.circle(screen, RED, (Xpos, int(SQUARESIZE+15)), CIRCLE_RADIUS)
                    else:
                        pygame.draw.rect(screen, BLUE, (0, 65, SCREEN_HEIGHT, SQUARESIZE)) #make a rectangle where there is a circle displaying where the player is going to drop the circle
                        pygame.draw.circle(screen, YELLOW, (Xpos, int(SQUARESIZE+15)), CIRCLE_RADIUS)
                
                if event.type == pygame.MOUSEBUTTONDOWN: #drop yellow or red circle when p1 or p2 player chooses a column
                    Xpos, Ypos = event.pos
                    if Ypos < 70:
                        if 25 <= Xpos <= 80 and 8 <= Ypos <= 68: #click on the home button
                            OpenHomepage()
                            return
                        if 95 <= Xpos <= 150 and 8 <= Ypos <= 68: #click on the volume button
                            if SoundOn == 1: #if the volume is on, change soundON to 2
                                SoundOn = 2
                                pygame.draw.rect(screen, BLUE, (95, 8, 55, 60)) #draw a blue rectangle over the volume icon because you cant remove the blitted image
                            else:
                                SoundOn = 1
                                pygame.draw.rect(screen, BLUE, (95, 8, 55, 60))

                            if SoundOn == 2: #if SoundOn is 2, stop the music because soundOn == 2 means that volume is off
                                pygame.mixer.music.stop()
                            elif SoundOn == 1:  
                                pygame.mixer.music.load("Connect4Music.mp3")   
                                pygame.mixer.music.play(-1)      
                        continue #ignore click event if the coordinate was less than 200
                        
                    if turn == 1: #player 1
                        pygame.draw.rect(screen, BLUE, (155, 5, 400, 40))
                        Xpos = event.pos[0]
                        column = int(math.floor(Xpos/SQUARESIZE)) #calculate the column index dividing the x coordinate of the mouse click and the squarsize(100). Then floor the number to the nearest whole number
                        if column == 7:#after the calculation, need to check if the column is 7 because it cant be more than 6(or else crash) since the column array is from 0-6
                            column = column-1

                        if not ColumnFullCheck(board, column): #if column is not full, continue to the next code, or else stay until they choose a column thats not full
                            continue
                        row = ValidRowCheck(board, column)
                        AnimateFallingPiece(column, turn)
                        DropPiece(board, row, column, turn)#set row to the next open row in the column the player chose

                    else: #player 2
                        pygame.draw.rect(screen, BLUE, (155, 5, 400, 40))                        
                        Xpos = event.pos[0]
                        column = int(math.floor(Xpos/SQUARESIZE))
                        if column == 7:
                            column = column-1

                        if not ColumnFullCheck(board, column):
                            continue
                        AnimateFallingPiece(column, turn)
                        row = ValidRowCheck(board, column)
                        DropPiece(board, row, column, turn)

                    if WinCheck(board, turn): #if there is a winner, assign the winner to the "winner" variable
                        if turn == 1:
                            winner = "Player 1"
                            game_state = "win"
                        else:
                            winner = "Player 2"
                            game_state = "win"
                    if TieCheck(board):
                        winner = "Tie"
                        game_state = "win"
                    TwoContinuousTurn = random.randint(0,8)
                #Just for testing 0-1 range, Ill change to 0-10 later.
                    if TwoContinuousTurn == 1:
                    #preparation for displaying text
                        text = "LUCKY YOU! You got two turns!!"
                        font = pygame.font.Font(None, 36)
                        if turn == 1:
                            text_surface = font.render(text, True, RED) 
                        elif turn == 2:
                            text_surface = font.render(text, True, YELLOW)            
                           
                    
                        screen.blit(text_surface, (155, 5))
                                
                        turn = turn # remain the turn
                    else:
                        turn = 3 - turn #switch between player 1 and 2
                    
            if game_state == "win":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos #at the time of click, assign the coordinates of the click to x and y variables
                    if SCREEN_WIDTH/2 - 80 <= x <= SCREEN_WIDTH/2 + 80 and SCREEN_HEIGHT/2 + 20 <= y <= SCREEN_HEIGHT/2 + 70: #check where the click coordinates was within the rectangular region
                        board = CreateBoard()
                        counter1, text1 = 120, '02:00' #reset the timer
                        game_state = "running"
                    elif SCREEN_WIDTH/2 - 60 <= x <= SCREEN_WIDTH/2 + 60 and SCREEN_HEIGHT/2 + 90 <= y <= SCREEN_HEIGHT/2 + 140:
                        sys.exit()

        if game_state == "win":
            DisplayWin(winner)

        pygame.display.update()


#player vs computer main game
def PlayPVC():
    global SoundOn, TimerOn
    pygame.display.set_caption("Pygame Player vs Computer")
    screen = pygame.display.set_mode((750,780))
    screen.fill(BLUE)

    board = CreateBoard()
    turn = 1

    SQUARESIZE = 100
    SCREEN_WIDTH = COLUMNS * SQUARESIZE+50 #750
    SCREEN_HEIGHT = (ROWS+1) * SQUARESIZE+80 #780
    CIRCLE_RADIUS = int(SQUARESIZE/2 - 5)
    MainFont = pygame.font.SysFont("arial", 90)
    SmallerFont = pygame.font.SysFont("arial", 30)
    homeImg = pygame.image.load("home.png")
    homeImg = pygame.transform.scale(homeImg,(55, 60))#change size of home icon
    

    game_state = "running"

    def ColumnFullCheck(board, column):#check if the top row of the column that the player chose is full
            if board[ROWS-1][column] == 0:
                    return True
            return False

    def ValidRowCheck(board, column):#for the column that the player chose, check what is the next open row from the bottom to top
            for r in range(ROWS):
                    if board[r][column] == 0:
                            return r

    def DropPiece(board, row, column, turn):#Drop the piece in the board using the column they chose and the next open row as coordinates
            board[row][column] = turn

    def WinCheck(board, turn):
            # Check horizontal win
            for c in range(COLUMNS-3):
                    for r in range(ROWS):
                            if board[r][c] == turn and board[r][c+1] == turn and board[r][c+2] == turn and board[r][c+3] == turn:
                                    return True
            # Check vertical win
            for c in range(COLUMNS):
                    for r in range(ROWS-3):
                            if board[r][c] == turn and board[r+1][c] == turn and board[r+2][c] == turn and board[r+3][c] == turn:
                                    return True
            # Check positive slope
            for c in range(COLUMNS-3):
                    for r in range(ROWS-3):
                            if board[r][c] == turn and board[r+1][c+1] == turn and board[r+2][c+2] == turn and board[r+3][c+3] == turn:
                                    return True
            # Check negative slope
            for c in range(COLUMNS-3):#start at 3 because its not possible to have a negative slope that goes down from the 3rd row because you need at least 4
                    for r in range(3, ROWS):
                            if board[r][c] == turn and board[r-1][c+1] == turn and board[r-2][c+2] == turn and board[r-3][c+3] == turn:
                                    return True
            return False
            
    def TieCheck(board):
            #Check tie
            for c in range(COLUMNS):
                    for r in range(ROWS):
                            if board[r][c] == 0:
                                    return False
            return True
    def DrawBoard(board):
            board = np.flip(board, 0)#flip the board so the (0,0) index starts at bottom left corner instead of top left
            screen.blit(homeImg, (25, 8)) #display the home icon image
            if SoundOn == 1: #if sound is on, load the volume on img, and if its off load the volume off image
                volumeImg = pygame.image.load("volume.png")
                volumeImg = pygame.transform.scale(volumeImg,(55, 60)) 
            else:
                volumeImg = pygame.image.load("volumeoff.png")
                volumeImg = pygame.transform.scale(volumeImg,(55, 60))
            screen.blit(volumeImg, (95, 8)) #display the volume image

            if TimerOn == 1:
                minutes = counter1 // 60  # Calculate minutes
                seconds = counter1 % 60  # Calculate seconds
                text1 = f"{minutes:02d}:{seconds:02d}"  # Format the text
                screen.fill(BLUE, (580, 20, 200, 45))
                screen.blit(TimerFont.render(text1, True, (0, 0, 0)), (580, 20))

            for c in range(COLUMNS): #draw 42 squares with a circle in each one to make the 6x7 board.
                    for r in range(ROWS):
                            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE+SQUARESIZE/4, r*SQUARESIZE+SQUARESIZE+80, SQUARESIZE, SQUARESIZE))

            for c in range(COLUMNS):
                    for r in range(ROWS):
                            if board[r][c] == 0: #draw different colored circles based on what piece is placed in the coordinate. If there is none, make it gray
                                    pygame.draw.circle(screen, GRAY, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)
                            elif board[r][c] == 1:
                                    pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)
                            else:
                                    pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+70), int(r*SQUARESIZE+SQUARESIZE+110)), CIRCLE_RADIUS)

            if game_state == "win":
                    DisplayWin(winner)

    def DisplayWin(winner):#create a square overlay which says the player who won and gives the options to quit game or replay
            pygame.draw.rect(screen, BLUE, pygame.Rect(0, 0, 750, 780))
            if winner == "Tie":
                    label = MainFont.render("It's a tie!", 1, RED)
                    screen.blit(label, (SCREEN_WIDTH/2-135, SCREEN_HEIGHT/2-100))
            elif winner == "Time":
                label = MainFont.render("Time's Up.", 1, RED)
                screen.blit(label, (SCREEN_WIDTH/2-190, SCREEN_HEIGHT/2-200))
                label = MainFont.render("It's a tie!.", 1, RED)
                screen.blit(label, (SCREEN_WIDTH/2-170, SCREEN_HEIGHT/2-100))
            else:
                    label = MainFont.render(f"{winner} wins!", 1, RED)
                    screen.blit(label, (SCREEN_WIDTH/2-280, SCREEN_HEIGHT/2-100))
            # Create "Play Again" button
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH/2 - 80, SCREEN_HEIGHT/2 + 20, 160, 50))#create a rectangle for the button, and display the text over it
            play_again_label = SmallerFont.render("Play Again", 1, BLUE)
            screen.blit(play_again_label, (SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 + 30))
            # Create "Quit" button
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH/2 - 60, SCREEN_HEIGHT/2 + 90, 120, 50))
            quit_label = SmallerFont.render("Quit", 1, BLUE)
            screen.blit(quit_label, (SCREEN_WIDTH/2 - 35, SCREEN_HEIGHT/2 + 100))
    def AnimateFallingPiece(column, turn): #animation of dropping the piece
            if row is not None: #check if the selected column is NOT full
                    starting_y = 80 #where the circle starts to drop from
                    ending_y = (ROWS - row) * SQUARESIZE - 50
                    current_y = starting_y
                    while current_y <= ending_y: #loop to check if the current y of the circle is less than the ending y(where the circle should stop moving)
                            screen.fill(BLUE, (0, 70, 800, 800))
                            DrawBoard(board)
                            if turn == 1:
                                    pygame.draw.circle(screen, RED, (int(column*SQUARESIZE+70), int(current_y+110)), CIRCLE_RADIUS)
                            else:
                                    pygame.draw.circle(screen, YELLOW, (int(column*SQUARESIZE+70), int(current_y+110)), CIRCLE_RADIUS)
                            pygame.display.update()
                            current_y = current_y + 4 
                            #this animation works by incremeenting the y position of the circle, which allows it to move downwards. The board redraws and the screen updaates until the current y reaches the ending y.
    player_turn = True #create a flag for player turn or else there are problems when using the turn variable
    is_paused1 = False  # Variable to track the timer's state
    counter1, text1 = 120, '02:00'
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Timer set to 1 second
    TimerFont = pygame.font.SysFont('Consolas', 45)   

    while True:
        DrawBoard(board)
        
        for event in pygame.event.get():  #pygame quit loop
            if event.type == pygame.QUIT:
                sys.exit()

            if game_state == "running": #what happens if a game is currently being played(no winner yet)
                if event.type == pygame.USEREVENT and not is_paused1 and TimerOn == 1:     
                    minutes = counter1 // 60  # Calculate minutes
                    seconds = counter1 % 60  # Calculate seconds
                    text1 = f"{minutes:02d}:{seconds:02d}"  # Format the text
                    counter1 -= 1
                    screen.fill(BLUE, (580, 20, 200, 45))
                    screen.blit(TimerFont.render(text1, True, (0, 0, 0)), (580, 20))                                                                        
                    if counter1 < 0:
                        winner= "Time"
                        game_state= "win"

                if event.type == pygame.MOUSEMOTION:  #moving your cursor around to move the circle at the top
                    Xpos, Ypos = event.pos #position of the cursor in the pygame window
                    if Ypos < 70: #check if the cursor is less than 200 because the top of the screen is for the home button and you cant move the circle when you move your cursor up
                        continue 
                    if turn == 1: #display a yellow or red circle in the top rectangle based on whose turn it is
                        pygame.draw.rect(screen, BLUE, (0, 65, SCREEN_HEIGHT, SQUARESIZE)) #make a rectangle where there is a circle displaying where the player is going to drop the circle
                        pygame.draw.circle(screen, RED, (Xpos, int(SQUARESIZE+15)), CIRCLE_RADIUS) #draw a circle above the rectangle
                    else:
                        pygame.draw.rect(screen, BLUE, (0, 65, SCREEN_HEIGHT, SQUARESIZE)) 
                        pygame.draw.circle(screen, YELLOW, (Xpos, int(SQUARESIZE+15)), CIRCLE_RADIUS)

                
                if event.type == pygame.MOUSEBUTTONDOWN: #drop yellow or red circle when p1 or p2 player chooses a column
                    Xpos, Ypos = event.pos
                    if Ypos < 70:
                        if 25 <= Xpos <= 80 and 8 <= Ypos <= 68:
                            OpenHomepage()
                            return
                        if 95 <= Xpos <= 150 and 8 <= Ypos <= 68: #click on the volume button
                            if SoundOn == 1: #if the volume is on, change soundON to 2
                                SoundOn = 2
                                pygame.draw.rect(screen, BLUE, (95, 8, 55, 60)) #draw a blue rectangle over the volume icon because you cant remove the blitted image
                            else:
                                SoundOn = 1
                                pygame.draw.rect(screen, BLUE, (95, 8, 55, 60))

                            if SoundOn == 2: #if SoundOn is 2, stop the music because soundOn == 2 means that volume is off
                                pygame.mixer.music.stop()
                            elif SoundOn == 1:  
                                pygame.mixer.music.load("Connect4Music.mp3")   
                                pygame.mixer.music.play(-1)      
                        continue #ignore click event if the coordinate was less than 200
                
                if player_turn: #player 1   
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        Xpos = event.pos[0]
                        column = int(math.floor(Xpos/SQUARESIZE)) #calculate the column index dividing the x coordinate of the mouse click and the squarsize(100). Then floor the number to the nearest whole number
                        if column == 7:#after the calculation, need to check if the column is 7 because it cant be more than 6(or else crash) since the column array is from 0-6
                            column = column-1

                        if not ColumnFullCheck(board, column): #if column is not full, continue to the next code, or else stay until they choose a column thats not full
                            continue
                        row = ValidRowCheck(board, column)
                        AnimateFallingPiece(column, turn)
                        DropPiece(board, row, column, turn)#set row to the next open row in the column the player chose

                        if WinCheck(board, turn): #before changing turn, check if there is a winner. Ff there is a winner, assign the winner to the "winner" variable
                            if turn == 1:
                                winner = "Player 1"
                                game_state = "win"
                            else:
                                winner = "Player 2"
                                game_state = "win"
                        if TieCheck(board):
                            winner = "Tie"
                            game_state = "win"
                        player_turn = False
                        turn = 3-turn    
                        
                else:
                    column = random.randint(0,6) #use random randint to choose a random column from 0-6(1-7)
                    if not ColumnFullCheck(board, column):
                        continue
                    row = ValidRowCheck(board, column)
                    AnimateFallingPiece(column, turn)
                    DropPiece(board, row, column, turn)
                    if WinCheck(board, turn): 
                        if turn == 1:
                            winner = "Player 1"
                            game_state = "win"
                        else:
                            winner = "Player 2"
                            game_state = "win"
                    if TieCheck(board):
                        winner = "Tie"
                        game_state = "win"
                    player_turn = True
                    turn = 3-turn
        
            if game_state == "win": #in the display winner screen, handle click events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos #at the time of click, assign the coordinates of the click to x and y variables
                    if SCREEN_WIDTH/2 - 80 <= x <= SCREEN_WIDTH/2 + 80 and SCREEN_HEIGHT/2 + 20 <= y <= SCREEN_HEIGHT/2 + 70: #check where the click coordinates was within the rectangular region
                        board = CreateBoard()
                        game_state = "running"
                        counter1, text1 = 120, '02:00' #reset the timer
                    elif SCREEN_WIDTH/2 - 60 <= x <= SCREEN_WIDTH/2 + 60 and SCREEN_HEIGHT/2 + 90 <= y <= SCREEN_HEIGHT/2 + 140:
                        sys.exit()

        if game_state == "win": #if the game state is win, display the winner
            DisplayWin(winner)

        pygame.display.update()


def OpenHomepage():
    text_font=pygame.font.SysFont("Sriracha",90)
    text_font2=pygame.font.SysFont("Sriracha",40)
    pygame.display.set_caption("Connect 4 Menu")
    screen = pygame.display.set_mode((1200,800)) #change screen dimensions
    def draw_text(text, font, text_col,x,y):
        img=font.render(text,True,text_col)
        screen.blit(img,(x,y))
    
    def OpenSettings():
        global SoundOn, TimerOn #global the variables since the variables are assigned outside of the function, which means they are local. global variables make the variable accessible throughout the program
        SettingsWindow=pygame.Rect((300,250,600,400))
        SettingsExitbutton=pygame.Rect((850,250,50,30))
        SelectionBoxSound=pygame.Rect((775,415,100,40))
        SelectionBoxTimer=pygame.Rect((775,515,100,40))
        while True: #while loop for the settings menu
            pygame.draw.rect(screen,(246,178,107,100), SettingsWindow)
            pygame.draw.rect(screen,(204,0,0,100), SettingsExitbutton)
            draw_text("Settings",text_font,(0,0,0),325,240) 
            draw_text("Sound",text_font2,(0,0,0),320,400) 
            draw_text("Timer",text_font2,(0,0,0),320,500)       

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Xpos, Ypos = event.pos
                    if SettingsExitbutton.collidepoint(Xpos, Ypos):
                        return  # Exit settings if you click on the settings exit button
                    elif SelectionBoxSound.collidepoint(Xpos, Ypos):
                    #toggle sound settings
                        if SoundOn == 1:
                            SoundOn = 2
                        else:
                            SoundOn = 1

                        if SoundOn == 2:
                            pygame.mixer.music.stop()
                        elif SoundOn == 1:  
                            pygame.mixer.music.load("Connect4Music.mp3")   
                            pygame.mixer.music.play(-1)   
                    elif SelectionBoxTimer.collidepoint(Xpos, Ypos):
                        # toggle timer settings
                        if TimerOn == 1:
                            TimerOn = 2
                        else:
                            TimerOn = 1
                    elif Xpos>400 and Xpos<800 and Ypos>700 and Ypos<775: #quit game
                          sys.exit()

            if SoundOn==1: #change the box color and the text (on/off)
                    pygame.draw.rect(screen,(100,206,55,100), SelectionBoxSound)   
                    draw_text("ON",text_font2,(0,0,0),780,400)       
            else:
                    pygame.draw.rect(screen,(204,0,0,100), SelectionBoxSound)   
                    draw_text("OFF",text_font2,(0,0,0),780,400)
                    pygame.mixer.stop()
            if TimerOn==1:
                    pygame.draw.rect(screen,(100,206,55,100), SelectionBoxTimer) 
                    draw_text("ON",text_font2,(0,0,0),780,500)                
            else:
                    pygame.draw.rect(screen,(204,0,0,100), SelectionBoxTimer)
                    draw_text("OFF",text_font2,(0,0,0),780,500)
            
                    
            pygame.display.update()

    while True: #main while loop for the home menu
        screen.fill(YELLOW)
        BlueRectHome= pygame.Rect((0,0,200,800))
        BlueRectHome2= pygame.Rect((1000,0,200,800))
        pygame.draw.rect(screen,(74,134,232,100), BlueRectHome)    
        pygame.draw.rect(screen,(74,134,232,100), BlueRectHome2)        
        #Side circles for design
        pygame.draw.circle(screen,(241,194,50,100),(100,50),45)
        pygame.draw.circle(screen,(204,0,0,100),(100,150),45) 
        pygame.draw.circle(screen,(241,194,50,100),(100,250),45)
        pygame.draw.circle(screen,(204,0,0,100),(100,350),45)  
        pygame.draw.circle(screen,(241,194,50,100),(100,450),45)
        pygame.draw.circle(screen,(204,0,0,100),(100,550),45) 
        pygame.draw.circle(screen,(241,194,50,100),(100,650),45)
        pygame.draw.circle(screen,(204,0,0,100),(100,750),45)
        #Side circles on the other side for design
        pygame.draw.circle(screen,(241,194,50,100),(1100,50),45)
        pygame.draw.circle(screen,(204,0,0,100),(1100,150),45) 
        pygame.draw.circle(screen,(241,194,50,100),(1100,250),45)
        pygame.draw.circle(screen,(204,0,0,100),(1100,350),45)  
        pygame.draw.circle(screen,(241,194,50,100),(1100,450),45)
        pygame.draw.circle(screen,(204,0,0,100),(1100,550),45) 
        pygame.draw.circle(screen,(241,194,50,100),(1100,650),45)
        pygame.draw.circle(screen,(204,0,0,100),(1100,750),45) 
        pygame.draw.ellipse(screen,(204,0,0,100),(300,50,600,120)) 
        draw_text("Connect 4",text_font,(0,0,0),385,30)        

        PVPButton= pygame.Rect((400,250,400,75))
        PVCButton= pygame.Rect((400,400,400,75))
        SettingsButton= pygame.Rect((400,550,400,75))
        QuitGameButton= pygame.Rect((400,700,400,75))
        PVPButton2= pygame.Rect((410,260,400,75))
        PVCButton2= pygame.Rect((410,410,400,75))
        SettingsButton2= pygame.Rect((410,560,400,75))
        QuitGameButton2= pygame.Rect((410,710,400,75))
        pygame.draw.rect(screen,(246,178,107,100), PVPButton)
        pygame.draw.rect(screen,(246,178,107,100), PVCButton) 
        pygame.draw.rect(screen,(246,178,107,100), SettingsButton)    
        pygame.draw.rect(screen,(246,178,107,100), QuitGameButton)
        pygame.draw.rect(screen,(255,140,46,100), PVPButton2)
        draw_text("Player V Player",text_font2,(0,0,0),413,260)
        pygame.draw.rect(screen,(255,140,46,100), PVCButton2)
        draw_text("Player V Computer",text_font2,(0,0,0),413,410)    
        pygame.draw.rect(screen,(255,140,46,100), SettingsButton2)
        draw_text("Settings",text_font2,(0,0,0),413,560)    
        pygame.draw.rect(screen,(255,140,46,100), QuitGameButton2) 
        draw_text("Quit Game",text_font2,(0,0,0),413,710) 

            

        for event in pygame.event.get():  #pygame quit loop
            if event.type == pygame.QUIT:
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN: 
                Xpos, Ypos = event.pos
                if Xpos>=410 and Xpos<=800 and Ypos>=260 and Ypos<=335: #call differnet functions based on where the user clicked
                    PlayPVP()
                elif Xpos>=410 and Xpos<=800 and Ypos>=410 and Ypos<=485:
                    PlayPVC()
                elif Xpos>=410 and Xpos<=800 and Ypos>=560 and Ypos<=635:
                    OpenSettings()
                elif Xpos>=410 and Xpos<=800 and Ypos>=710 and Ypos<=785:
                    sys.exit()

        pygame.display.update()

OpenHomepage()#start the game