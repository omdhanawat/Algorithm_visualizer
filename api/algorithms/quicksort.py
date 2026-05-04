from tracker.call_tracker import CallTracker

def get_quicksort_tracker():
    if not hasattr(get_quicksort_tracker, "tracker"):
        get_quicksort_tracker.tracker = CallTracker()
    return get_quicksort_tracker.tracker

def tracked_quicksort(arr, depth=0):
    tracker = get_quicksort_tracker()
    
    if depth == 0:
        tracker.reset()

    n = len(arr)
    call_id = tracker.record_call("quick_sort", {"arr": arr, "n": n})

    if n <= 1:
        tracker.record_phase(
            "base_case",
            message=f"Array {arr} has size {n}. It is already sorted.",
            state={"arr": arr, "result": arr}
        )
        tracker.record_return(call_id, arr)
        return arr

    pivot_idx = n // 2
    pivot = arr[pivot_idx]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    tracker.record_phase(
        "partition", 
        message=f"Partitioning around pivot {pivot} (from mid index {pivot_idx}). Items smaller move left, larger move right.",
        i=pivot_idx,
        visual={"nodes": [pivot_idx], "active_cells": [pivot_idx]},
        state={"arr": arr, "pivot": pivot, "left": left, "middle": middle, "right": right}
    )

    result = tracked_quicksort(left, depth + 1) + middle + tracked_quicksort(right, depth + 1)
    
    tracker.record_phase("sorted", message=f"Subproblems sorted and combined into {result}.", state={"arr": result, "result": result})
    tracker.record_return(call_id, result)
    return result
