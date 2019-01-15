from random import randint

from turtle import *


def init_board():
    board = []
    for x in range(0, 8):
        board.append([0] * 8)
        tiles = [[0, 0, 2, 2], [2, 0, 2, 2], [4, 0, 3, 2], [7, 0, 1, 2], [0, 2, 3, 2], [3, 2, 2, 2], [5, 2, 2, 2],
                 [7, 2, 1, 2], [0, 4, 3, 2], [3, 4, 3, 2], [6, 4, 2, 2], [0, 6, 3, 1], [3, 6, 3, 1], [6, 6, 2, 1],
                 [0, 7, 3, 1], [3, 7, 3, 1], [6, 7, 2, 1]]
    print_board(board)
    return board, tiles




def check_move_h(x, y, tiles, board, seqC, seqH):
    h_tile = find_tile(x, y, tiles)
    last_move = seqC[-1]
    last_x = last_move[0]
    last_y = last_move[1]
    if h_tile == find_tile(last_x, last_y, tiles):
        print("Invalid Tile!")
    elif board[x][y] != 0:
        print("Space occupied!")
    elif x == last_x or y == last_y:
        board[x][y] = 2
        draw_move(x, y, 2)
        seqH.append([x, y])
    else:
        print("Invalid Move!")

    # sequence1 contains tile AND coordinates
    return board, seqH




def find_tile(x, y, tiles):
    for tile in tiles:
        if x in range(tile[0], tile[0] + tile[2]) and y in range(tile[1], tile[1] + tile[3]):
            return tile


def gen_moves(last_x, last_y, tiles, board):
    moves = []
    last_tile = find_tile(last_x, last_y, tiles)
    for x in range(0, 8):
        if board[x][last_y] == 0 and find_tile(x, last_y, tiles) != last_tile:
            moves.append([x, last_y])
    for y in range(0, 8):
        if board[last_x][y] == 0 and find_tile(last_x, y, tiles) != last_tile:
            moves.append([last_x, y])
    return moves


def print_board(board):
    # print("\n")
    for y in range(7, -1, -1):
        for x in range(0, 8):
            print(board[x][y], end=" ")
        print("")


def draw_board():
    speed(0)
    color('black', 'wheat')
    begin_fill()
    up()
    goto(-300, -300)
    down()
    forward(600)
    left(90)
    forward(600)
    left(90)
    forward(600)
    left(90)
    forward(600)
    left(90)
    end_fill()

    for i in range(0, 8):
        forward(600)
        up()
        goto(-300, 75 * (i + 1) - 300)
        down()

    left(-90)
    for i in range(0, 8):
        forward(600)
        up()
        goto(75 * (i + 1) - 300, 300)
        down()
    speed(3)


def draw_move(x, y, p):
    speed(0)
    if p == 1:
        color('red')
    else:
        color('black')
    begin_fill()
    up()
    goto(75 * x - 300 + 20, 75 * y - 300 + 37)
    down()
    circle(15)
    end_fill()
    up()
    goto(-400, -400)
    speed(3)


def draw_tiles(tiles):
    speed(10)
    color('blue')
    pensize(5)
    for tile in tiles:
        x = tile[0]
        y = tile[1]
        length = tile[2]
        height = tile[3]
        up()
        goto(75 * x - 300 + 5, 75 * y - 300 + 5)
        down()
        setheading(0)
        forward(75 * length - 10)
        left(90)
        forward(75 * height - 10)
        left(90)
        forward(75 * length - 10)
        left(90)
        forward(75 * height - 10)
    speed(3)


def score_board(board, tiles):
    score1 = 0
    score2 = 0
    for tile in tiles:
        t1 = 0
        t2 = 0
        xstart = tile[0]
        ystart = tile[1]
        length = tile[2]
        height = tile[3]
        for x in range(xstart, xstart + length):
            for y in range(ystart, ystart + height):
                if board[x][y] == 1:
                    t1 = t1 + 1
                elif board[x][y] == 2:
                    t2 = t2 + 1
        if t1 > t2:
            score1 = score1 + length * height
        elif t2 > t1:
            score2 = score2 + length * height
    #print(score1, score2)
    return score1, score2


def best_move(moves, board, tiles, p):
    biggest = -1000
    best_move = moves[0]
    if p == 1:
        a=0
        b=1
    else:
        a=1
        b=0
    for move in moves:
        temp_board = board
        temp_board[move[0]][move[1]] = p
        scores = score_board(temp_board, tiles)
        if scores[a] - scores[b] > biggest:
            biggest = scores[a] - scores[b]
            best_move = move
        #print(move, best_move, biggest)
        temp_board[move[0]][move[1]] = 0
    return best_move


def play_kulami_AI():
    seqC = []
    seqH = []
    [board, tiles] = init_board()
    draw_board()
    draw_tiles(tiles)
    seqC = [[randint(0, 7), randint(0, 7)]]
    #print(seqC)
    board[seqC[-1][0]][seqC[-1][1]] = 1
    draw_move(seqC[-1][0], seqC[-1][1], 1)
    #print_board(board)
    while len(seqC) <= 28:
        inputx = int(input('enter an x coordinate: '))-1
        inputy = int(input('enter a y coordinate: '))-1
        [board, seqH] = check_move_h(inputx, inputy, tiles, board, seqC, seqH)
        #print_board(board)
        #print(seqC, seqH)
        if seqH:
            moves = gen_moves(seqH[-1][0], seqH[-1][1], tiles, board)
        else:
            moves = []
        # print (moves)
        if moves:
            com_move = best_move(moves, board, tiles, 1)
        # com_move = moves[randint(0,len(moves)-1)]
            board[com_move[0]][com_move[1]] = 1
            draw_move(com_move[0], com_move[1], 1)
            seqC.append(com_move)
        # print(moves)
            print(com_move[0]+1,',',com_move[1]+1)        #print_board(board)
        print('Move ', len(seqC),".", score_board(board,tiles))
    final_score = score_board(board, tiles)
    print("Good game! The score was: ", final_score[0], "to ", final_score[1])

