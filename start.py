# import platform
import time
import random
import pygame as pg
import pygame_widgets as pw
from pygame_widgets.textbox import TextBox
# import class objects
from battleship.button import ClickableButton
from battleship.board import Board
from enum import Enum
import os
import re
from battleship.board import Ship

DEBUG = True

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MIDDLE = pg.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
BACKGROUND = pg.Surface(SCREEN.get_size()).convert()
CLOCK = pg.time.Clock() # keep to limit framerate
fps=30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

num_ships = None
lvl_of_play = None
game_over = False
winner = 0

def draw_board(board, x_offset, y_offset):
    # TODO
    my_font = pg.font.Font(pg.font.get_default_font(), 36)
    GRID_SIZE = 10
    CELL_SIZE = 60
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pg.Rect(x_offset + x * CELL_SIZE, y_offset + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(BACKGROUND, (0, 0, 0), rect, 1)
            if board.gameBoard[y][x] == -1: #-1 on the grid indicates a miss
                pg.draw.circle(BACKGROUND, (0,0,255), rect.center, CELL_SIZE // 4)
            elif board.gameBoard[y][x] == -2: #-2 on the grid indicates a hit
                pg.draw.circle(BACKGROUND, (255, 0, 0), rect.center, CELL_SIZE // 4)
            #elif isinstance(board.grid[y][x], Ship) and not hide_ships:
                #pg.draw.rect(screen, GRAY, rect)
    SCREEN.blit(BACKGROUND, (0,0))


def start_game():
    globals().update(game_over=False)

    running = True
    startBtn = ClickableButton("Start", (250, 100), (MIDDLE.x - 125, MIDDLE.y + 200))

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN]) #added event set for performance
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        BACKGROUND.fill("grey")
        SCREEN.fill("grey")

        img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
        img.convert()
        img_size = img.get_size()
        BACKGROUND.blit(img, (MIDDLE.x - img_size[0]/2, 100))

        if not startBtn.clicked:
            startBtn.draw(BACKGROUND, events)
            startBtn.btn.show()
            startBtn.btn.enable()
        else:
            running = False
            # make start button is disabled
            startBtn.btn.hide()
            startBtn.btn.disable()


        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()
        #pg.display.update()

        tick = CLOCK.tick(30) # limits FPS to 60

    return True

def choose_gamemode():
    running = True
    def txtCb(txt):
        text = ''.join(txt)
        match = re.match("[1-5]", text)
        if match:
            print(f"num ships: {match[0]}")
            globals().update(num_ships=int(match[0]))

    shipTxtbox = TextBox(BACKGROUND, MIDDLE.x - 30, MIDDLE.y + 200, 60, 80, fontSize=50, onSubmit=txtCb)
    shipTxtbox.onSubmitParams = [shipTxtbox.text]

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        BACKGROUND.fill("grey")
        SCREEN.fill("grey")

        if not num_ships:
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            BACKGROUND.blit(img, (MIDDLE.x - img_size[0]/2, 100))

            my_font = pg.font.Font(pg.font.get_default_font(), 36)
            text_surface = my_font.render('Choose number of ships [1-5]', True, (0, 0, 0))
            BACKGROUND.blit(text_surface, (MIDDLE.x - text_surface.get_width()/2, MIDDLE.y + 150))

            shipTxtbox.draw()
            shipTxtbox.show()
            shipTxtbox.enable()
        else:
            running = False
            shipTxtbox.hide()
            shipTxtbox.disable()

        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()
        #pg.display.update()

        tick = CLOCK.tick(60) # limits FPS to 60
    
    return True

MARGIN = 50
X_OFFSET = 360
CELL_SIZE = 60
GRID_SIZE = 10

def choose_level_of_play():
    running = True
    def txtCb_2(txt):
        text = ''.join(txt)
        match = re.match("[1-4]", text)
        if match:
            print(f"difficulty: {match[0]}")
            globals().update(lvl_of_play=int(match[0]))

    levelofPlay = TextBox(BACKGROUND, MIDDLE.x - 30, MIDDLE.y + 200, 60, 80, fontSize=50, onSubmit=txtCb_2)
    levelofPlay.onSubmitParams = [levelofPlay.text]

    while running:
        # poll for events
        # pg.QUIT event means the user clicked X to close the window
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                return False
        
        BACKGROUND.fill("grey")
        SCREEN.fill("grey")

        if not lvl_of_play:
            img = pg.image.load(os.path.join("data/battleship_fontbolt.png"))
            img.convert()
            img_size = img.get_size()
            BACKGROUND.blit(img, (MIDDLE.x - img_size[0]/2, 100))

            my_font = pg.font.Font(pg.font.get_default_font(), 36)
            text_surface = my_font.render('Choose level of play [1-4] (2-4 for AI)', True, (0, 0, 0))
            BACKGROUND.blit(text_surface, (MIDDLE.x - text_surface.get_width()/2, MIDDLE.y + 150))

            levelofPlay.draw()
            levelofPlay.show()
            levelofPlay.enable()
        else:
            running = False
            levelofPlay.hide()
            levelofPlay.disable()

        SCREEN.blit(BACKGROUND, (0, 0))
        pw.update(events)  # Call once every loop to allow widgets to render and listen
        
        # flip() the display to put the work we did on screen
        pg.display.flip()
        #pg.display.update()

        tick = CLOCK.tick(60) # limits FPS to 60
    
    return True

MARGIN = 50
X_OFFSET = 360
CELL_SIZE = 60
GRID_SIZE = 10

def player_place_ships(screen, board, clock):
    """
    Outline for the rest of functionality
    Place Ship object
    Confirm placement
    Change screen to a blank screen with a button that says
    'Player two press to start turn'
    Swithces to Player 2 start state when clicked
    """
    ships = [Ship(i+1) for i in range(num_ships)]  # Add ship sizes based on your design
    font = pg.font.Font(None, 36)

    for ship in ships:
        placing = True
        horizontal = True

        invalid_placement = None
        while placing:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    return False
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    grid_x = (x - X_OFFSET) // CELL_SIZE
                    grid_y = (y - MARGIN) // CELL_SIZE
                    if DEBUG:
                        print(f"({x}, {y})")
                        print(f"({grid_x}, {grid_y})")
                    
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        if board.place_ship(ship, grid_x, grid_y, horizontal):
                            placing = False
                            invalid_placement = None
                        else:
                            invalid_placement = True
                            print(f"Invalid placement at ({grid_x}, {grid_y}), horizontal: {horizontal}")
                
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        horizontal = not horizontal
            
            screen.fill("grey")
            BACKGROUND.fill("grey")
            screen.blit(BACKGROUND, (0, 0))
            draw_board(board, X_OFFSET, MARGIN)

            # Draw ship preview
            mouse_x, mouse_y = pg.mouse.get_pos()
            grid_x = (mouse_x) // CELL_SIZE
            grid_y = (mouse_y - MARGIN) // CELL_SIZE

            if 0 <= (mouse_x - X_OFFSET) // CELL_SIZE < GRID_SIZE and 0 <= (mouse_y - MARGIN) // CELL_SIZE < GRID_SIZE:
                can_place = True
                if horizontal:
                    gx = (mouse_x - X_OFFSET) // CELL_SIZE
                    gy = (mouse_y - MARGIN) // CELL_SIZE
                    if gx + ship.size > 10: #10 is the grid size
                        can_place = False
                    try:
                        for i in range(ship.size):
                            if board.gameBoard[gy][gx + i] != 0:
                                can_place=False
                    except:
                        can_place = False
                else:
                    gx = (mouse_x - X_OFFSET) // CELL_SIZE
                    gy = (mouse_y - MARGIN) // CELL_SIZE
                    if gy + ship.size > 10: # 10 is the grid size
                        can_place=False
                    try:
                        for i in range(ship.size):
                            if board.gameBoard[gy + i][gx] != 0:
                                can_place=False
                    except:
                        can_place = False
                preview_color = "green" if can_place else "red"
                if horizontal:
                    pg.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, ship.size * CELL_SIZE, CELL_SIZE), 2)
                else:
                    pg.draw.rect(screen, preview_color, (grid_x * CELL_SIZE, MARGIN + grid_y * CELL_SIZE, CELL_SIZE, ship.size * CELL_SIZE), 2)

            # Draw instructions
            text = font.render(f"Place your ship of size {ship.size}. Press SPACE to rotate.", True, "white")
            screen.blit(text, (10, 10))
            if invalid_placement is not None:
                text = font.render(f"Invalid placement!", True, "red")
                screen.blit(text, (10, 300))
            
            pg.display.flip()
            #pg.display.update()

