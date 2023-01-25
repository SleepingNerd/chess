import pygame
import engine
import math
import piece
from random import choice
from typing import Optional
from random import shuffle



class Player():
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False):
        self.name = name
        self.name_surf = font.render(name, antialiasing,font_color )
        self.image = pygame.transform.scale(pygame.image.load(avatar_img).convert_alpha(), avatar_img_size)


class Human(Player):
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False):
        super().__init__(avatar_img, avatar_img_size,name, font, font_color, antialiasing)
        self.reset()
    def reset(self):
        self.selected = None
        self.legal_moves = []
        self.promotion = None

    def touch(self, board_data: engine.BoardData, pos: engine.Coordinate):
        
        if pos.x < 0 or  pos.x > 7 or pos.y < 0 or pos.x > 7:
            return
        
        
        # If it's not empty
        if  board_data.board[pos.y][pos.x] != piece.EMPTY:
            # If of his color
            if board_data.board[pos.y][pos.x].color == board_data.active:

                self.selected = pos
                self.legal_moves = engine.get_piece_moves(board_data, self.selected)

            # If piece of other color
            else:
                self.apply(board_data, pos)
        # If it's empty
        else:
            self.apply(board_data, pos)
    # NOTE: In only checks for identity
    def apply(self, board_data: engine.BoardData, pos: engine.Coordinate, p_type = None):
        for move in self.legal_moves:
            if move.dest.y == pos.y and move.dest.x == pos.x:
                # If it's a promotion move
                if isinstance(move, engine.Promotion):
                    if p_type == None:
                        self.promotion = move.dest
                        return False
                    elif move.type.type == p_type:
                        board_data.apply_move(move)
                else:
                    board_data.apply_move(move)
                    self.reset()
                    return True
        self.reset()
        return False
        
    def tell_type(self, board_data: engine.BoardData, p_type):
        self.apply(board_data, self.promotion, p_type)
    
    
    
class Bot(Player):
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False, depth=0):
        super().__init__(avatar_img, avatar_img_size,name, font, font_color, antialiasing)
        self.depth = depth
    def move(self, board_data: engine.BoardData) -> Optional[engine.Move]:
        pass
    
class RandomBot(Bot):        
    def move(self, board_data: engine.BoardData) -> Optional[engine.Move]:
        moves = engine.get_moves(board_data, board_data.active)
        if moves == []:
            return None
        return choice(moves)
    
"""
DEPTH 2 2 MOVES BOTS -> 
-61.115899324417114
-2.994014024734497
-7.587989330291748
-4.615025520324707
____________________________________________________
-4.371410369873047
-35.51592993736267
-22.456780433654785
__________________________________________________________
-4.3600013256073
-34.29758954048157
-22.33568811416626
_____________________________________________________________
-4.373029708862305
-29.864010334014893
-21.820008993148804
______________________________________________________________

-4.847798109054565
-13.156013011932373
-19.75897741317749
Killer move heuristics lets goo
___________________________________________________________________



"""
    
class BasicBot(Bot):
    def __init__(self,avatar_img, avatar_img_size,name, font, font_color, antialiasing = False, depth=0):
        super().__init__(avatar_img, avatar_img_size,name, font, font_color, antialiasing, depth)
        self.killer_moves = [[], []]

    def move(self, board_data: engine.BoardData, depth = None) -> Optional[engine.Move]:
        self.killer_moves =  [[], []]
        if depth == None:
            depth = self.depth
        moves = engine.get_moves(board_data, board_data.active)
        moves = self.first_order(board_data, moves)
        current_choice = None
        alpha = -math.inf
        beta =  math.inf
        
        if depth > 0:
            if board_data.active == piece.WHITE:
                max_value = -math.inf
                for move in moves:
                    
                    evaluation = self.minimax(engine.apply_move(board_data,move), depth-1, alpha, beta)  
                    if max_value < evaluation:
                        max_value = evaluation  
                        current_choice = move      
                                    
                    alpha = max(alpha, evaluation)
                    if beta <= alpha:
                        self.killer_moves[board_data.active].append(move)
                        break  
                    
                return current_choice       
            
            else:
                min_value = math.inf
                for move in moves:
                    evaluation = self.minimax(engine.apply_move(board_data, move), depth -1, alpha, beta)
                    if min_value > evaluation:
                        min_value = evaluation
                        current_choice = move

                    beta = min(beta, evaluation)
                    if beta <= alpha:
                        self.killer_moves[board_data.active].append(move)
                        break   
                return current_choice   
                    
    ""
    def minimax(self, board_data: engine.BoardData, depth, alpha, beta) -> int:
        #
        if depth == 0:
            return self.evaluate(board_data)
        # White should try to get the HIGHEST value 
        elif board_data.active == piece.WHITE:
            # Get moves and order them
            moves = engine.get_moves(board_data, piece.WHITE)
            moves = self.order(board_data, moves)
            
            # Set a maximum
            max_value = -math.inf
            
            # For every move
            for move in moves:
                # Evaluate
                evaluation = self.minimax(engine.apply_move(board_data, move), depth -1, alpha, beta)
                
                 # Overwrite node value
                max_value = max(max_value, evaluation)
                
                # Overwrite alpha (best position for white)
                alpha = max(alpha, evaluation)
            
                # If beta is less than alpha (can only happen if beta)
                if beta <= alpha:
                    self.killer_moves[board_data.active].append(move)
                    break
                
            return max_value   
        
        # Black should try to get the LOWEST value
        else:    
            # Get moves and order them
            moves = engine.get_moves(board_data, piece.BLACK)
            moves = self.order(board_data, moves)

            # Set a minimum
            min_value = math.inf
            
            # For every move
            for move in moves:
                # Evaluate
                evaluation = self.minimax(engine.apply_move(board_data, move), depth -1, alpha, beta)
                
                # Overwrite node value
                min_value = min(min_value, evaluation)
                
                # Overwrite beta (worst position for white)
                beta = min(beta, evaluation)
                if beta <= alpha:
                    self.killer_moves[board_data.active].append(move)
                    break
            return min_value   
        
    """
    Looks at how good the current position is,
    Positive = better for white, 
    0 = neutral,
    negative, better for black
    """
    def evaluate(self, board_data: engine.BoardData) -> int:
        score = 0
        for y in range(0,8):
            for x in range(0, 8):
                weight = -1
                if board_data.board[y][x].color == piece.WHITE:
                    weight = 1
                        
                score += piece.PIECE_TO_CLASSICAL_VALUE[board_data.board[y][x].type]* weight
        return score
    
    def order(self, board_data: engine.BoardData, moves: list[engine.Move]):
        ls = [[], [], []]
        for move in moves:
            if isinstance(move, engine.Capture):
                ls[0].append(move)
           
            else: 
                for kmove in self.killer_moves[board_data.active]:
                    if move.origin.x == kmove.origin.x and move.origin.y == kmove.origin.y and move.dest.x == kmove.dest.x and move.dest.y == kmove.dest.y:
                        ls[1].append(move)
                        break
                else:
                    ls[2].append(move)
        
        return engine.flatten(ls)
         
    def first_order(self, board_data: engine.BoardData, moves: list[engine.Move]):
        return self.order(board_data, moves)