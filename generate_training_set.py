import os
import chess.pgn
import numpy as np
from state import State

def get_dataset(num_samples=None):
    X, Y = [], []
    gn = 0
    values = {'1/2-1/2':0, '0-1':-1, '1-0':1}
    # png files in the data folder
    for fn in os.listdir("data"):
        pgn = open(os.path.join("data", fn))
        while True:
            try:
                game = chess.pgn.read_game(pgn)
            except:
                pass
            if game is None:
                break
            res = game.headers['Result']
            if res not in values:
                continue
            value = values[res]
            board = game.board()
            for i, move in enumerate(game.main_line()):
                board.push(move)
                ser = State(board).serialize()
                X.append(ser)
                Y.append(value)
            print("parsing game %d, got %d examples" % (gn, len(X)))
            if num_samples is not None and len(X) > num_samples:
                return X, Y
            gn += 1
    return X, Y

if __name__ == "__main__":
    for n, suf in [(1000, '1k'), (1e6, '1M'), (10e6, '10M')]:
        print('generate %s' % suf)
        X, Y = get_dataset(n)
        np.savez('processed/dataset_%s.npz' % suf, X, Y)
