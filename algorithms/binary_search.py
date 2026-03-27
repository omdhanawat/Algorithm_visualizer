from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_binary_search(arr, target, low=0, high=None):

    if high is None:
        high = len(arr) - 1

    call_id = tracker.record_call("binarySearch", {
        "low": low,
        "high": high,
        "target": target
    })

    if low > high:
        tracker.record_return(call_id, -1)
        return -1

    mid = (low + high) // 2

    tracker.record_phase("mid", {
        "low": low,
        "high": high,
        "mid": mid,
        "value": arr[mid]
    })

    if arr[mid] == target:
        tracker.record_phase("found", {"index": mid})
        tracker.record_return(call_id, mid)
        return mid

    elif arr[mid] < target:
        tracker.record_phase("right", {"new_low": mid + 1})
        result = tracked_binary_search(arr, target, mid + 1, high)

    else:
        tracker.record_phase("left", {"new_high": mid - 1})
        result = tracked_binary_search(arr, target, low, mid - 1)

    tracker.record_return(call_id, result)
    return result