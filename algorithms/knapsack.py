from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_knapsack(weights, values, W):

    n = len(weights)

    # DP table
    dp = [[0 for _ in range(W+1)] for _ in range(n+1)]

    tracker.record_call("knapsack", {
        "items": n,
        "capacity": W
    })

    for i in range(1, n+1):
        for w in range(W+1):

            tracker.record_phase("consider", {
                "i": i,
                "w": w
            })

            if weights[i-1] <= w:

                include = values[i-1] + dp[i-1][w - weights[i-1]]
                exclude = dp[i-1][w]

                dp[i][w] = max(include, exclude)

                tracker.record_phase("update", {
                    "i": i,
                    "w": w,
                    "include": include,
                    "exclude": exclude,
                    "chosen": dp[i][w],
                    "table": [row[:] for row in dp]
                })

            else:
                dp[i][w] = dp[i-1][w]

                tracker.record_phase("skip", {
                    "i": i,
                    "w": w,
                    "table": [row[:] for row in dp]
                })

    tracker.record_return(0, dp[n][W])

    return dp[n][W]