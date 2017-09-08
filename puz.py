import random
from random import randint
import itertools

def print_piece(num, piece):
    """ Function to print out a piece """
    print("   {0}:{1}".format(piece["up"]["bird"], piece["up"]["side"]))
    print("{0}:{1} {2} {3}:{4}".format(piece["left"]["bird"], \
      piece["left"]["side"], num, piece["right"]["bird"],
      piece["right"]["side"]))
    print("   {0}:{1}".format(piece["down"]["bird"], piece["down"]["side"]))

def rotate_left(piece, pieces):
    """ rotate a piece to the left """
    # print "Rotating piece ", piece

    temp = {}
    temp["bird"] = pieces[piece]["up"]["bird"]
    temp["side"] = pieces[piece]["up"]["side"]

    pieces[piece]["up"]["bird"] = pieces[piece]["right"]["bird"]
    pieces[piece]["up"]["side"] = pieces[piece]["right"]["side"]

    pieces[piece]["right"]["bird"] = pieces[piece]["down"]["bird"]
    pieces[piece]["right"]["side"] = pieces[piece]["down"]["side"]

    pieces[piece]["down"]["bird"] = pieces[piece]["left"]["bird"]
    pieces[piece]["down"]["side"] = pieces[piece]["left"]["side"]

    pieces[piece]["left"]["bird"] = temp["bird"]
    pieces[piece]["left"]["side"] = temp["side"]


def print_board_row(br):
    """ Print out the given board row """
    print("+--{0}:{1}--+ +--{2}:{3}--+ +--{4}:{5}--+").format(\
      br["r"]["up"]["bird"], br["r"]["up"]["side"],\
      br["m"]["up"]["bird"], br["m"]["up"]["side"],\
      br["l"]["up"]["bird"], br["l"]["up"]["side"])

    print"|       | |       | |       |"
    print("{0}:{1}   {2}:{3} {4}:{5}   {6}:{7} {8}:{9}   {10}:{11}").format(\
      br["r"]["left"]["bird"], br["r"]["left"]["side"],\
      br["r"]["right"]["bird"], br["r"]["right"]["side"],\
      br["m"]["left"]["bird"], br["m"]["left"]["side"],\
      br["m"]["right"]["bird"], br["m"]["right"]["side"],\
      br["l"]["left"]["bird"], br["l"]["left"]["side"],\
      br["l"]["right"]["bird"], br["l"]["right"]["side"])

    print"|       | |       | |       |"
    print("+--{0}:{1}--+ +--{2}:{3}--+ +--{4}:{5}--+").format(\
      br["r"]["down"]["bird"], br["r"]["down"]["side"],\
      br["m"]["down"]["bird"], br["m"]["down"]["side"],\
      br["l"]["down"]["bird"], br["l"]["down"]["side"])


def print_board(board):
    """ Print out the board"""
    print_board_row(board["top"])
    print_board_row(board["middle"])
    print_board_row(board["bottom"])

pieces = {
    1:{"up":   {"bird":3, "side":1},
       "right":{"bird":3, "side":2},
       "down": {"bird":1, "side":2},
       "left": {"bird":2, "side":1}},
    2:{"up":   {"bird":2, "side":2},
       "right":{"bird":4, "side":2},
       "down": {"bird":1, "side":1},
       "left": {"bird":1, "side":1}},
    3:{"up":   {"bird":1, "side":1},
       "right":{"bird":2, "side":1},
       "down": {"bird":4, "side":1},
       "left": {"bird":3, "side":1}},
    4:{"up":   {"bird":4, "side":2},
       "right":{"bird":1, "side":1},
       "down": {"bird":3, "side":1},
       "left": {"bird":2, "side":1}},
    5:{"up":   {"bird":3, "side":2},
       "right":{"bird":4, "side":2},
       "down": {"bird":2, "side":2},
       "left": {"bird":1, "side":1}},
    6:{"up":   {"bird":1, "side":1},
       "right":{"bird":2, "side":1},
       "down": {"bird":4, "side":2},
       "left": {"bird":3, "side":1}},
    7:{"up":   {"bird":2, "side":2},
       "right":{"bird":3, "side":1},
       "down": {"bird":4, "side":2},
       "left": {"bird":4, "side":1}},
    8:{"up":   {"bird":4, "side":1},
       "right":{"bird":2, "side":2},
       "down": {"bird":3, "side":2},
       "left": {"bird":1, "side":2}},
    9:{"up":   {"bird":3, "side":1},
       "right":{"bird":1, "side":2},
       "down": {"bird":2, "side":1},
       "left": {"bird":4, "side":2}},
}

empty = {"up":   {"bird":0, "side":0},
         "right":{"bird":0, "side":0},
         "down": {"bird":0, "side":0},
         "left": {"bird":0, "side":0}}

board = { "top":   {"r":{}, "m":{}, "l":{}},
          "middle":{"r":{}, "m":{}, "l":{}},
          "bottom":{"r":{}, "m":{}, "l":{}}}

for piece in pieces:
    print_piece(piece, pieces[piece])

