Zero Knowledge Chess Engine (liar!)

* Establish the search tree
* Use a neural network to prune the search tree

Definition: Value network
V = f(state)

What is V?
V = -1 black wins board state
V = 0  draw board state
V = 1  white wins board state

Should we fix the value of the initial board state?

What's the value of "about to lose"?

Simpler:
All positions where white wins = 1
All positions where draw = 0
All positions where black wins = -1

State(Board):

Pieces(2+7*2 = 16):
* Universal
** Blank
** Blank (En passant)
* Pieces
** Pawn
** Bishop
** Knight
** Rook
** Rook (can castle)
** Queen
** King

Extra move:
* To move

8x8x4 + 1 = 257 bits (vectors of 0 or 1)




== Download training data

```bash
$ wget http://kingbase-chess.net/download/599 data/kb2018.zip
```
