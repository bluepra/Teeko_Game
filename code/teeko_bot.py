# Prannav Arora
# Ryan Almizyed
# Teeko Game

import random
import copy
import numpy as np


class TeekoBot:
    """ An object representation for an AI game player for the game Teeko2.
    """
    def __init__(self, ai_piece, level):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.board = [[' ' for j in range(5)] for i in range(5)]
        self.pieces = ['b', 'r']
        self.my_piece = ai_piece
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]
        self.level = level
    
    # Gets the AI's first move
    def AI_first_move(self, state):
        curr_state = copy.deepcopy(state)
        move = []
        (row, col) = (random.randint(1, 3), random.randint(1, 3))
        while curr_state[row][col] != ' ':
            (row, col) = (random.randint(1, 3), random.randint(1, 3))
        move.insert(0, (row, col))
        return move

    # Selects a (row, col) space for the next move. You may assume that whenever
    # this function is called, it is this player's turn to move.
    def make_move(self, state):
        # start = time.time()

        # Detect drop phase
        curr_state = copy.deepcopy(state)
        drop_phase = self.drop_phase_currently(curr_state)

        count_of_AI_pieces = 0
        move = []
        for i in range(5):
            for j in range(5):
                if curr_state[i][j] == self.my_piece:
                    count_of_AI_pieces += 1

        if(count_of_AI_pieces == 0):
            move = self.AI_first_move(curr_state)
            # end = time.time()
            # print("make_move took " + str(end - start) + " seconds")
            return move

        succ_states = self.succ(curr_state, self.my_piece)

        # TODO: implement a minimax algorithm to play better - DONE
        max_val = -5
        highest_state = None
        for succ in succ_states:
            # self.print_state(succ)
            if(self.game_value(succ) == 1):
                highest_state = succ
                break
            # temp = self.Min_Value(succ, 0)
            temp = self.Min_Value(succ, 0, -5, 5)  # Added alpha beta pruning
            if(temp > max_val):
                max_val = temp
                highest_state = succ
        # print(self.heuristic_game_value(highest_state, self.my_piece))
        # self.print_state(highest_state)

        # highest_state is going to be the best succ for AI to take
        # make the move list
        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if curr_state[i][j] == ' ' and highest_state[i][j] == self.my_piece:
                        (row, col) = (i, j)
            move.insert(0, (row, col))
        else:
            for i in range(5):
                for j in range(5):
                    if curr_state[i][j] == ' ' and highest_state[i][j] == self.my_piece:
                        # print("Line 50: " + str(i) + str(j))
                        (row, col) = (i, j)
                        move.insert(0, (row, col))
                    if curr_state[i][j] == self.my_piece and highest_state[i][j] == ' ':
                        # print("Line 54: " + str(i) + str(j))
                        (source_row, source_col) = (i, j)
                        move.insert(1, (source_row, source_col))
        # end = time.time()
        # print("make_move took " + str(end - start) + " seconds")
        return move

    # For AI's turn - used wikipedia pseudo code (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
    def Max_Value(self, state, depth, alpha, beta):
        cutoff_depth = self.level
        curr_state = copy.deepcopy(state)
        terminate = self.game_value(curr_state)
        # print("Max Value " + str(depth))
        if terminate == 1:
            return terminate

        if depth == cutoff_depth:
            return self.heuristic_game_value(curr_state, self.my_piece)

        succ_states = self.succ(curr_state, self.my_piece)
        max_val = -5
        for succ in succ_states:
            max_val = max(self.Min_Value(
                succ, depth + 1, alpha, beta), max_val)
            alpha = max(alpha, max_val)
            if alpha >= beta:
                break
        return max_val

    # For Opponent's Turn - used wikipedia pseudo code (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
    def Min_Value(self, state, depth, alpha, beta):
        cutoff_depth = self.level
        curr_state = copy.deepcopy(state)
        terminate = self.game_value(curr_state)
        #print("Min Value " + str(depth))
        if terminate == -1:
            return terminate

        if depth == cutoff_depth:
            return self.heuristic_game_value(curr_state, self.opp)

        succ_states = self.succ(curr_state, self.opp)
        min_val = 5
        for succ in succ_states:
            min_val = min(self.Max_Value(
                succ, depth + 1, alpha, beta), min_val)
            beta = min(beta, min_val)
            if beta <= alpha:
                break
        return min_val

    # If state is a terminal state returns the output of game_value(state).
    # Otherwise, returns a float between -1 and 1
    def heuristic_game_value(self, state, player):
        curr_state = copy.deepcopy(state)
        return_of_game_value = self.game_value(curr_state)
        if return_of_game_value != 0:
            return return_of_game_value

        # check horizontal
        max_horiz_score = 0
        for row in curr_state:
            horizontal_pieces = row.count(player)
            horizontal_score = horizontal_pieces / 4
            max_horiz_score = max(max_horiz_score, horizontal_score)

        # check vertical
        c = np.array(curr_state).T.tolist()
        max_vertical_score = 0
        for row in c:
            vertical_pieces = row.count(player)
            vertical_score = vertical_pieces / 4
            max_vertical_score = max(max_vertical_score, vertical_score)

        # check \ diagonal
        max_lower_diagonal_score = 0
        for i in range(2):
            for j in range(2):
                diag = []
                diag.append(curr_state[i][j])
                diag.append(curr_state[i+1][j+1])
                diag.append(curr_state[i+2][j+2])
                diag.append(curr_state[i+3][j+3])
                lower_diagonal_pieces = diag.count(player)
                lower_diagonal_score = lower_diagonal_pieces / 4
                max_lower_diagonal_score = max(
                    max_lower_diagonal_score, lower_diagonal_score)

        #check / diagonal
        max_upper_diagonal_score = 0
        for i in range(3, 5):
            for j in range(2):
                diag = []
                diag.append(curr_state[i][j])
                diag.append(curr_state[i-1][j+1])
                diag.append(curr_state[i-2][j+2])
                diag.append(curr_state[i-3][j+3])
                upper_diagonal_pieces = diag.count(player)
                upper_diagonal_score = upper_diagonal_pieces / 4
                max_upper_diagonal_score = max(
                    max_upper_diagonal_score, upper_diagonal_score)

        # check diamond
        max_diamond_score = 0
        for i in range(1, 4):
            for j in range(1, 4):
                diamond = []
                diamond.append(curr_state[i][j - 1])
                diamond.append(curr_state[i][j + 1])
                diamond.append(curr_state[i - 1][j])
                diamond.append(curr_state[i + 1][j])
                diamond_pieces = diamond.count(player)
                diamond_score = diamond_pieces / 4
                max_diamond_score = max(max_diamond_score, diamond_score)

        max_score = max(max_horiz_score, max_vertical_score,
                        max_lower_diagonal_score, max_upper_diagonal_score, max_diamond_score)

        # print(max_horiz_score)
        # print(max_vertical_score)
        # print(max_lower_diagonal_score)
        # print(max_upper_diagonal_score)
        # print(max_diamond_score)
        # print()

        if(player == self.opp):
            max_score *= -1

        return max_score

    # Given a current game board, this function returns all successor game boards - DONE
    def succ(self, state, player):
        drop_phase = True
        coord = []
        for i in range(5):
            for j in range(5):
                if state[i][j] == player:
                    coord.append((i, j))

        if len(coord) >= 4:
            drop_phase = False

        new_coords = []

        if(drop_phase):
            for i in range(5):
                for j in range(5):
                    if state[i][j] == ' ':
                        new_coords.append([(i, j)])
        else:
            #coord = [(1,3), (2,2), (4,0), (2,3)]
            for r, c in coord:
                if(c + 1 <= 4):  # Move right
                    new_coords.append([(r, c + 1), (r, c)])
                if(c - 1 >= 0):  # Move left
                    new_coords.append([(r, c - 1), (r, c)])
                if(r - 1 >= 0):  # Move Up
                    new_coords.append([(r - 1, c), (r, c)])

                    if(c + 1 <= 4):  # Move Up and right
                        new_coords.append([(r - 1, c + 1), (r, c)])
                    if(c - 1 >= 0):  # Move Up and left
                        new_coords.append([(r - 1, c - 1), (r, c)])
                if(r + 1 <= 4):  # Move Down
                    new_coords.append([(r + 1, c), (r, c)])

                    if(c + 1 <= 4):  # Move Down and right
                        new_coords.append([(r + 1, c + 1), (r, c)])
                    if(c - 1 >= 0):  # Move Down and left
                        new_coords.append([(r + 1, c - 1), (r, c)])

        # From new coords, create succ states and add to list
        all_succ_states = []
        for new_coord in new_coords:
            copy_of_state = copy.deepcopy(state)
            if len(new_coord) > 1:
                orig_pos = new_coord[1]
                if(copy_of_state[new_coord[0][0]][new_coord[0][1]] != ' '):
                    continue
                else:
                    copy_of_state[orig_pos[0]][orig_pos[1]] = ' '
            copy_of_state[new_coord[0][0]][new_coord[0][1]] = player
            all_succ_states.append(copy_of_state)

        return all_succ_states

    # Helper function is used to determine whether the state passed in is still in drop phase.

    def drop_phase_currently(self, state):
        count_of_pieces = 0
        for row in state:
            for spot in row:
                if spot != ' ':
                    count_of_pieces += 1

        # If more than (25 - 8) open spaces ' ', we are still in drop phase
        if count_of_pieces < 8:
            return True
        else:
            return False

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception(
                    'Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")
        print('-------------')

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins - DONE
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j+1] == state[i+2][j+2] == state[i+3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check / diagonal wins - DONE
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i-1][j+1] == state[i-2][j+2] == state[i-3][j+3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check diamond wins - DONE
        for i in range(1, 4):
            for j in range(1, 4):
                is_neighbourhood_full = (state[i][j - 1] != ' ') and (
                    state[i][j + 1] != ' ') and (state[i - 1][j] != ' ') and (state[i + 1][j] != ' ')
                if state[i][j] == ' ' and is_neighbourhood_full and (state[i][j - 1] == state[i][j + 1] == state[i - 1][j] == state[i + 1][j]):
                    return 1 if state[i-1][j] == self.my_piece else -1

        return 0  # no winner yet
