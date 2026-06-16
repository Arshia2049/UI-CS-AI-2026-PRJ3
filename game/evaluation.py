from game.othello import BLACK, WHITE, EMPTY

def square_weights(n):
    last = n - 1
    corners = [(0, 0), (0, last), (last, 0), (last, last)]
    w = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(0.0)
        w.append(row)

    for r in range(n):
        for c in range(n):
            is_corner = False
            for corner in corners:
                if corner[0] == r and corner[1] == c:
                    is_corner = True
            if is_corner == True:
                w[r][c] = 4.0
            else:
                near_corner = None
                for corner in corners:
                    cr = corner[0]
                    cc = corner[1]
                    if abs(r - cr) <= 1 and abs(c - cc) <= 1:
                        near_corner = corner
                if near_corner != None:
                    cr = near_corner[0]
                    cc = near_corner[1]
                    if r == cr or c == cc:
                        w[r][c] = -3.0
                    else:
                        w[r][c] = -4.0
                elif r == 0 or c == 0 or r == last or c == last:
                    w[r][c] = 2.0
                elif r == 1 or c == 1 or r == last - 1 or c == last - 1:
                    w[r][c] = -1.0
                else:
                    w[r][c] = 1.0
    return w

def order_moves(game, moves):
    weights = square_weights(game.size)
    def get_weight(m):
        return weights[m[0]][m[1]]
    sorted_moves = sorted(moves, key=get_weight, reverse=True)
    return sorted_moves