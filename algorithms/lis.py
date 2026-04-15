from tracker.call_tracker import CallTracker

def get_lis_tracker():
    if not hasattr(get_lis_tracker, "tracker"):
        get_lis_tracker.tracker = CallTracker()
    return get_lis_tracker.tracker

def tracked_lis(arr):
    n = len(arr)
    tracker = get_lis_tracker()
    tracker.reset()
    call_id = tracker.record_call("longest_increasing_subsequence", {"arr": arr, "n": n})

    if n == 0: return 0
    
    lis = [1] * n
    tracker.record_phase("init", message="Initialized LIS array with 1 (each element is a subsequence of length 1).", state={"lis": list(lis)})

    for i in range(1, n):
        for j in range(0, i):
            tracker.record_phase(
                "check_extension",
                message=f"Checking if arr[{j}] ({arr[j]}) < arr[{i}] ({arr[i]}) to extend subsequence ending at {j}.",
                i=i, j=j,
                visual={
                    "active_cells": [[0, i]],
                    "dependency_cells": [[0, j]]
                },
                state={"lis": list(lis)}
            )
            if arr[i] > arr[j] and lis[i] < lis[j] + 1:
                lis[i] = lis[j] + 1
                tracker.record_phase(
                    "update_lis",
                    message=f"Condition met! New LIS ending at index {i} is length {lis[i]}.",
                    i=i,
                    state={"lis": list(lis)}
                )

    result = max(lis)
    tracker.record_phase("complete", message=f"LIS complete. Length of longest increasing subsequence is {result}.", state={"lis": list(lis)})
    tracker.record_return(call_id, result)
    return result