def auto_place_ships(screen, board, clock):
    """
    Place Ship object by AI module
    Took player_place_ships, removed pg_event_get since everything is handled automatically
    removed lines of code that showed where ships are placed
    the rest of the logic is the same as player_place_ships
    """
    ships = [Ship(i+1) for i in range(num_ships)]  # Add ship sizes based on your design
    font = pg.font.Font(None, 36)

    for ship in ships:
        placing = True
        horizontal = True

        invalid_placement = None
        while placing:
                
            grid_x = random.randint(0, 9)
            grid_y = random.randint(0, 9)
            orientation = random.choice([1, 2])

            if orientation == 1:
               horizontal = horizontal
            elif orientation == 2:
               horizontal = not horizontal
                
            if DEBUG:
                #print(f"({x}, {y})")
                print(f"({grid_x}, {grid_y})")
                    
            if board.place_ship(ship, grid_x, grid_y, horizontal):
                    placing = False
                    invalid_placement = None
            else:
                    invalid_placement = True
                        
            
    screen.fill("grey")
    BACKGROUND.fill("grey")
    screen.blit(BACKGROUND, (0, 0))
    draw_board(board, X_OFFSET, MARGIN)


#def transition_between_turns(pnum):
    """
    Display whose turn it is, then wait until the enter
    button is pushed for confirmation to show that players
    attack/self board
    """
    #hold = True
    #while hold:
        #pg.event.set_allowed([pg.QUIT, pg.KEYDOWN]) #added event set to improve performance
        #for event in pg.event.get():
            #if event.type == pg.QUIT:
                #pg.quit()
                #return False
            #if event.type == pg.KEYDOWN:
                #if event.key == pg.K_RETURN:
                    #return

        #font = pg.font.Font(pg.font.get_default_font(), 48)
        #SCREEN.fill("grey")
        #BACKGROUND.fill("grey")
        #text = font.render(f"Player {pnum}'s Turn Press Enter to continue", True, "white")
        #text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        #BACKGROUND.blit(text, text_rect)
        #SCREEN.blit(BACKGROUND, (0,0))

        #events = pg.event.get()
        #pw.update(events)  # Call once every loop to allow widgets to render and listen

        #pg.display.flip()
        #pg.display.update()

