from tracker.call_tracker import CallTracker

def get_lcs_tracker():
    if not hasattr(get_lcs_tracker, "tracker"):
        get_lcs_tracker.tracker = CallTracker()
    return get_lcs_tracker.tracker

def tracked_lcs(X, Y):
    m, n = len(X), len(Y)
    tracker = get_lcs_tracker()
    tracker.reset()
    call_id = tracker.record_call("longest_common_subsequence", {"X": X, "Y": Y})

    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    tracker.record_phase("init", message=f"Initialized {m+1}x{n+1} DP table with zeros.", state={"dp": dp})

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                reason = f"Character match: '{X[i-1]}'. diagonal increment: {dp[i-1][j-1]} + 1."
                deps = [[i-1, j-1]]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                reason = f"Mismatch: '{X[i-1]}' != '{Y[j-1]}'. Max(top: {dp[i-1][j]}, left: {dp[i][j-1]}) = {dp[i][j]}."
                deps = [[i-1, j], [i, j-1]]

            tracker.record_phase(
                "update_cell",
                message=reason,
                i=i, j=j,
                visual={
                    "active_cells": [[i, j]],
                    "dependency_cells": deps
                },
                state={"dp": dp}
            )

    # Backtracking Phase
    tracker.record_phase("backtrack_start", message="LCS table complete. Backtracking to reconstruct the string sequence.", state={"dp": dp})
    
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            tracker.record_phase("backtrack_match", message=f"Found match '{X[i-1]}'. Moving diagonally.", i=i, j=j, visual={"active_cells": [[i, j]]})
            lcs_str.append(X[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            tracker.record_phase("backtrack_move", message="Moving up (top > left).", i=i, j=j, visual={"active_cells": [[i, j]]})
            i -= 1
        else:
            tracker.record_phase("backtrack_move", message="Moving left.", i=i, j=j, visual={"active_cells": [[i, j]]})
            j -= 1

    final_lcs = "".join(reversed(lcs_str))
    tracker.record_phase("complete", message=f"LCS reconstruction complete: {final_lcs}.", state={"dp": dp, "lcs": final_lcs})
    tracker.record_return(call_id, final_lcs)
    return final_lcs