from tracker.call_tracker import CallTracker

def get_knapsack_tracker():
    if not hasattr(get_knapsack_tracker, "tracker"):
        get_knapsack_tracker.tracker = CallTracker()
    return get_knapsack_tracker.tracker

def tracked_knapsack(weights, values, capacity):
    n = len(weights)
    tracker = get_knapsack_tracker()
    tracker.reset()
    call_id = tracker.record_call("knapsack_01", {"weights": weights, "values": values, "capacity": capacity})

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    def snapshot():
        return [row[:] for row in dp]

    tracker.record_phase(
        "init", 
        message=f"Initialized DP table ({n+1}x{capacity+1}) with zeros. Rows: Items, Cols: Capacity.", 
        state={"dp": snapshot()}
    )

    for i in range(1, n + 1):
        w = weights[i-1]
        v = values[i-1]
        for j in range(capacity + 1):
            if w <= j:
                # Option 1: Take the item
                take = v + dp[i-1][j - w]
                # Option 2: Skip the item
                skip = dp[i-1][j]
                
                dp[i][j] = max(take, skip)
                
                reason = f"Item {i} fits (weight {w}). Take it (+{v}) or skip? Max({take}, {skip}) = {dp[i][j]}."
                deps = [[i-1, j - w], [i-1, j]]
            else:
                dp[i][j] = dp[i-1][j]
                reason = f"Item {i} is too heavy (weight {w} > capacity {j}). Inheriting value from row above."
                deps = [[i-1, j]]

            tracker.record_phase(
                "update_cell",
                message=reason,
                i=i, j=j,
                visual={
                    "active_cells": [[i, j]],
                    "dependency_cells": deps
                },
                state={"dp": snapshot()}
            )

    tracker.record_phase("complete", message=f"Max value for capacity {capacity} is {dp[n][capacity]}.", state={"dp": snapshot()})
    tracker.record_return(call_id, dp[n][capacity])
    return dp[n][capacity]