board["top"]["r"] = empty
board["top"]["m"] = empty
board["top"]["l"] = empty
board["middle"]["r"] = empty
board["middle"]["m"] = empty
board["middle"]["l"] = empty
board["bottom"]["r"] = empty
board["bottom"]["m"] = empty
board["bottom"]["l"] = empty

print ""

# With 3x3, make this row/column based
def check_board(b):
    """ See if this board order is valid """
    if b["top"]["r"]["right"]["bird"] != b["top"]["m"]["left"]["bird"]:
        return False
    if b["top"]["r"]["right"]["side"] == b["top"]["m"]["left"]["side"]:
        return False
    if b["top"]["m"]["right"]["bird"] != b["top"]["l"]["left"]["bird"]:
        return False
    if b["top"]["m"]["right"]["side"] == b["top"]["l"]["left"]["side"]:
        return False

    if b["top"]["r"]["down"]["bird"] != b["middle"]["r"]["up"]["bird"]:
	return False
    if b["top"]["r"]["down"]["side"] == b["middle"]["r"]["up"]["side"]:
        return False
    if b["top"]["m"]["down"]["bird"] != b["middle"]["m"]["up"]["bird"]:
	return False
    if b["top"]["m"]["down"]["side"] == b["middle"]["m"]["up"]["side"]:
        return False
    if b["top"]["l"]["down"]["bird"] != b["middle"]["l"]["up"]["bird"]:
	return False
    if b["top"]["l"]["down"]["side"] == b["middle"]["l"]["up"]["side"]:
        return False

    if b["middle"]["r"]["right"]["bird"] != b["middle"]["m"]["left"]["bird"]:
        return False
    if b["middle"]["r"]["right"]["side"] == b["middle"]["m"]["left"]["side"]:
        return False
    if b["middle"]["m"]["right"]["bird"] != b["middle"]["l"]["left"]["bird"]:
        return False
    if b["middle"]["m"]["right"]["side"] == b["middle"]["l"]["left"]["side"]:
        return False

    if b["middle"]["r"]["down"]["bird"] != b["bottom"]["r"]["up"]["bird"]:
	return False
    if b["middle"]["r"]["down"]["side"] == b["bottom"]["r"]["up"]["side"]:
        return False
    if b["middle"]["m"]["down"]["bird"] != b["bottom"]["m"]["up"]["bird"]:
	return False
    if b["middle"]["m"]["down"]["side"] == b["bottom"]["m"]["up"]["side"]:
        return False
    if b["middle"]["l"]["down"]["bird"] != b["bottom"]["l"]["up"]["bird"]:
	return False
    if b["middle"]["l"]["down"]["side"] == b["bottom"]["l"]["up"]["side"]:
        return False

    if b["bottom"]["r"]["right"]["bird"] != b["bottom"]["m"]["left"]["bird"]:
        return False
    if b["bottom"]["r"]["right"]["side"] == b["bottom"]["m"]["left"]["side"]:
        return False
    if b["bottom"]["m"]["right"]["bird"] != b["bottom"]["l"]["left"]["bird"]:
        return False
    if b["bottom"]["m"]["right"]["side"] == b["bottom"]["l"]["left"]["side"]:
        return False
    return True


found = False
perms = 0;
tc = 0;

for bp in itertools.permutations((x for x in range(1, 10)), 9):
    perms = perms + 1

print "We have ", perms, " permutations to explore"

count = 0
for bp in itertools.permutations((x for x in range(1, 10)), 9):
    count = count + 1

    print bp, perms - count
    board["top"]["r"] = pieces[bp[0]]
    board["top"]["m"] = pieces[bp[1]]
    board["top"]["l"] = pieces[bp[2]]
    board["middle"]["r"] = pieces[bp[3]]
    board["middle"]["m"] = pieces[bp[4]]
    board["middle"]["l"] = pieces[bp[5]]
    board["bottom"]["r"] = pieces[bp[6]]
    board["bottom"]["m"] = pieces[bp[7]]
    board["bottom"]["l"] = pieces[bp[8]]

    found = False

    for bp0_r in range(0, 4):
	for bp1_r in range(0, 4):
	    for bp2_r in range(0, 4):
		for bp3_r in range(0, 4):
		    for bp4_r in range(0, 4):
			for bp5_r in range(0, 4):
			    for bp6_r in range(0, 4):
				for bp7_r in range(0, 4):
				    for bp8_r in range(0, 4):
					# print_board(board)
					tc = tc + 1
					if check_board(board):
					    print "Yes"
					    found = True
					    break
					rotate_left(bp[8], pieces)
				    if found == True:
					break
				    rotate_left(bp[7], pieces)
				if found == True:
				    break
				rotate_left(bp[6], pieces)
			    if found == True:
				break
			    rotate_left(bp[5], pieces)
			if found == True:
			    break
			rotate_left(bp[4], pieces)
		    if found == True:
			break
		    rotate_left(bp[3], pieces)
		if found == True:
		    break
		rotate_left(bp[2], pieces)
	    if found == True:
		break
	    rotate_left(bp[1], pieces)
	if found == True:
	    break
	rotate_left(bp[0], pieces)
    if found == True:
	break

print_board(board)
print bp
print "after ", count, " permutaions and ", tc, " rotations"
