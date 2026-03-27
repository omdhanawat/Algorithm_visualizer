from tracker.call_tracker import CallTracker

tracker = CallTracker()

def solve_nqueens(n, tracker):

    board = [-1] * n   

    def is_safe(row, col):
        for r in range(row):
            c = board[r]

            if c == col or abs(c - col) == abs(r - row):
                return False

        return True


    def backtrack(row):

        call_id = tracker.record_call("nQueens", {"row": row})

        if row == n:
            tracker.record_phase("solution", {"board": board.copy()})
            tracker.record_return(call_id, board.copy())
            return True

        for col in range(n):

            tracker.record_phase("explore", {
                "row": row, 
                "col": col,
                "board": board.copy()
                })

            if is_safe(row, col):

                board[row] = col

                tracker.record_phase("place", {
                    "row": row,
                    "col": col,
                    "board": board.copy()
                })

                if backtrack(row + 1):
                    tracker.record_return(call_id, board.copy())
                    return True

                board[row] = -1

                tracker.record_phase("remove", {
                    "row": row,
                    "col": col,
                    "board": board.copy()
                })

            else:
                tracker.record_phase("invalid", {
                    "row": row,
                    "col": col,
                    "board": board.copy()
                    })

        tracker.record_return(call_id, None)
        return False


    backtrack(0)