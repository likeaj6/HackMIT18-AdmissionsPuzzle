{"col":1,"message":"Connection failed! Your driver had to choose a random direction.","row":3,"time":596}
{"col":0,"message":"Phew! The message made it through - your driver made the correct turn.","row":3,"time":593}
{"message":"Invalid move."}
{"message":"You are stuck, go ahead and reset!"}
import requests

URL = "https://gps.hackmirror.icu/api/"



def try_move(move):
    move_param = {'user':'likeaj6_18fb1e', move: move}
    return move_param

def make_move(data):
    r = requests.post(url = URL, data = data)
    data = r.json()
    #TODO:

def determine_move(response):
    moved = False
    invalid = False
    reset = False
    message = response['message']
    if message == "You are stuck, go ahead and reset!":
        url = "https://gps.hackmirror.icu/api/reset?user=likeaj6_18fb1e"
        reset = True
        print("RESET")
    else:
        invalid = True
        if message == "Connection failed! Your driver had to choose a random direction.":
            moved = True
            invalid = False
            row = response['row']
            col = response['col']
            print("GOT RANDOM CUCKED: ")
            print("row: ", row)
            print("col: ", col)
        if message == "Phew! The message made it through - your driver made the correct turn.":
            moved = True
            invalid = False
            row = response['row']
            col = response['col']
            print("MOVED")
            print("row: ", row)
            print("col: ", col)
    return moved, invalid, reset

def reset_directions_tried():
    #tried_right, tried_down, tried_left, tried_up
    return [False, False, False, False]

def next_direction(tried):

while True:
    currentPosition = (0, 0)
    tried = reset_directions_tried()
    direction = next_direction(tried)
    params = try_move(direction)
    response = make_move(make_move)
    moved, invalid, reset = determine_move(response)
    if moved:
        tried = reset_directions_tried()
