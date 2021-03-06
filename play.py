import base64
import chess
import chess.svg
import time
import torch
import traceback
from flask import Flask, Response, request
from state import State
from train import Net


class Valuator(object):
    def __init__(self):
        vals = torch.load("nets/value.pth", map_location=lambda storage, loc: storage)
        self.model = Net()
        self.model.load_state_dict(vals)

    def __call__(self, s):
        brd = s.serialize()[None]
        output = self.model(torch.tensor(brd).float())
        return float(output.data[0][0])


def explore_leaves(s, v):
    ret = []
    for e in s.edges():
        s.board.push(e)
        ret.append((v(s), e))
        s.board.pop()
    return ret


def to_svg(s):
    return base64.b64encode(chess.svg.board(board=s.board).encode('utf-8')).decode('utf-8')


# chess board and "engine"
v = Valuator()
s = State()

def computer_move(s, v):
    moves = sorted(explore_leaves(s, v), key=lambda x: x[0], reverse=s.board.turn)
    print('Top 3:')
    for i, m in enumerate(moves[0:3]):
        print('  ', m)
    if len(moves) > 0:
        move = moves[0]
        print(move)
        s.board.push(move[1])
    else:
        print("No move left")


app = Flask(__name__)


@app.route("/")
def hello():
    ret = '<html>'
    ret += '<head><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script></head>'
    ret += '<body>'
    ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br />' % to_svg(s)
    ret += '<form action="/move"><input id="move" name="move" type="text"></input><input type="submit" value="Move"></input></form>'
    ret += '<script>$(function() { var input = document.getElementById("move"); input.focus(); input.select(); }); </script>'
    ret += '</body>'
    ret += '</html>'
    return ret


@app.route("/selfplay")
def selfplay():
    s = State()

    ret = '<html>'
    ret += '<body>'
    while not s.board.is_game_over():
        computer_move(s, v)
        ret += '<img width=600 height=600 src="data:image/svg+xml;base64,%s"></img><br />' % to_svg(s)
    ret += '</body>'
    ret += '</html>'

    return ret


@app.route("/move")
def move():
    if not s.board.is_game_over():
        move = request.args.get('move', default='')
        if move is not None and move != '':
            print("human moves", move)
            try:
                s.board.push_san(move)
                computer_move(s, v)
            except Exception:
                traceback.print_exc()
    else:
        print("GAME IS OVER")
    return hello()


if __name__ == "__main__":
    app.run(debug=True)