def play_kulami_rand():
    seqC = []
    seqH = []
    [board, tiles] = init_board()
    draw_board()
    draw_tiles(tiles)
    seqC = [[randint(0, 7), randint(0, 7)]]
    #print(seqC)
    board[seqC[-1][0]][seqC[-1][1]] = 1
    draw_move(seqC[-1][0], seqC[-1][1], 1)
    #print_board(board)
    while len(seqC) <= 28:
        inputx = int(input('enter an x coordinate: '))-1
        inputy = int(input('enter a y coordinate: '))-1
        [board, seqH] = check_move_h(inputx, inputy, tiles, board, seqC, seqH)
        #print_board(board)
        #print(seqC, seqH)
        if seqH:
            moves = gen_moves(seqH[-1][0], seqH[-1][1], tiles, board)
        else:
            moves = []
        moves = gen_moves(seqH[-1][0], seqH[-1][1], tiles, board)
        # print (moves)
        # com_move = best_move(moves,board,tiles)
        if moves:
            com_move = moves[randint(0, len(moves) - 1)]
            board[com_move[0]][com_move[1]] = 1
            draw_move(com_move[0], com_move[1], 1)
            seqC.append(com_move)
            print(com_move[0] + 1, ',', com_move[1] + 1)
        #print_board(board)
        print('Move ', len(seqC),".", "Computer move:", seqC[-1][0]+1,",", seqC[-1][1]+1, " Score: ", score_board(board,tiles))
    final_score = score_board(board, tiles)
    print("Good game! The score was: ", final_score[0], "to ", final_score[1])


def play_kulami_Vs():
    seqR = []
    seqAI = []
    [board, tiles] = init_board()
    draw_board()
    draw_tiles(tiles)
    seqR = [[randint(0, 7), randint(0, 7)]]
    #print(seqR)
    board[seqR[-1][0]][seqR[-1][1]] = 1
    draw_move(seqR[-1][0], seqR[-1][1], 1)
    #print_board(board)
    stuck = 0
    while len(seqR) <= 28:
        moves = gen_moves(seqR[-1][0], seqR[-1][1], tiles, board)
        if moves:
            com_move = best_move(moves, board, tiles, 2)
            board[com_move[0]][com_move[1]] = 2
            draw_move(com_move[0], com_move[1], 2)
            seqAI.append(com_move)
            print(com_move)

        else:
            stuck = 1
        #print(com_move)
        #print_board(board)
        #inputx = int(input('enter an x coordinate: '))-1
        #inputy = int(input('enter a y coordinate: '))-1
        moves = gen_moves(seqAI[-1][0], seqAI[-1][1], tiles, board)
        if moves:
            rand_move = moves[randint(0, len(moves) - 1)]
            seqR.append(rand_move)
            board[seqR[-1][0]][seqR[-1][1]] = 1
            draw_move(seqR[-1][0], seqR[-1][1], 1)
        else:
            stuck = stuck + 1
        print('Move ', len(seqR),".", score_board(board,tiles))
        if stuck == 2:
            break
        print (rand_move)
    final_score = score_board(board, tiles)
    print("Good game! The score was: ", final_score[0], "to ", final_score[1])
    input("Press enter to CLOSE")
    return final_score





#play_kulami_rand()
clearscreen()
setup(650,650)
#play_kulami_AI()
#all_scores=[]
#for i in range(0,10):
#    clearscreen()
#    all_scores.append(play_kulami_Vs())
#print(all_scores)


def look_ahead(last_x, last_y, tiles, board):
   next_moves = gen_moves(last_x, last_y, tiles, board)
   next2moves = []
   sd = -1000
   current_best = next_moves[0]
   for m in next_moves:
      temp_board = board
      temp_board[m[0],m[1]]=1
      best_move = best_move(m[0],m[1],tiles,temp_board,2)
      temp_board[current_best[0],current_best[1]]=2
      [s1,s2] = score_board(temp_board, tiles)
      if s1-s2 > sd:
         sd=s1-s2
         current_best = m
         


def play_kulami():
    print("This is Kulami, a game where you place")
    print("balls down on a board.")
    print("You must play in the same row or column")
    print("as the opponent's last move,")
    print("but on a different tile.")
    print("At the end each tile goes")
    print("to the player who has more balls on it.")
    print("Each tile's score is its area,")
    print("i.e.,1, 2, 3, 4,or 6.")
    print("You have 3 options:")
    print("(1) AI vs Random")
    print("(2) AI vs you")
    print("(3) Random vs you")
    type = int(input("Which option would you like? Please type 1, 2 ,or 3: "))

    if type == 1:
        play_kulami_Vs()

    elif type == 2:
        play_kulami_AI()

    elif type == 3:
        play_kulami_rand()

    else:
        print ("invalid response")
        return


play_kulami()