def updated_transition_between_turns(pnum):
    """
    Display whose turn it is, then wait until the enter
    button is pushed for confirmation to show that players
    attack/self board
    updated routine to improve performance
    """
    #hold = True
    #while hold:
        #pg.event.set_allowed([pg.QUIT, pg.KEYDOWN]) #added event set to improve performance
        #for event in pg.event.get():
            #if event.type == pg.QUIT:
                #pg.quit()
                #return False
            #if event.type == pg.KEYDOWN:
                #if event.key == pg.K_RETURN:
                    #return

    font = pg.font.Font(pg.font.get_default_font(), 48)
    SCREEN.fill("grey")
    BACKGROUND.fill("grey")
    text = font.render(f"Player {pnum}'s Turn Press Enter to continue", True, "white")
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    BACKGROUND.blit(text, text_rect)
    SCREEN.blit(BACKGROUND, (0,0))

    #events = pg.event.get()
    #pw.update(events)  # Call once every loop to allow widgets to render and listen

    pg.display.flip()
    #pg.display.update()
    time.sleep(2)

def check_victory(board):
    for row in board.gameBoard:
        for cell in row:
            if cell == 1:
                return False  # If there is at least one ship that hasn't been hit, no victory yet.
    return True  # If all ships have been hit, declare victory.

def player_turn(board, pnum):
    '''
    Look at hits on their board
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 2 turn
    '''
    attacking = True
    hit = False
    while attacking:
        pg.event.set_allowed([pg.QUIT, pg.MOUSEBUTTONDOWN]) #added event set for performance
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                return False

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                grid_x = (x - X_OFFSET) // CELL_SIZE  # Adjust grid based on offset and cell size
                grid_y = (y - MARGIN) // CELL_SIZE

                if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                    cell_value = board.gameBoard[grid_y][grid_x]
                    if cell_value == 0:  # Miss
                        print(f"Miss at ({grid_x}, {grid_y})")
                        board.gameBoard[grid_y][grid_x] = -1
                        attacking = False  # End turn after miss
                    elif isinstance(cell_value, Ship) or cell_value > 0:  # Hit
                        print(f"Hit at ({grid_x}, {grid_y})")
                        board.gameBoard[grid_y][grid_x] = -2
                        hit = True
                        # Check if the game is over
                        if check_victory(board):
                            globals().update(game_over=True)
                            globals().update(winner=pnum)
                            print("Player {pnum} wins!")
                            return True
                        else:
                            attacking = False  # End turn after a successful hit
                    else:
                        print("Already attacked this cell")

        draw_board(board, X_OFFSET, MARGIN)
        pg.display.flip()
        #pg.display.update()
        CLOCK.tick(60)
    return hit

