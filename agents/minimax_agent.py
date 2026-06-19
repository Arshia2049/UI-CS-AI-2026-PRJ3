from agents.evaluation import evaluate, order_moves

class MinimaxAgent:
    def __init__(self, depth=4):
        self.depth = depth
        self.nodes_count = 0

    def evaluate(self, game, player):
        return evaluate(game, player)

    def minimax(self, game, depth, maximizing, root_player):
        self.nodes_count += 1

        if depth == 0 or game.game_over():
            return self.evaluate(game, root_player), None

        if maximizing:
            player_color = root_player  
        else: 
            player_color = -root_player 
        moves = game.get_valid_moves(player_color)

        if not moves:
            v2, action = self.minimax(game, depth, not maximizing, root_player)
            return v2, None
        
        if maximizing:
            v = float('-inf')
            
            for move in order_moves(game, moves):

                child = game.copy()
                child.make_move(player_color, *move)

                v2, _ = self.minimax(child, depth - 1, False, root_player)

                if v2 > v:
                    v = v2
                    choice = move

            return v, choice
        else:
            v = float('inf')

            for move in order_moves(game, moves):

                child = game.copy()
                child.make_move(player_color, *move)

                v2, _ = self.minimax(child, depth - 1, True, root_player)

                if v2 < v:
                    v = v2
                    choice = move

            return v, choice

    def choose_move(self, game, player):
        self.nodes_count = 0
        moves = game.get_valid_moves(player)

        if not moves:
            return None
        
        value, move = self.minimax(game, self.depth, True, player)

        return move if move is not None else moves[0]
