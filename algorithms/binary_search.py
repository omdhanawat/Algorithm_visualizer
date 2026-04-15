from tracker.call_tracker import CallTracker

def get_binary_search_tracker():
    if not hasattr(get_binary_search_tracker, "tracker"):
        get_binary_search_tracker.tracker = CallTracker()
    return get_binary_search_tracker.tracker

def tracked_binary_search(arr, target, low=0, high=None):
    tracker = get_binary_search_tracker()
    
    if high is None:
        tracker.reset()
        high = len(arr) - 1

    call_id = tracker.record_call("binary_search", {
        "arr": arr,
        "low": low,
        "high": high,
        "target": target
    })

    if low > high:
        tracker.record_phase(
            "target_not_found", 
            message=f"Search range is empty (low {low} > high {high}). Target {target} is not in the array.",
            state={"arr": arr, "low": low, "high": high, "target": target}
        )
        tracker.record_return(call_id, -1)
        return -1

    mid = (low + high) // 2

    tracker.record_phase(
        "check_middle", 
        message=f"Checking middle element at index {mid}. Value {arr[mid]} vs Target {target}.", 
        i=mid,
        visual={"nodes": [mid], "active_cells": [mid]},
        state={"arr": arr, "low": low, "high": high, "mid": mid, "target": target}
    )

    if arr[mid] == target:
        tracker.record_phase(
            "target_found", 
            message=f"Match! Target {target} found at index {mid}.", 
            i=mid, 
            visual={"nodes": [mid], "active_cells": [mid]},
            state={"arr": arr, "low": low, "high": high, "mid": mid, "target": target, "found_index": mid}
        )
        tracker.record_return(call_id, mid)
        return mid

    elif arr[mid] < target:
        tracker.record_phase(
            "search_right", 
            message=f"{arr[mid]} < {target}. Since the array is sorted, the target must be in the right half. Discarding indices {low} to {mid}.", 
            i=mid,
            visual={"nodes": [mid], "active_cells": [mid]},
            state={"arr": arr, "low": low, "new_low": mid + 1, "high": high, "target": target}
        )
        result = tracked_binary_search(arr, target, mid + 1, high)

    else:
        tracker.record_phase(
            "search_left", 
            message=f"{arr[mid]} > {target}. Since the array is sorted, the target must be in the left half. Discarding indices {mid} to {high}.", 
            i=mid,
            visual={"nodes": [mid], "active_cells": [mid]},
            state={"arr": arr, "low": low, "high": high, "new_high": mid - 1, "target": target}
        )
        result = tracked_binary_search(arr, target, low, mid - 1)

    tracker.record_return(call_id, result)
    return result
