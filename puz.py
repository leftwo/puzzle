import itertools
import math
import argparse
import sys

empty = { "name": "0", "orentation":0, "card":[
       {"bird":0, "side":0},
       {"bird":0, "side":0},
       {"bird":0, "side":0},
       {"bird":0, "side":0}
    ]}

# The board is a 9X9 square.
# Each location describes a piece and it's orentation (turn)
# Turn is 0-3 with 0 being no turn, 1 is rotating the piece clockwise
# by 1/4, and so on.
board_old = { 
     "top":    {"l":{}, "c":{}, "r":{}}, \
     "middle": {"l":{}, "c":{}, "r":{}}, \
     "bottom": {"l":{}, "c":{}, "r":{}}}

board = [ {}, {}, {}, {}, {}, {}, {}, {}, {} ]

test_pieces = { \
    1:{"name": "1", "orentation":0, "card":[
       {"bird":3, "side":1}, # 0
       {"bird":3, "side":2}, # 1
       {"bird":1, "side":2}, # 2
       {"bird":2, "side":1}  # 3
    ]},
    2:{"name": "2", "orentation":0, "card":[
       {"bird":3, "side":2},
       {"bird":4, "side":2},
       {"bird":1, "side":1},
       {"bird":4, "side":1}
    ]},
    3:{"name": "3", "orentation":0, "card":[
       {"bird":1, "side":1},
       {"bird":2, "side":2},
       {"bird":4, "side":2},
       {"bird":3, "side":1}
    ]}}

# 1 3 2 3 2 0
all_pieces = { \
    1:{"name": "1", "orentation":0, "card":[
       {"bird":3, "side":1}, # 0
       {"bird":3, "side":2}, # 1
       {"bird":1, "side":2}, # 2
       {"bird":2, "side":1}  # 3
    ]},
    2:{"name": "2", "orentation":0, "card":[
       {"bird":2, "side":2},
       {"bird":4, "side":2},
       {"bird":1, "side":1},
       {"bird":1, "side":1}
    ]},
    3:{"name": "3", "orentation":0, "card":[
       {"bird":1, "side":1},
       {"bird":2, "side":1},
       {"bird":4, "side":1},
       {"bird":3, "side":2}
    ]},
    4:{"name": "4", "orentation":0, "card":[
       {"bird":4, "side":2},
       {"bird":1, "side":1},
       {"bird":3, "side":1},
       {"bird":2, "side":2}
    ]},
    5:{"name": "5", "orentation":0, "card":[
       {"bird":3, "side":2},
       {"bird":4, "side":1},
       {"bird":4, "side":1},
       {"bird":1, "side":1}
    ]},
    6:{"name": "6", "orentation":0, "card":[
       {"bird":1, "side":2},
       {"bird":2, "side":1},
       {"bird":4, "side":2},
       {"bird":3, "side":1}
    ]},
    7:{"name": "6", "orentation":0, "card":[
       {"bird":1, "side":1},
       {"bird":2, "side":1},
       {"bird":4, "side":2},
       {"bird":3, "side":1}
    ]},
    8:{"name": "6", "orentation":0, "card":[
       {"bird":1, "side":1},
       {"bird":2, "side":1},
       {"bird":4, "side":2},
       {"bird":3, "side":1}
    ]},
    9:{"name": "6", "orentation":0, "card":[
       {"bird":1, "side":1},
       {"bird":2, "side":1},
       {"bird":4, "side":2},
       {"bird":3, "side":1}
    ]}
}

old_pieces = { \
    4:{"name": "4",
       0: {"bird":4, "side":2},
       1: {"bird":1, "side":1},
       2: {"bird":3, "side":1},
       3: {"bird":2, "side":1}},
    5:{"name": "5",
       0: {"bird":3, "side":2},
       1: {"bird":4, "side":2},
       2: {"bird":2, "side":2},
       3: {"bird":1, "side":1}},
    6:{"name": "6",
       0: {"bird":1, "side":1},
       1: {"bird":2, "side":1},
       2: {"bird":4, "side":2},
       3: {"bird":3, "side":1}},
    7:{"name": "7",
       0: {"bird":2, "side":2},
       1: {"bird":3, "side":1},
       2: {"bird":4, "side":2},
       3: {"bird":4, "side":1}},
    8:{"name": "8",
       0: {"bird":4, "side":1},
       1: {"bird":2, "side":2},
       2: {"bird":3, "side":2},
       3: {"bird":1, "side":2}},
    9:{"name": "9",
       0: {"bird":3, "side":1},
       1: {"bird":1, "side":2},
       2: {"bird":2, "side":1},
       3: {"bird":4, "side":2}},
}
def print_piece(piece):
    """ Function to print out a piece """
    up = (0 + piece["orentation"]) % 4
    right = (1 + piece["orentation"]) % 4
    down = (2 + piece["orentation"]) % 4
    left = (3 + piece["orentation"]) % 4
    print("+--{0}:{1}--+".format(piece["card"][up]["bird"], piece["card"][up]["side"]))
    print("|       |")
    print("{0}:{1} {2} {3}:{4}".format(piece["card"][left]["bird"], \
      piece["card"][left]["side"], piece["name"], piece["card"][right]["bird"],
      piece["card"][right]["side"]))
    print("|       |")
    print("+--{0}:{1}--+".format(piece["card"][down]["bird"], \
      piece["card"][down]["side"]))

