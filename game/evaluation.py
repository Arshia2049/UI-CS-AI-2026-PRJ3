from game.othello import BLACK, WHITE, EMPTY

WIN_SCORE = 100000.0

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

def ratio(mine, theirs):
    total = mine + theirs
    if total == 0:
        return 0.0
    else:
        return (mine - theirs) / total


def is_frontier(board, r, c, n):
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            rr = r + dr
            cc = c + dc
            if rr >= 0 and rr < n and cc >= 0 and cc < n:
                if board[rr][cc] == EMPTY:
                    return True
    return False


def evaluate(game, player):
    board = game.board
    n = game.size
    opp = -player

    if game.game_over() == True:
        b, w = game.score()
        if player == BLACK:
            my = b
            th = w
        else:
            my = w
            th = b

        if my > th:
            return WIN_SCORE + (my - th)
        elif my < th:
            return -WIN_SCORE + (my - th)
        else:
            return 0.0

    weights = square_weights(n)
    last = n - 1
    corners = [(0, 0), (0, last), (last, 0), (last, last)]

    my_disc = 0
    opp_disc = 0
    my_front = 0
    opp_front = 0
    my_corner = 0
    opp_corner = 0
    pos = 0.0

    for r in range(n):
        for c in range(n):
            cell = board[r][c]
            if cell == EMPTY:
                continue

            if cell == player:
                my_disc = my_disc + 1
                pos = pos + weights[r][c]
            else:
                opp_disc = opp_disc + 1
                pos = pos - weights[r][c]

            is_corner = False
            for corner in corners:
                if corner[0] == r and corner[1] == c:
                    is_corner = True
            if is_corner == True:
                if cell == player:
                    my_corner = my_corner + 1
                else:
                    opp_corner = opp_corner + 1

            if is_frontier(board, r, c, n) == True:
                if cell == player:
                    my_front = my_front + 1
                else:
                    opp_front = opp_front + 1

    parity = ratio(my_disc, opp_disc)
    corner = (my_corner - opp_corner) / 4.0
    frontier = ratio(opp_front, my_front)

    my_mob = len(game.get_valid_moves(player))
    opp_mob = len(game.get_valid_moves(opp))
    mobility = ratio(my_mob, opp_mob)

    my_close = 0
    opp_close = 0
    for corner in corners:
        cr = corner[0]
        cc = corner[1]
        if board[cr][cc] != EMPTY:
            continue
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                rr = cr + dr
                cc2 = cc + dc
                if rr >= 0 and rr < n and cc2 >= 0 and cc2 < n:
                    v = board[rr][cc2]
                    if v == player:
                        my_close = my_close + 1
                    elif v == opp:
                        opp_close = opp_close + 1
    closeness = (opp_close - my_close) / 12.0

    total_discs = my_disc + opp_disc
    if total_discs == 0:
        total_discs = 1
    pos_norm = pos / (4.0 * total_discs)

    filled = my_disc + opp_disc
    progress = filled / (n * n)

    w_parity = 0.05 + 0.45 * progress
    w_mobility = 0.30 * (1.0 - progress)
    w_frontier = 0.15 * (1.0 - progress)
    w_corner = 0.35
    w_close = 0.15
    w_pos = 0.10

    score = w_corner * corner + w_close * closeness + w_mobility * mobility + w_frontier * frontier + w_parity * parity + w_pos * pos_norm

    return 100.0 * score
