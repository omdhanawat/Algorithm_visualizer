from tracker.call_tracker import CallTracker

def get_fib_tracker():
    if not hasattr(get_fib_tracker, "tracker"):
        get_fib_tracker.tracker = CallTracker()
    return get_fib_tracker.tracker

def tracked_fib(n):
    """
    Tracked recursive Fibonacci.
    NOTE: tracker.reset() must be called BEFORE calling this function.
    The API (main_api.py) and main.py both do this. Do NOT reset inside
    the recursive function body or the call stack will be corrupted.
    """
    tracker = get_fib_tracker()

    call_id = tracker.record_call("fibonacci_rec", {"n": n})

    if n == 0 or n == 1:
        tracker.record_phase(
            "base_case",
            message=f"F({n}) is a base case. Returning {n}.",
            i=n,
            visual={"nodes": [n]},
            state={"result": n}
        )
        tracker.record_return(call_id, n)
        return n

    tracker.record_phase(
        "recursive_call",
        message=f"F({n}) needs F({n-1}) and F({n-2}). Branching into two sub-problems.",
        i=n,
        visual={"nodes": [n]}
    )

    res1 = tracked_fib(n - 1)
    res2 = tracked_fib(n - 2)
    result = res1 + res2

    tracker.record_phase(
        "sum_results",
        message=f"F({n}) = F({n-1}) + F({n-2}) = {res1} + {res2} = {result}",
        i=n,
        visual={"nodes": [n]},
        state={"res1": res1, "res2": res2, "result": result}
    )
    tracker.record_return(call_id, result)
    return result