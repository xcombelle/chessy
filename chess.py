import numpy as np
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
logging.info(start_position)
EMPTY = 0x0
PAWN = 0x2
KING= 0x4
QUEEN = 0x6
BISHOP = 0x8
KNIGHT = 0xA
ROOK = 0xC

WHITE = 0x1
BLACK = 0x0

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
assert diagram_bytes2text(diagram_text2bytes(start_position))==start_position


def to_2d(coordinate):
    row = 7 - (coordinate >> 3)
    column = coordinate & 0x7 
    return row,column
def pp_to_2d(coordinate):
    row,column = to_2d(coordinate)
    column =chr(ord("a")+column)
    return f"{column}{row+1}"

def p_convert():
    i=0
    d=diagram_text2bytes(start_position)
    r = []
    for raw in range(8):
        for column in range(8):            
            r.append(f"{pp_to_2d(i)} {byte2text[d[i]]} ")
            i+=1
        r.append("\n")
    logging.info("".join(r))
p_convert()          
#def legal_king(diagram, coordinate, color, direction):
#    if diagram[coordinate]!=color|KING:
#        raise Exception(f"no king in {coordinate=}")
#    row = coordinate
