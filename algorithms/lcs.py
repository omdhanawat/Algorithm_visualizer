from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_lcs(s1, s2):

    n = len(s1)
    m = len(s2)

    dp = [[0]*(m+1) for _ in range(n+1)]

    tracker.record_call("lcs", {"s1": s1, "s2": s2})

    for i in range(1, n+1):
        for j in range(1, m+1):

            tracker.record_phase("compare", {
                "i": i,
                "j": j,
                "c1": s1[i-1],
                "c2": s2[j-1]
            })

            if s1[i-1] == s2[j-1]:

                dp[i][j] = 1 + dp[i-1][j-1]

                tracker.record_phase("update", {
                    "i": i,
                    "j": j,
                    "value": dp[i][j],
                    "table": [row[:] for row in dp]
                })

            else:

                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

                tracker.record_phase("update", {
                    "i": i,
                    "j": j,
                    "value": dp[i][j],
                    "table": [row[:] for row in dp]
                })

    tracker.record_return(0, dp[n][m])
    return dp[n][m]