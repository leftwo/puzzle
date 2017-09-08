import random
from random import randint
import itertools
import math
import argparse
import sys

empty = {"up":   {"bird":0, "side":0},
         "right":{"bird":0, "side":0},
         "down": {"bird":0, "side":0},
         "left": {"bird":0, "side":0}}

board = { "top":   {"r":{}, "m":{}, "l":{}},
          "middle":{"r":{}, "m":{}, "l":{}},
          "bottom":{"r":{}, "m":{}, "l":{}}}

pieces = {
    1:{"name": "1",
       "up":   {"bird":3, "side":1},
       "right":{"bird":3, "side":2},
       "down": {"bird":1, "side":2},
       "left": {"bird":2, "side":1}},
    2:{"name": "2",
       "up":   {"bird":2, "side":2},
       "right":{"bird":4, "side":2},
       "down": {"bird":1, "side":1},
       "left": {"bird":1, "side":1}},
    3:{"name": "3",
       "up":   {"bird":1, "side":1},
       "right":{"bird":2, "side":1},
       "down": {"bird":4, "side":1},
       "left": {"bird":3, "side":1}},
    4:{"name": "4",
       "up":   {"bird":4, "side":2},
       "right":{"bird":1, "side":1},
       "down": {"bird":3, "side":1},
       "left": {"bird":2, "side":1}},
    5:{"name": "5",
       "up":   {"bird":3, "side":2},
       "right":{"bird":4, "side":2},
       "down": {"bird":2, "side":2},
       "left": {"bird":1, "side":1}},
    6:{"name": "6",
       "up":   {"bird":1, "side":1},
       "right":{"bird":2, "side":1},
       "down": {"bird":4, "side":2},
       "left": {"bird":3, "side":1}},
    7:{"name": "7",
       "up":   {"bird":2, "side":2},
       "right":{"bird":3, "side":1},
       "down": {"bird":4, "side":2},
       "left": {"bird":4, "side":1}},
    8:{"name": "8",
       "up":   {"bird":4, "side":1},
       "right":{"bird":2, "side":2},
       "down": {"bird":3, "side":2},
       "left": {"bird":1, "side":2}},
    9:{"name": "9",
       "up":   {"bird":3, "side":1},
       "right":{"bird":1, "side":2},
       "down": {"bird":2, "side":1},
       "left": {"bird":4, "side":2}},
}
def print_piece(num, piece):
    """ Function to print out a piece """
    print("   {0}:{1}".format(piece["up"]["bird"], piece["up"]["side"]))
    print("{0}:{1} {2} {3}:{4}".format(piece["left"]["bird"], \
      piece["left"]["side"], piece["name"], piece["right"]["bird"],
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
    print("{0}:{1} {2} {3}:{4} {5}:{6} {7} {8}:{9} {10}:{11} {12} {13}:{14}").\
      format(\
      br["r"]["left"]["bird"], br["r"]["left"]["side"], br["r"]["name"],
      br["r"]["right"]["bird"], br["r"]["right"]["side"],\
      br["m"]["left"]["bird"], br["m"]["left"]["side"], br["m"]["name"],
      br["m"]["right"]["bird"], br["m"]["right"]["side"],\
      br["l"]["left"]["bird"], br["l"]["left"]["side"], br["l"]["name"],
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


if __name__ == "__main__":
    """ Take our puzzle, compute permutations and start rotating """
    found = 0
    perms = 0;
    tc = 0;

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", \
                        help="Starting permutation count", type=int)
    parser.add_argument("-q", "--quit", \
                        help="quitting permutation count", type=int)
    args = parser.parse_args()

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

    for bp in itertools.permutations((x for x in range(1, 10)), 9):
        perms = perms + 1

    print "We have ", perms, " permutations to explore"

    # Total rotations possible per iteration is:
    # Sides of each piece to the power of number of pieces.
    rotations = int(math.pow(4, 9))

    count = 0
    for bp in itertools.permutations((x for x in range(1, 10)), 9):
        count = count + 1
        # Make command line option to start from a specific spot
        if (args.start and count < args.start):
            tc = tc + rotations
            continue

        if (args.quit and count > args.quit):
	    break

        # print bp, " count:", count, " remaining:", perms - count
	info_str = "\r" + str(bp) + " count:" + str(count) + " remaining:" + \
	    str(perms - count) + "   "
	sys.stdout.write(info_str)
	sys.stdout.flush()
        board["top"]["r"] = pieces[bp[0]]
        board["top"]["m"] = pieces[bp[1]]
        board["top"]["l"] = pieces[bp[2]]
        board["middle"]["r"] = pieces[bp[3]]
        board["middle"]["m"] = pieces[bp[4]]
        board["middle"]["l"] = pieces[bp[5]]
        board["bottom"]["r"] = pieces[bp[6]]
        board["bottom"]["m"] = pieces[bp[7]]
        board["bottom"]["l"] = pieces[bp[8]]

        for x in range(0, rotations):
            if check_board(board):
		found = found + 1
                print ""
                print "found match", found, "at ", bp
		print "after ", count, " permutaions and ", tc, " rotations"
		print_board(board)
		print ""

            rotate_left(bp[8], pieces)
            tc = tc + 1
            if (tc % 4 == 0):
                rotate_left(bp[7], pieces)
            if (tc % 16 == 0):
                rotate_left(bp[6], pieces)
            if (tc % 64 == 0):
                rotate_left(bp[5], pieces)
            if (tc % 256 == 0):
                rotate_left(bp[4], pieces)
            if (tc % 1024 == 0):
                rotate_left(bp[3], pieces)
            if (tc % 4096 == 0):
                rotate_left(bp[2], pieces)
            if (tc % 16384 == 0):
                rotate_left(bp[1], pieces)
            if (tc % 65536 == 0):
                rotate_left(bp[0], pieces)

    print "\n", found, "matches after ", count, " permutaions and ", tc,\
      " rotations"
