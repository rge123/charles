import copy
import ChessOopsie


class Board(object):
    def __init__(self, board=None, turns=0, turn="W"):
        if board is None:
            self.board = [[Rook("B", "a8"), Horse("B", "b8"), Bishop("B", "c8"), Queen("B", "d8"), King("B", "e8"), Bishop("B", "f8"), Horse("B", "g8"), Rook("B", "h8")],
                        [Pawn("B", "a7"), Pawn("B", "b7"), Pawn("B", "c7"), Pawn("B", "d7"), Pawn("B", "e7"), Pawn("B", "f7"), Pawn("B", "g7"), Pawn("B", "h7")],
                        [Space(" ", "a6"), Space(" ", "b6"), Space(" ", "c6"), Space(" ", "d6"), Space(" ", "e6"), Space(" ", "f6"), Space(" ", "g6"), Space(" ", "h6")],
                        [Space(" ", "a5"), Space(" ", "b5"), Space(" ", "c5"), Space(" ", "d5"), Space(" ", "e5"), Space(" ", "f5"), Space(" ", "g5"), Space(" ", "h5")],
                        [Space(" ", "a4"), Space(" ", "b4"), Space(" ", "c4"), Space(" ", "d4"), Space(" ", "e4"), Space(" ", "f4"), Space(" ", "g4"), Space(" ", "h4")],
                        [Space(" ", "a3"), Space(" ", "b3"), Space(" ", "c3"), Space(" ", "d3"), Space(" ", "e3"), Space(" ", "f3"), Space(" ", "g3"), Space(" ", "h3")],
                        [Pawn("W", "a2"), Pawn("W", "b2"), Pawn("W", "c2"), Pawn("W", "d2"), Pawn("W", "e2"), Pawn("W", "f2"), Pawn("W", "g2"), Pawn("W", "h2")],
                        [Rook("W", "a1"), Horse("W", "b1"), Bishop("W", "c1"), Queen("W", "d1"), King("W", "e1"), Bishop("W", "f1"), Horse("W", "g1"), Rook("W", "h1")]]
        else:
            self.board = board
        self.turns = turns
        self.turn = turn
        self.alpha = 'abcdefgh'
        self.captured_pieces = []
        self.old_board = None


    def __str__(self):
        return '\n'.join((''.join(str(x)) for x in self.board))
    
    def get_move_vector(self, start, end):
        start = self.square_to_coords(start)
        end = self.square_to_coords(end)
        return (end[0]-start[0], end[1]-start[1])
    

    
    def move(self, start, end):
        print(f"Move: {self.turns}, Turn: {self.turn}")
        self.get_square(end)
        move_vector = self.get_move_vector(start, end)
        piece = self.find_piece(start)
        piece.move(self, end, move_vector)
        self.old_board = self.board
        print('\n'.join((''.join(str(x)) for x in self.board)))

        if self.turn == "W":
            self.turn = "B"
        else:
            self.turns += 1
            self.turn = "W"
        print()
        print('='*79)
        print()

    def square_to_coords(self, square):
        col, row = list(square)
        return (8 - int(row), self.alpha.index(col))

    def get_square(self, square):
        row, col = self.square_to_coords(square)
        try:
            return self.board[row][col]
        except IndexError:
            raise ChessOopsie.FindPieceError("That square is not on the board!")

    def find_piece(self, start):
        piece = self.get_square(start)
        if isinstance(piece, type(Space())):
            raise ChessOopsie.FindPieceError(f"The square {start} has no piece on it")
        if piece.colour != self.turn:
            raise ChessOopsie.FindPieceError(f"The {piece} piece is not the same colour as the current turn: {self.turn}")
        
        return piece
    
    def move_collision(self, move_vector, piece):
        def get_sign(x):
            if x > 0 :
                return 1
            elif x < 0:
                return -1
            else:
                return 0
        start = piece.loc
        
        start_coord = self.square_to_coords(start)
        multiplier = abs(max(*move_vector))
        unit = tuple(map(get_sign, move_vector))

        if isinstance(piece, (type(King()), type(Horse()), type(Pawn()))):
            return False

        for i in range(1, multiplier):
            row = i * unit[0] + start_coord[0]
            col = i * unit[1] + start_coord[1]
            if not isinstance(self.board[row][col], type(Space())):
                return True

        return False
    
    def find_king(self, colour):
        for row in self.board:
            for piece in row:
                if type(piece) == type(King()) and piece.colour == colour:
                    return piece
        raise ValueError("No King on board!")

    def is_check(self):
        king = self.find_king(self.turn)
        coords = self.square_to_coords(king.loc)
        if self.turn == "W":
            pawn1_y = coords[0] - 1
            pawn1_x = coords[1] - 1
            pawn2_x = coords[1] + 1
            
            pawn_condition = type(self.board[pawn1_x][pawn1_y]) == type(Pawn()) or type(self.board[pawn2_x][pawn1_y]) == type(Pawn())


            try:
                if any(pawn_condition,):
                    return True
            except IndexError:
                pass 