def auto_attack_lvl2(board, pnum):
    '''
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 1 turn
    '''
    attacking = True
    hit = False
    while attacking:

        grid_x = random.randint(0, 9)
        grid_y = random.randint(0, 9)

        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            cell_value = board.gameBoard[grid_y][grid_x]
            if cell_value == 0:  # Miss
                print(f"Miss at ({grid_x}, {grid_y})")
                board.gameBoard[grid_y][grid_x] = -1
                attacking = False  # End turn after miss
            elif isinstance(cell_value, Ship) or cell_value > 0:  # Hit
                print(f"Hit at ({grid_x}, {grid_y})")
                board.gameBoard[grid_y][grid_x] = -2
                hit = True
                        # Check if the game is over
                if check_victory(board):
                    globals().update(game_over=True)
                    globals().update(winner=pnum)
                    print("Player {pnum} wins!")
                    return True
                else:
                    attacking = False  # End turn after a successful hit
            else:
                print("Already attacked this cell")

        draw_board(board, X_OFFSET, MARGIN)
        pg.display.flip()
        #pg.display.update()
        CLOCK.tick(60)

    return hit

def auto_attack_lvl3(board, pnum):
    '''
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 1 turn
    '''
    attacking = True
    hit = False
    needs_break = False
    found = False
    new_x = -1
    new_y = -1
    while attacking:

        for y in range (0, 10):
            for x in range (0, 10):
                cell_value = board.gameBoard[y][x]
                if cell_value == -2:  # There is a ship placed at this location
                    new_x, new_y, found = return_adj(board, x, y)
                    if found:
                        print("attack adjacent cell success", new_x, new_y)
                        needs_break = True
                        cell_value = board.gameBoard[new_y][new_x]
                        if cell_value == 0:
                            print("miss")
                            board.gameBoard[new_y][new_x] = -1
                            attacking = False
                        elif cell_value == 1:
                            print("hit")
                            board.gameBoard[new_y][new_x] = -2
                            hit = True
                            attacking = False
                            if check_victory(board):
                                globals().update(game_over=True)
                                globals().update(winner=pnum)
                                print(f"Player {pnum} wins!")
                                return True
                        else:
                            attacking = True
                    else:
                        print("no targets found")
                if needs_break:
                    break
            if needs_break:
                break
        if not found: 
            hit = auto_attack_lvl2(board, pnum)  
            attacking = False  
            
    
        draw_board(board, X_OFFSET, MARGIN)
        pg.display.flip()
        #pg.display.update()
        CLOCK.tick(30)

    time.sleep(1.5)

    return hit

def auto_attack_lvl4(board, pnum):
    '''
    subroutine to automatically guess player 1 ships
    Moves to attack phase and confirms hits
    Check victory condition
    on miss switch to transition screen
    switch to player 1 turn
    '''
    attacking = True
    hit = False
    needs_break = False
    while attacking:

        for y in range (0, 10):
            for x in range (0, 10):
                cell_value = board.gameBoard[y][x]
                if cell_value == 1:  # There is a ship placed at this location
                    board.gameBoard[y][x] = -2
                    print(f"Hit at ({x}, {y})")
                    #attacking = False  # End turn after miss
                    hit = True
                    attacking = False
                    needs_break = True
                    break
            if needs_break:
                break
            #elif isinstance(cell_value, Ship) or cell_value > 0:  # Hit
                #print(f"Hit at ({grid_x}, {grid_y})")
                #board.gameBoard[grid_y][grid_x] = -2
                #hit = True
                        # Check if the game is over
    if check_victory(board):
        globals().update(game_over=True)
        globals().update(winner=pnum)
        print("Player {pnum} wins!")
        return True
    #else:
        #attacking = False  # End turn after a successful hit
        #else:
            #print("Already attacked this cell")

    draw_board(board, X_OFFSET, MARGIN)
    pg.display.flip()
    #pg.display.update()
    CLOCK.tick(60)

    return hit

