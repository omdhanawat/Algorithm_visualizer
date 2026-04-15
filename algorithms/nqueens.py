from tracker.call_tracker import CallTracker

def get_nqueens_tracker():
    if not hasattr(get_nqueens_tracker, "tracker"):
        get_nqueens_tracker.tracker = CallTracker()
    return get_nqueens_tracker.tracker

def tracked_nqueens(n):
    tracker = get_nqueens_tracker()
    tracker.reset()
    tracker.record_call("n_queens", {"n": n})
    
    board = [-1] * n # board[row] = col

    def find_conflict(row, col):
        for r in range(row):
            c = board[r]
            if c == col:
                return (r, c, "column")
            if abs(c - col) == abs(r - row):
                return (r, c, "diagonal")
        return None

    def backtrack(row):
        call_id = tracker.record_call("n_queens_row", {"row": row, "board": list(board)})

        if row == n:
            tracker.record_phase(
                "found_solution", 
                message="All queens placed safely! Solution found.", 
                state={"board": list(board)}
            )
            tracker.record_return(call_id, True)
            return True

        for col in range(n):
            conflict = find_conflict(row, col)
            
            tracker.record_phase(
                "check_position",
                message=f"Checking square ({row}, {col}).",
                i=row, j=col,
                visual={
                    "active_cells": [[row, col]],
                    "dependency_cells": [[conflict[0], conflict[1]]] if conflict else []
                },
                state={"board": list(board)}
            )

            if not conflict:
                board[row] = col
                tracker.record_phase(
                    "place_queen",
                    message=f"Square ({row}, {col}) is safe. Placing queen and moving to row {row+1}.",
                    i=row, j=col,
                    visual={"active_cells": [[row, col]]},
                    state={"board": list(board)}
                )

                if backtrack(row + 1):
                    tracker.record_return(call_id, True)
                    return True

                # Backtrack logic
                old_col = board[row]
                board[row] = -1
                tracker.record_phase(
                    "backtrack",
                    message=f"Row {row+1} had no safe squares. Backtracking: removing queen from ({row}, {old_col}).",
                    i=row, j=old_col,
                    visual={"active_cells": [[row, old_col]]},
                    state={"board": list(board)}
                )
            else:
                conf_r, conf_c, type_ = conflict
                tracker.record_phase(
                    "conflict_detected",
                    message=f"Conflict! ({row}, {col}) is attacked by the queen at ({conf_r}, {conf_c}) on the same {type_}.",
                    i=row, j=col,
                    visual={
                        "active_cells": [[row, col]],
                        "dependency_cells": [[conf_r, conf_c]]
                    },
                    state={"board": list(board)}
                )

        tracker.record_return(call_id, False)
        return False

    tracker.record_phase("init", message=f"Starting N-Queens for a {n}x{n} board. Goal: Place {n} non-attacking queens.", state={"board": board[:]})
    backtrack(0)
    tracker.record_phase("complete", message="Exploration complete.", state={"board": board[:]})
    tracker.record_return(0, board)
    return board
