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
def print_piece(piece):
    """ Function to print out a piece """

    print("+--{0}:{1}--+".format(piece["up"]["bird"], piece["up"]["side"]))
    print("|       |")
    print("{0}:{1} {2} {3}:{4}".format(piece["left"]["bird"], \
      piece["left"]["side"], piece["name"], piece["right"]["bird"],
      piece["right"]["side"]))
    print("|       |")
    print("+--{0}:{1}--+".format(piece["down"]["bird"], \
      piece["down"]["side"]))


def rotate_left(piece, pieces):
    """ rotate a piece to the left """
    # print("Rotating piece ", piece)

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

    print("|       | |       | |       |")
    print("{0}:{1} {2} {3}:{4} {5}:{6} {7} {8}:{9} {10}:{11} {12} {13}:{14}").\
      format(\
      br["r"]["left"]["bird"], br["r"]["left"]["side"], br["r"]["name"],
      br["r"]["right"]["bird"], br["r"]["right"]["side"],\
      br["m"]["left"]["bird"], br["m"]["left"]["side"], br["m"]["name"],
      br["m"]["right"]["bird"], br["m"]["right"]["side"],\
      br["l"]["left"]["bird"], br["l"]["left"]["side"], br["l"]["name"],
      br["l"]["right"]["bird"], br["l"]["right"]["side"])

    print("|       | |       | |       |")
    print("+--{0}:{1}--+ +--{2}:{3}--+ +--{4}:{5}--+").format(\
      br["r"]["down"]["bird"], br["r"]["down"]["side"],\
      br["m"]["down"]["bird"], br["m"]["down"]["side"],\
      br["l"]["down"]["bird"], br["l"]["down"]["side"])


def print_board(board):
    """ Print out the board"""
    print_board_row(board["top"])
    print_board_row(board["middle"])
    print_board_row(board["bottom"])
    print("\n")


def piece_has(cp, bs):
    """ Walk the four sides of the "compare piece" cp, and see if any of
        the sides match our "board side" bs.  """
    if cp["up"]["bird"] == bs["bird"] and cp["up"]["side"] != bs["side"]:
        return True

    if cp["right"]["bird"] == bs["bird"] and cp["right"]["side"] != bs["side"]:
        return True

    if cp["left"]["bird"] == bs["bird"] and cp["left"]["side"] != bs["side"]:
        return True

    if cp["down"]["bird"] == bs["bird"] and cp["down"]["side"] != bs["side"]:
        return True

    return False


def piece_match_piece(cp, mp):
    """ Take mp and walk all four sides of it, looking to see if any of them
        have a match in cp.  One match is all we need, so return True as soon
        as we find it. """

    if piece_has(cp, mp["left"]):
        return True

    if piece_has(cp, mp["up"]):
        return True

    if piece_has(cp, mp["right"]):
        return True

    if piece_has(cp, mp["down"]):
        return True

    return False

def check_permutation(b):
    """ Make a first pass at a specific permutation, without verifying
        every single connection.
        For corner spots, make sure they have at least two matches, one
        for each ajoining piece
        For side center pieces, make sure their are three matches, one
        for each ajoining piece.
        For the center, each side needs one match per side.

        We can do even better, but this is a start."""

    # For the middle, we need 4 matches
    found = 0
    cp = b["top"]["m"]
    mp = b["middle"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["r"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["l"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["bottom"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    if found != 4:
        return False

    if found > 4:
        print("What, more than 4????")
        print(mp)
        print(cp)
        print(b)
        sys.exit(1)

    # Top left compare
    found = 0
    mp = b["top"]["l"]
    cp = b["top"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["l"]
    if piece_match_piece(cp, mp):
        found = found + 1

    if found == 2:
        return True

    # top right compare
    found = 0
    mp = b["top"]["r"]
    p = b["top"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["r"]
    if piece_match_piece(cp, mp):
        found = found + 1

    if found == 2:
        return True

    # bottom left compare
    found = 0
    mp = b["bottom"]["l"]
    cp = b["bottom"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["l"]
    if piece_match_piece(cp, mp):
        found = found + 1

    if found == 2:
        return True

    # bottom right compare
    found = 0
    mp = b["bottom"]["r"]
    cp = b["bottom"]["m"]
    if piece_match_piece(cp, mp):
        found = found + 1

    cp = b["middle"]["r"]
    if piece_match_piece(cp, mp):
        found = found + 1

    if found == 2:
        return True

    return False

# With 3x3, make this row/column based
def check_board(b):
    """ See if this board order is a solved puzzle """
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


def brute_force(args, board): 
    found = 0
    perms = 0;
    tc = 0;
    possible = 0;
    skip = 0;

    for bp in itertools.permutations((x for x in range(1, 10)), 9):
        perms = perms + 1

    print("We have %d permutations to explore" % perms)

    # Total rotations possible per iteration is:
    # Sides of each piece to the power of number of pieces.
    rotations = int(math.pow(4, 9))

    count = 0
    for bp in itertools.permutations((x for x in range(1, 10)), 9):
        count = count + 1
        if (args.start and count < args.start):
            tc = tc + rotations
            continue

        if (args.quit and count > args.quit):
            break

        # print bp, " count:", count, " remaining:", perms - count
        info_str = "\r" + str(bp) + " count:" + str(count) + " remaining:" + \
            str(perms - count) + " skip:" + str(skip) + " possible:" + \
            str(possible) + "    "
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

        # This is not really saving us much, as the check test is not
        # very good.
        if not check_permutation(board):
            tc = tc + rotations
            skip = skip + 1
            continue

        possible = possible + 1
        #
        # Another idea is to test rotated item right away for its edges
        # and see if it passes.  Will this help us with speeding up the
        # check board function?
        for x in range(0, rotations):
            if check_board(board):
                found = found + 1
                print("\n")
                print("found match", found, "at ", bp)
                print("after %d permutaions and %d rotations" % (count, tc))
                print_board(board)

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

    print("found %d matches after %d permutaions and %d rotations"
            % (found, count, tc))


if __name__ == "__main__":
    """ Take our puzzle, compute permutations and start rotating """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", \
                        help="Starting permutation count", type=int)
    parser.add_argument("-q", "--quit", \
                        help="quitting permutation count", type=int)
    args = parser.parse_args()

    for piece in pieces:
        print_piece(pieces[piece])

    board["top"]["r"] = empty
    board["top"]["m"] = empty
    board["top"]["l"] = empty
    board["middle"]["r"] = empty
    board["middle"]["m"] = empty
    board["middle"]["l"] = empty
    board["bottom"]["r"] = empty
    board["bottom"]["m"] = empty
    board["bottom"]["l"] = empty

    brute_force(args, board)
