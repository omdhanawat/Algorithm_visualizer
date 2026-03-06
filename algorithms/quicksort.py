from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_quicksort(arr):
    call_id = tracker.record_call("quickSort", {"arr": arr.copy()})

    if len(arr) <= 1:
        tracker.record_return(call_id, arr.copy())
        return arr

    pivot = arr[0]
    # tracker.record_action("pivot", {"pivot": pivot, "array": arr.copy()})
    tracker.record_phase("choose", {"pivot": pivot})

    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]

    tracker.record_action("partition", {"left": left, "right": right})

    sorted_left = tracked_quicksort(left)
    sorted_right = tracked_quicksort(right)

    result = sorted_left + [pivot] + sorted_right

    tracker.record_action("combine", {"result": result})

    tracker.record_return(call_id, result.copy())
    return result