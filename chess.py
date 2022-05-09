import logging

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] \n%(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=logging.INFO)
start_position ="""r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R"""

only_king_position =""". . . . k . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . K . . ."""


logging.info(start_position)
logging.info(only_king_position)
EMPTY = 0x0
PAWN = 0x2
KING= 0x4
QUEEN = 0x6
BISHOP = 0x8
KNIGHT = 0xA
ROOK = 0xC

WHITE = 0x1
BLACK = 0x0
COLOR = 0x1
convert = [
    (EMPTY,"."),
    (PAWN|WHITE,"P"),
    (KING|WHITE,"K"),
    (QUEEN|WHITE,"Q"),
    (BISHOP|WHITE,"B"),
    (KNIGHT|WHITE,"N"),
    (ROOK|WHITE,"R"),
    (PAWN|BLACK,"p"),
    (KING|BLACK,"k"),
    (QUEEN|BLACK,"q"),
    (BISHOP|BLACK,"b"),
    (KNIGHT|BLACK,"n"),
    (ROOK|BLACK,"r"),
    ]
    
text2byte = {
    text:byte for (byte,text) in convert
    }

byte2text = {
    byte:text for (byte,text) in convert
    }



def diagram_text2bytes(text):
    result=[]
    for piece in text.split():
        piece=text2byte[piece]
        result.append(piece)
    return result
def diagram_bytes2text(bytes_):
    result=[]
    for i in range(8):
        row_input=bytes_[:8]
        bytes_[:8]=[]
        row_output=[]
        for byte in row_input:
            char = byte2text[byte]
            row_output.append(char)
        result.append(" ".join(row_output))
    return "\n".join(result)
logging.info(diagram_bytes2text(diagram_text2bytes(start_position)))
logging.info("internal representation\n"+repr(diagram_text2bytes(start_position)))
logging.info(diagram_bytes2text(diagram_text2bytes(only_king_position)))
logging.info("internal representation\n"+repr(diagram_text2bytes(only_king_position)))
assert diagram_bytes2text(diagram_text2bytes(start_position))==start_position
assert diagram_bytes2text(diagram_text2bytes(only_king_position))==only_king_position

def from_2d(row,column):
    return row<<3|column
def to_2d(coordinate):
    row = 7 - (coordinate >> 3)
    column = coordinate & 0x7 
    return row,column
def pp_to_2d(coordinate):
    row,column = to_2d(coordinate)
    column =chr(ord("a")+column)
    return f"{column}{row+1}"

def p_convert(d):
    i=0
    d=diagram_text2bytes(d)
    r = []
    for raw in range(8):
        for column in range(8):            
            r.append(f"{pp_to_2d(i)} {byte2text[d[i]]} ")
            i+=1
        r.append("\n")
    logging.info("".join(r))
p_convert(start_position)          
p_convert(only_king_position)

directions_king=direction_queen=[
    (-1,-1),(-1,0),(-1,1),
    (0,-1),(0,1),
    (1,-1),(1,0),(1,1)]


def moves_king(diagram, coordinate, color):
    if diagram[coordinate]!=color|KING:
        raise Exception(f"no king in {coordinate=}")
    row,column = to_2d(coordinate)
    for dr,dc in directions_king:
        yield row+dr,column+dc
def legal_king(diagram, coordinate, color):
    for m in moves_king(diagram, coordinate, color):
        yield m


def is_outside(row, column):
    #print(f"{row:=} {column:=}")
    return not((0<=row<=7) and (0<=column<=7))

def is_check_king(diagram,position,color):
    row,column=to_2d(position)
    for dr,dc in directions_king:
        if is_outside(row+dr, column+dc):
            continue
                
        if diagram[from_2d(row+dr,column+dc)]==KING|0x1-color:
            return true

def is_check(diagram,color):
    for from_, piece in enumerate(diagram):
        if (KING|color) == piece:
            if is_check_king(diagram,from_,color):
                return true
        elif KING|(0x1-color) == piece:
            pass
        elif piece==EMPTY:
            pass
        else:
            #print(piece,KING|color,KING|(0x1-color))
            raise Exception(f"unknown piece piece")
    return False

#TODO replace from_ by src
def play(diagram,src,dest):
    #print(src,dest)
    result=diagram[:]
    result[dest]=diagram[src]
    result[src]=EMPTY
    return result
def legals(diagram,color):
    for from_, piece in enumerate(diagram):
        if KING|color == piece:
            for dest_r, dest_c in moves_king(diagram,from_,color):
                #print("ici")
                if is_outside(dest_r, dest_c):
                    continue
                elif not (EMPTY==piece or (0x1 & piece == color)):
                    continue
                else:
                    #print(dest_r,dest_c)
                    #print(is_outside(dest_r,dest_c))
                    #print(from_,color,diagram,is_outside(dest_r, dest_c))
        
                    new_diagram = play(diagram,from_,from_2d(dest_r,dest_c))
                    if is_check(diagram,color):
                        continue
                    yield from_,from_2d(dest_r,dest_c),new_diagram
        

        elif KING|(0x1-color) == piece:
            continue
        elif piece==EMPTY:
            continue
        else:
            Exception(f"unknown piece {piece=}")
def perft(diagram,color,depth):
    s=0
    if depth==0:
        return 1
    for from_,to,diagram_result in legals(diagram,color):
        s += perft(diagram, 0x1-color, depth-1)
    return s

for depth in range(99):
    #print("ici")
    print(f"depth:{depth},perft:{perft(diagram_text2bytes(only_king_position),WHITE,depth)}")
