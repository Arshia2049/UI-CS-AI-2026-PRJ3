# TODO: STUDENT IMPLEMENTATION

from agents.evaluation import evaluate, order_moves


class AlphaBetaAgent:

    def __init__(self, depth=4):
        self.depth = depth
        self.nodes_count = 0


    def evaluate(self, game, player):
        return evaluate(game, player)


    def alphabeta(self, game, depth, alpha, beta, maximizing, root_player):

        self.nodes_count += 1

        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None
        


        if maximizing:
            player_color = root_player  
        else: 
            player_color = -root_player 
        moves = game.get_valid_moves(player_color)

        if not moves:
            value, action = self.alphabeta(game, depth, alpha, beta, not maximizing, root_player)
            return value, None
        

        if maximizing:

            v = float('-inf')
            for move in order_moves(game, moves):

                g = game.copy()
                g.make_move(player_color, *move)

                v2, _ = self.alphabeta(g, depth-1, alpha, beta, False, root_player)

                if v2 > v:     # به عنوان نود پدر یا فرزند از این استفاده می کند
                    v = v2
                    choice = move
                    alpha = max(alpha,v)

                if v >= beta:      # به عنوان نود فرزند از این استفاده می کند تا هرس شود
                    break

            return v,choice
        

        else:
            v = float('inf')

            for move in order_moves(game, moves):

                g = game.copy()
                g.make_move(player_color, *move)

                v2, _ = self.alphabeta(g, depth-1, alpha, beta, True, root_player)

                if v2 < v:             # به عنوان نود پدر یا فرزند از این استفاده می کند
                    v = v2
                    choice = move
                    beta = min(beta,v)

                if v <= alpha:              # به عنوان نود فرزند از این استفاده می کند تا هرس شود
                    break
                
            return v,choice     


    def choose_move(self, game, player):

        self.nodes_count = 0
        moves = game.get_valid_moves(player)
        if not moves:
            return None
        
        value , move = self.alphabeta(
            game, self.depth, float('-inf'), float('inf'), True, player
        )
        return move