def print_board_summary(board):
    for bn in range(0, 6):
        print("{}({}) ".format(board[bn]["name"], board[bn]["orentation"]),
                end="")

    print("")

def print_board_row(board, row = 0):
    """ Print out the given board row """
    up = 0
    right = 1
    down = 2
    left = 3

    row_base = row
    # These are some shortcuts to specific cards rotated to their
    # respective orentations.
    #    First character
    # o for orentation,  c for card
    #    Second character
    # # Board slot number
    #    Third character (only for "c" card shortcuts)
    # u for up, r for right, d for down, l for left,
    # Third character is adjusted based on offset value.
    #
    o0 = board[row_base]['orentation']
    o1 = board[row_base + 1]['orentation']
    o2 = board[row_base + 2]['orentation']

    c0u = board[row_base]['card'][(up + o0) % 4]
    c1u = board[row_base + 1]['card'][(up + o1) % 4]
    c2u = board[row_base + 2]['card'][(up + o2) % 4]
    print("+--{0}:{1}--+ +--{2}:{3}--+ +--{4}:{5}--+".format(\
      c0u['bird'], c0u['side'], c1u['bird'], c1u['side'], \
      c2u['bird'], c2u['side']))

    print("|    {0}  | |    {1}  | |    {2}  |".format(\
      board[row_base]['orentation'], board[row_base + 1]['orentation'],
      board[row_base + 2]['orentation']))

    c0l = board[row_base]['card'][(left + o0) % 4]
    c0r = board[row_base]['card'][(right + o0) % 4]
    c1l = board[row_base + 1]['card'][(left + o1) % 4]
    c1r = board[row_base + 1]['card'][(right + o1) % 4]
    c2l = board[row_base + 2]['card'][(left + o2) % 4]
    c2r = board[row_base + 2]['card'][(right + o2) % 4]
    print("{0}:{1} {2} {3}:{4} {5}:{6} {7} {8}:{9} {10}:{11} {12} {13}:{14}".\
      format(\
      c0l['bird'], c0l["side"], board[row_base]["name"],
      c0r['bird'], c0r["side"], 
      c1l['bird'], c1l["side"], board[row_base + 1]["name"],
      c1r['bird'], c1r["side"], 
      c2l['bird'], c2l["side"], board[row_base + 2]["name"],
      c2r['bird'], c2r["side"]))

    print("|       | |       | |       |")

    c0d = board[row_base]['card'][(down + o0) % 4]
    c1d = board[row_base + 1]['card'][(down + o1) % 4]
    c2d = board[row_base + 2]['card'][(down + o2) % 4]
    print("+--{0}:{1}--+ +--{2}:{3}--+ +--{4}:{5}--+".format(\
      c0d['bird'], c0d['side'], c1d['bird'], c1d['side'], \
      c2d['bird'], c2d['side']))


def print_board(board):
    """ Print out the board"""
    print_board_row(board)
    print_board_row(board, 3)
    # print_board_row(board["bottom"])


def check_board(b):
    """ Walk the board from top left (0) to bottom right (9).
        If we find a mis-match, return the board slot number.
        If it's all good, return 10
    """
    up = 0
    right = 1
    down = 2
    left = 3

    # Shortcut names
    # o for orentation, then the index of the board slot 
    o0 = b[0]['orentation']
    o1 = b[1]['orentation']
    o2 = b[2]['orentation']
    # c for card, then the index of the board slot
    c0 = b[0]['card']
    c1 = b[1]['card']
    c2 = b[2]['card']

    """ See if this board order is a solved puzzle """
    # 0 with 1
    if c0[(right + o0) % 4]["bird"] != c1[(left + o1) % 4]["bird"]:
        return 0
    if c0[(right + o0) % 4]["side"] == c1[(left + o1) % 4]["side"]:
        return 0

    # 1 with 2
    if c1[(right + o1) % 4]["bird"] != c2[(left + o2) % 4]["bird"]:
        return 1
    if c1[(right + o1) % 4]["side"] == c2[(left + o2) % 4]["side"]:
        return 1

    # End of top row
    # o for orentation, then the index of the board slot 
    o3 = b[3]['orentation']
    o4 = b[4]['orentation']
    o5 = b[5]['orentation']
    # c for card, then the index of the board slot
    c3 = b[3]['card']
    c4 = b[4]['card']
    c5 = b[5]['card']

    # This is for comparing card 3, if UP fails, we consider 2
    # the last succes, but if to the right fails (after up works)
    # we return 3 and let slot 4 rotate first.
    if c0[(down + o0) % 4]["bird"] != c3[(up + o3) % 4]["bird"]:
        return 2
    if c0[(down + o0) % 4]["side"] == c3[(up + o3) % 4]["side"]:
        return 2
    if c3[(right + o3) % 4]["bird"] != c4[(left + o4) % 4]["bird"]:
        return 3
    if c3[(right + o3) % 4]["side"] == c4[(left + o4) % 4]["side"]:
        return 3

    # Now on to board slot 4
    if c1[(down + o1) % 4]["bird"] != c4[(up + o4) % 4]["bird"]:
        print("3.1")
        return 3
    if c1[(down + o1) % 4]["side"] == c4[(up + o4) % 4]["side"]:
        print("3.1")
        return 3
    if c4[(right + o4) % 4]["bird"] != c5[(left + o5) % 4]["bird"]:
        return 4
    if c4[(right + o4) % 4]["side"] == c5[(left + o5) % 4]["side"]:
        return 4

    # Final test for first 2 rows, board slot 2 & 5 up & down
    if c1[(down + o1) % 4]["bird"] != c4[(up + o3) % 4]["bird"]:
        return 4
    if c1[(down + o1) % 4]["side"] == c4[(up + o3) % 4]["side"]:
        return 4

    return 10
    #
    return 10


