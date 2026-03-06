from tracker.call_tracker import CallTracker

tracker = CallTracker()
memo = {}

def tracked_fib_dp(n):
    call_id = tracker.record_call("fibDP", {"n": n})

    if n in memo:
        # tracker.record_action("cache_hit", {"n": n, "value": memo[n]})
        # tracker.record_phase("memo_hit")
        tracker.record_phase("dp_update", {
            "table" : memo.copy()
        })
        tracker.record_phase("memo_hit", {"n": n})
        tracker.record_return(call_id, memo[n])
        return memo[n]

    if n <= 1:
        memo[n] = n
        # tracker.record_action("store", {"n": n, "value": n})
        tracker.record_phase("memo_store", {"n": n, "value": n})

        # tracker.record_phase("memo_store")
        tracker.record_return(call_id, n)
        return n

    value = tracked_fib_dp(n-1) + tracked_fib_dp(n-2)

    memo[n] = value
    tracker.record_phase("dp_update", {
        "table" : memo.copy()
    })
    tracker.record_action("store", {"n": n, "value": value})

    tracker.record_return(call_id, value)
    return value