from tracker.call_tracker import CallTracker

def get_fib_dp_tracker():
    if not hasattr(get_fib_dp_tracker, "tracker"):
        get_fib_dp_tracker.tracker = CallTracker()
    return get_fib_dp_tracker.tracker

def tracked_fib_dp(n):
    tracker = get_fib_dp_tracker()
    tracker.reset()
    call_id = tracker.record_call("fibonacci_dp", {"n": n})
    
    if n <= 1:
        tracker.record_phase("base", message=f"F({n}) is {n}.", i=n, state={"dp": [0, 1][:n+1]})
        tracker.record_return(call_id, n)
        return n

    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1
    
    tracker.record_phase(
        "init", 
        message="Initialized DP table with base cases F(0)=0 and F(1)=1.", 
        state={"dp": list(dp)}
    )

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        tracker.record_phase(
            "calculate", 
            message=f"F({i}) = F({i-1}) + F({i-2}) = {dp[i-1]} + {dp[i-2]} = {dp[i]}.", 
            i=0, j=i,
            visual={
                "active_cells": [[0, i]], 
                "dependency_cells": [[0, i-1], [0, i-2]]
            },
            state={"dp": list(dp)}
        )

    tracker.record_phase("complete", message=f"DP complete. F({n}) = {dp[n]}", state={"dp": list(dp)})
    tracker.record_return(call_id, dp[n])
    return dp[n]