class Piece(object):
    def __init__(self, colour=None, loc=None):
        self.colour = colour
        self.loc = loc
        self.moves = 0

    def __str__(self):
        return self.colour + self.symbol
    
    def __repr__(self):
        return self.colour + self.symbol
    
    def check_move_is_legal(self, move_vector, board, end):
        if move_vector not in self.move_vectors:
            raise ChessOopsie.MoveError(f"{self} cannot move that far")
        if isinstance(self, type(Pawn())) and ((move_vector[0] > 0 and self.colour == 'W') or (move_vector[0] < 0 and self.colour == 'B')):
            raise ChessOopsie.MoveError("Pawns can only move forward") 
        if isinstance(self, type(Pawn())) and (abs(move_vector[0]) > 1) and (self.loc[1] != ("2" if self.colour == "W" else "7")):
            raise ChessOopsie.MoveError("Pawns can only double move at the beginning")
        if isinstance(self, type(Pawn())) and (abs(move_vector[1]) > 0) and isinstance(board.get_square(end), type(Space())):
            raise ChessOopsie.MoveError("Pawns cannot move diagonaly into an empty space")
        if isinstance(self, type(Pawn())) and (abs(move_vector[1]) == 0) and not isinstance(board.get_square(end), type(Space())):
            raise ChessOopsie.MoveError("Pawns cannot attck forward")
        if isinstance(self, type(King())) and abs(move_vector[1] > 1) and ((self.loc != ("e1" if self.colour == "W" else "e8")) or (type(board.get_square("h1" if self.colour == "W" else "h8")) != type(Rook()))):
            raise ChessOopsie.MoveError("Can only short castle if king and rook are in start positions")
        if board.move_collision(move_vector, self):
            raise ChessOopsie.MoveError("Only Horses can jump over other pieces")
        #TODO: check

    def castle(self, board):
        if self.colour == "W":
            board.board[7][5] = board.get_square("h1")
            board.board[7][7] = Space(" ", "h1")
        else:
            board.board[0][5] = board.get_square("h8")
            board.board[0][7] = Space(" ", "h8")
        print("Short castle")
            

    
    def move(self, board, end, move_vector):
        self.check_move_is_legal(move_vector, board, end)
        start_coord = board.square_to_coords(self.loc)
        end_piece = board.get_square(end)
        old_loc = self.loc
        self.loc = end
        self.moves += 1
        end_coord = board.square_to_coords(end)
        board.board[start_coord[0]][start_coord[1]] = Space(" ", end)
        board.board[end_coord[0]][end_coord[1]] = self

        if self.symbol == "K" and abs(move_vector[1]) > 1:
            self.castle(board)

        if board.is_check():
            self.board = self.old_board
            self.moves -= 1
            self.loc = old_loc
            raise ChessOopsie.MoveError("You cannot move a piece that results in self check")

        if not isinstance(end_piece, type(Space())):
            board.captured_pieces.append(end_piece)
            print(f"{board.turn} captured {end_piece} on {end}")

class Space(Piece):
    symbol = ' '

class Pawn(Piece):
    symbol = 'P'
    move_vectors = [(1, 0), (2, 0), (1, 1), (1, -1),
                    (-1, 0), (-2, 0), (-1, 1), (-1, -1)]
    worth = 1

class Rook(Piece):
    symbol = 'R'
    move_vectors = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0,7),
                    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                    (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]
    worth = 5

class Horse(Piece):
    symbol = 'H'
    move_vectors = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (1, 2), (1, -2)]
    worth = 3

class Bishop(Piece):
    symbol = 'B'
    move_vectors = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7),
                    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
    worth = 3

class Queen(Piece):
    symbol = 'Q'
    move_vectors = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0,7),
                    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                    (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7),
                    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7),
                    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]
    worth = 9

class King(Piece):
    symbol = 'K'
    move_vectors = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1),
                    (0, 2)] #TODO add long castle



def main():
    board = Board()
    board.move("e2", "e4")
    board.move("e7", "e5")
    board.move("f1", "c4")
    board.move("d8", "h4")
    board.move("d2", "d3")
    board.move("f8", "b4")
    board.move("b1", "c3")
    board.move("b8", "a6")
    board.move("g1", "f3")
    board.move("b4", "c3")
    board.move("b2", "c3")
    board.move("a6", "c5")
    board.move("e1", "g1")
    board.move("h4", "e7")
    

if __name__ == '__main__':
    main()