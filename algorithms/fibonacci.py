from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_fib(n):
    call_id = tracker.record_call("fib", {"n": n})

    if n <= 1:
        tracker.record_return(call_id, n)
        return n

    result = tracked_fib(n-1) + tracked_fib(n-2)

    tracker.record_return(call_id, result)
    return result