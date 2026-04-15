from tracker.call_tracker import CallTracker

def get_fib_tracker():
    if not hasattr(get_fib_tracker, "tracker"):
        get_fib_tracker.tracker = CallTracker()
    return get_fib_tracker.tracker

def tracked_fib(n):
    tracker = get_fib_tracker()
    
    if n == 0 or n == 1:
        call_id = tracker.record_call("fibonacci_rec", {"n": n})
        tracker.record_phase(
            "base_case", 
            message=f"F({n}) is a base case. Returning {n}.", 
            i=n,
            visual={"nodes": [n]},
            state={"result": n}
        )
        tracker.record_return(call_id, n)
        return n

    call_id = tracker.record_call("fibonacci_rec", {"n": n})
    tracker.record_phase(
        "recursive_call", 
        message=f"F({n}) needs simpler values: F({n-1}) and F({n-2}). Branching out.", 
        i=n,
        visual={"nodes": [n]}
    )
    
    res1 = tracked_fib(n-1)
    res2 = tracked_fib(n-2)
    result = res1 + res2

    tracker.record_phase(
        "sum_results", 
        message=f"Combining results: F({n}) = F({n-1}) + F({n-2}) = {res1} + {res2} = {result}", 
        i=n,
        visual={"nodes": [n]},
        state={"res1": res1, "res2": res2, "result": result}
    )
    tracker.record_return(call_id, result)
    return result