def return_adj(board, x, y):
    #looks for adjacent cells, locations that haven't been attacked
    #if a cell contains 0 or 1, can be attacked. Returns coordinates of the cell 
    can_attack = None
    new_x = x
    new_y = y


    if y < 9 and board.gameBoard[y+1][x] > -1:      #bounds checking 
        new_y = y+1
        can_attack = True
        return new_x, new_y, can_attack
    elif x < 9 and board.gameBoard[y][x+1] > -1:
        new_x = x+1
        can_attack = True
        return new_x, new_y, can_attack
    elif y > 0 and board.gameBoard[y-1][x] > -1:
        new_y = y-1
        can_attack = True
        return new_x, new_y, can_attack
    elif x > 0 and board.gameBoard[y][x-1] > -1:
        new_x = x-1
        can_attack = True
        return new_x, new_y, can_attack
    else:
        can_attack = False
        return new_x, new_y, can_attack
    

def display_attack_result(attacking_player, hit):
    font = pg.font.Font(None, 60)
    if hit:
        text = font.render("Hit!", True, RED)
    else:
        text = font.render("Miss!", True, BLUE)
    text_rect = text.get_rect(center=(MIDDLE.x, MIDDLE.y))
    SCREEN.blit(text, text_rect)
    pg.display.flip()
    #pg.display.update()
    time.sleep(1.5)  # Display the result for 1.5 seconds

def run():
    # pygame setup
    pg.init()
    # set screen size
    pg.display.set_caption("Battleship")

    SCREEN.fill("grey")
    BACKGROUND.fill("grey")
    SCREEN.blit(BACKGROUND, (0,0))
    pg.display.update()

    running = True # track if loop should keep running

    player1_board = Board() # Initializes both players boards
    player2_board = Board()

    if not start_game():
        return -1

    if not choose_gamemode():
        return -1
    
    if not choose_level_of_play():
        return -1


    player_place_ships(SCREEN, player1_board, CLOCK)
    updated_transition_between_turns(2)
    #player_place_ships(SCREEN, player2_board, CLOCK)
    if lvl_of_play > 1:
        auto_place_ships(SCREEN, player2_board, CLOCK)
    else:
        player_place_ships(SCREEN, player1_board, CLOCK)

    global game_over
    while not game_over:
        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        updated_transition_between_turns(1)
        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        hit = player_turn(player2_board, 1)
        #hit = auto_attack_lvl2(player2_board, 1)
        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        display_attack_result(1, hit)

        if DEBUG:
            print(player1_board.gameBoard)
            print(player2_board.gameBoard)

        if game_over:
            break

        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        updated_transition_between_turns(2)
        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        #hit = player_turn(player1_board, 2)
        if lvl_of_play == 1:
            hit = player_turn(player1_board, 2)
        elif lvl_of_play ==2:
            hit = auto_attack_lvl2(player1_board, 2)
        elif lvl_of_play == 3:
            hit = auto_attack_lvl3(player1_board, 2)
        else:
            hit = auto_attack_lvl4(player1_board, 2)

        BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
        SCREEN.fill("grey")
        SCREEN.blit(BACKGROUND, (0, 0))
        display_attack_result(2, hit)

        if DEBUG:
            print(player1_board.gameBoard)
            print(player2_board.gameBoard)

        if game_over:
            break

    # clear board
    BACKGROUND.fill("grey") # These calls here need to be moved since they are interfering with the draw_board
    SCREEN.fill("grey")
    SCREEN.blit(BACKGROUND, (0, 0))
    # display winner
    font = pg.font.Font(None, 60)
    text = font.render(f"Game Over! Winner: Player {winner}", True, BLUE)
    text_rect = text.get_rect(center=(MIDDLE.x, MIDDLE.y))
    SCREEN.blit(text, text_rect)
    pg.display.flip()
    #pg.display.update()
    time.sleep(1.5)  # Display the result for 1.5 seconds

    pg.quit()
    return 0 # returned in good state

def main():
    # run main loop
    exit_state = run()
    print(f"Exited with state {exit_state}")

if __name__ == "__main__":
    main()
