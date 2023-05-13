import copy
import ChessOopsie


class Board(object):
    def __init__(self):
        self.board = [[Rook("B", "a8"), Horse("B", "b8"), Bishop("B", "c8"), Queen("B", "d8"), King("B", "e8"), Bishop("B", "f8"), Horse("B", "g8"), Rook("B", "h8")],
                      [Pawn("B", "a7"), Pawn("B", "b7"), Pawn("B", "c7"), Pawn("B", "d7"), Pawn("B", "e7"), Pawn("B", "f7"), Pawn("B", "g7"), Pawn("B", "h7")],
                      [Space(" ", "a6"), Space(" ", "b6"), Space(" ", "c6"), Space(" ", "d6"), Space(" ", "e6"), Space(" ", "f6"), Space(" ", "g6"), Space(" ", "h6")],
                      [Space(" ", "a5"), Space(" ", "b5"), Space(" ", "c5"), Space(" ", "d5"), Space(" ", "e5"), Space(" ", "f5"), Space(" ", "g5"), Space(" ", "h5")],
                      [Space(" ", "a4"), Space(" ", "b4"), Space(" ", "c4"), Space(" ", "d4"), Space(" ", "e4"), Space(" ", "f4"), Space(" ", "g4"), Space(" ", "h4")],
                      [Space(" ", "a3"), Space(" ", "b3"), Space(" ", "c3"), Space(" ", "d3"), Space(" ", "e3"), Space(" ", "f3"), Space(" ", "g3"), Space(" ", "h3")],
                      [Pawn("W", "a2"), Pawn("W", "b2"), Pawn("W", "c2"), Pawn("W", "d2"), Pawn("W", "e2"), Pawn("W", "f2"), Pawn("W", "g2"), Pawn("W", "h2")],
                      [Rook("W", "a1"), Horse("W", "b1"), Bishop("W", "c1"), Queen("W", "d1"), King("W", "e1"), Bishop("W", "f1"), Horse("W", "g1"), Rook("W", "h1")]]
        self.turn = "W"
        self.turns = 0
        self.alpha = 'abcdefgh'


    def __str__(self):
        return '\n'.join((''.join(str(x)) for x in self.board))
    
    def get_move_vector(self, start, end):
        pass
    
    def move(self, start, end):
        self.check_moves_are_on_board(start, end)
        move_vector = self.get_move_vector(start, end)
        piece = self.find_piece(start)
        piece.move(self, end, move_vector)
        if self.turn == "W":
            self.turn == "B"
            print(f"It is now turn for {self.turn}")
        else:
            self.turns += 1
            self.turn == "W"
            print(f"End of move:{self.turns}. It is now turn for {self.turn}")

    def get_square(self, square):
        col, row = list(square)
        try:
            return self.board[8 - int(row)][self.alpha.index(col)]
        except IndexError:
            raise ChessOopsie.FindPieceError("That square is not on the board!")

    def find_piece(self, start):
        piece = self.get_square(start)
        if isinstance(piece, type(Space())):
            raise ChessOopsie.FindPieceError(f"The start square {start} has no piece on it")
        if piece.colour != self.turn:
            raise ChessOopsie.FindPieceError(f"The {piece} piece is not the same colour as the current turn: {self.turn}")
        
        return piece



class Piece(object):
    def __init__(self, colour=None, loc=None):
        self.colour = colour
        self.loc = loc

    def __str__(self):
        return self.colour + self.symbol
    
    def __repr__(self):
        return self.colour + self.symbol
    
    def check_move_is_legal(self, move_vector):
        if move_vector not in self.move_vectors:
            raise ChessOopsie.MoveError(f"{self} cannot move that far")
        

    
    def move(self, board, end, move_vector):
        self.check_move_is_legal(move_vector)
        end_square = board.get_square(end)
        pass

    

class Space(Piece):
    symbol = ' '

class Pawn(Piece):
    symbol = 'P'
    move_vectors = [(1, 0), (2, 0), (1, 1), (1, -1)]

class Rook(Piece):
    symbol = 'R'
    move_vectors = [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0,7),
                    (-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0), (-6, 0), (-7, 0),
                    (0, -1), (0, -2), (0, -3), (0, -4), (0, -5), (0, -6), (0, -7)]

class Horse(Piece):
    symbol = 'H'
    move_vectors = [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (1, 2), (1, -2)]

class Bishop(Piece):
    symbol = 'B'
    move_vectors = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                    (1, -1), (2, -2), (3, -3), (4, -4), (5, -5), (6, -6), (7, -7),
                    (-1, -1), (-2, -2), (-3, -3), (-4, -4), (-5, -5), (-6, -6), (-7, -7),
                    (-1, 1), (-2, 2), (-3, 3), (-4, 4), (-5, 5), (-6, 6), (-7, 7)]

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

class King(Piece):
    symbol = 'K'
    move_vectors = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]



def main():
    board = Board()
    #print(board)
    board.move("e7", "e4")

if __name__ == '__main__':
    main()