def smart_solve(board): 
    found = 0
    perms = 0
    tc = 0
    possible = 0
    skip = 0

    # The possible orderings of a set of unique items is the factorial of
    # that set size.
    perms = math.factorial(9) 

    # Total rotations possible per iteration is:
    # Sides of each piece to the power of number of pieces.
    rotations = int(math.pow(4, 9))
    total = rotations * perms
    print("We have {0} permutations with {1} rotations".format(perms, rotations))
    print("Total:{0:,}".format(total))
    print("")

    bn = 0
    done = False
    found = 0
    max_failed = 0
    checked = 0
    while not done:
        checked += 1
        print_board(board)
        failed_at = check_board(board)
        print("Failed at {}".format(failed_at))
        # We keep track of the furthest we got while
        # looking for a match so we can skip any iterations that happen below
        # that point as we already know we can't make a match that deep.
        max_failed = max(max_failed, failed_at)
        if failed_at == 10:
            print("We found one here")
            print_board_summary(board)
            found += 1
            failed_at = 1

        bn = failed_at + 1
        # Rotate next, if we are giving up on a subset (i.e. moving up
        # one in the rotation list, then we can also throw out all iterations
        # that exist for that subset.  No point in trying 1234 1243 if 12 can't
        # match.
        if rotate_next(board, bn) == True:
            print("Continue testing")
        else:
            print("Nothing left in this instance to rotate")
            done = True

    print("Found:{} checked:{}  deepest:{}".format(found, checked, max_failed))

def rotate_next(board, bn):
    """ Move the rotation to the next possible spot from the given stop """
    done = False
    while bn >= 0:
        print("bn:{} board:{}".format(bn, board[bn]))
        if board[bn]["orentation"] < 3:
            board[bn]["orentation"] += 1
            # print("Rotate {} to {}".format(bn, board[bn]['orentation']))
            return True

        board[bn]["orentation"] = 0
        # print("Reset {} to {}".format(bn, board[bn]['orentation']))
        bn = bn - 1

    return False


def brute_force(board):
    """ Try every possible combination of the current iteration """
    found = 0
    checked = 0
    for b0_rotation in range(0, 4):
        board[0]['orentation'] = b0_rotation
        for b1_rotation in range(0, 4):
            board[1]['orentation'] = b1_rotation
            for b2_rotation in range(0, 4):
                board[2]['orentation'] = b2_rotation
                for b3_rotation in range(0, 4):
                    board[3]['orentation'] = b3_rotation
                    for b4_rotation in range(0, 4):
                        board[4]['orentation'] = b4_rotation

                        # print_board(board)
                        if check_board(board) == 10:
                            found += 1
                            print_board_summary(board)
                        checked += 1


    print("Brute force Found:{} checked:{}".format(found, checked))

if __name__ == "__main__":
    """ Take our puzzle, compute permutations and start rotating """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--start", \
                        help="Starting permutation count", type=int)
    parser.add_argument("-q", "--quit", \
                        help="quitting permutation count", type=int)
    args = parser.parse_args()

    print_piece(all_pieces[1])

    board[0] = all_pieces[1]
    board[1] = all_pieces[2]
    board[2] = all_pieces[3]
    board[3] = all_pieces[4]
    board[4] = all_pieces[5]
    board[5] = all_pieces[6]
    board[6] = all_pieces[7]
    board[7] = all_pieces[8]
    board[8] = all_pieces[9]

    # print(board)
    smart_solve(board)

    brute_force(board)
