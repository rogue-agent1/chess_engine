#!/usr/bin/env python3
"""Minimal chess engine — board representation + minimax evaluation."""
import sys

PIECES = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000,
          'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000}

INIT_BOARD = [
    list("rnbqkbnr"), list("pppppppp"),
    list("........"), list("........"),
    list("........"), list("........"),
    list("PPPPPPPP"), list("RNBQKBNR"),
]

class Chess:
    def __init__(self):
        self.board = [row[:] for row in INIT_BOARD]
    def at(self, r, c):
        if 0 <= r < 8 and 0 <= c < 8: return self.board[r][c]
        return None
    def is_white(self, p): return p.isupper()
    def evaluate(self):
        score = 0
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != '.': score += PIECES.get(p, 0)
        return score
    def moves(self, white=True):
        result = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == '.' or self.is_white(p) != white: continue
                pt = p.upper()
                if pt == 'P':
                    d = -1 if white else 1
                    if self.at(r+d, c) == '.':
                        result.append((r, c, r+d, c))
                    for dc in [-1, 1]:
                        t = self.at(r+d, c+dc)
                        if t and t != '.' and self.is_white(t) != white:
                            result.append((r, c, r+d, c+dc))
                elif pt in ('N',):
                    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
                        t = self.at(r+dr, c+dc)
                        if t is not None and (t == '.' or self.is_white(t) != white):
                            result.append((r, c, r+dr, c+dc))
                elif pt in ('B', 'R', 'Q', 'K'):
                    dirs = []
                    if pt in ('B', 'Q'): dirs += [(-1,-1),(-1,1),(1,-1),(1,1)]
                    if pt in ('R', 'Q'): dirs += [(-1,0),(1,0),(0,-1),(0,1)]
                    if pt == 'K': dirs = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
                    for dr, dc in dirs:
                        nr, nc = r+dr, c+dc
                        while True:
                            t = self.at(nr, nc)
                            if t is None: break
                            if t == '.': result.append((r, c, nr, nc))
                            elif self.is_white(t) != white:
                                result.append((r, c, nr, nc)); break
                            else: break
                            if pt == 'K': break
                            nr += dr; nc += dc
        return result
    def make_move(self, r1, c1, r2, c2):
        b = Chess(); b.board = [row[:] for row in self.board]
        b.board[r2][c2] = b.board[r1][c1]; b.board[r1][c1] = '.'
        return b
    def minimax(self, depth, white, alpha=-99999, beta=99999):
        if depth == 0: return self.evaluate(), None
        moves = self.moves(white)
        if not moves: return self.evaluate(), None
        best_move = None
        if white:
            best = -99999
            for m in moves:
                b = self.make_move(*m)
                score, _ = b.minimax(depth-1, False, alpha, beta)
                if score > best: best = score; best_move = m
                alpha = max(alpha, best)
                if beta <= alpha: break
        else:
            best = 99999
            for m in moves:
                b = self.make_move(*m)
                score, _ = b.minimax(depth-1, True, alpha, beta)
                if score < best: best = score; best_move = m
                beta = min(beta, best)
                if beta <= alpha: break
        return best, best_move
    def render(self):
        lines = ["  a b c d e f g h"]
        for r in range(8):
            row = f"{8-r} " + " ".join(self.board[r]) + f" {8-r}"
            lines.append(row)
        lines.append("  a b c d e f g h")
        return "\n".join(lines)

if __name__ == "__main__":
    depth = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    game = Chess()
    print(game.render())
    score, move = game.minimax(depth, True)
    if move:
        r1, c1, r2, c2 = move
        print(f"\nBest white move (depth {depth}): {chr(c1+97)}{8-r1} -> {chr(c2+97)}{8-r2} (eval: {score})")
        game = game.make_move(*move)
        print(game.render())
