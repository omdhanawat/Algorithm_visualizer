from tracker.call_tracker import CallTracker

tracker = CallTracker()


def tracked_mergesort(arr):
    call_id = tracker.record_call("m", {"arr": arr.copy()})

    if len(arr) <= 1:
        tracker.record_return(call_id, arr.copy())
        return arr

    mid = len(arr) // 2

    left_part = arr[:mid]
    right_part = arr[mid:]

    # tracker.record_action("split", {"left": left_part, "right": right_part})
    tracker.record_phase("divide")
    tracker.record_action("state", {"array": arr.copy(), "stage": "current"})

    left = tracked_mergesort(left_part)
    right = tracked_mergesort(right_part)

    tracker.record_action("merge_start", {"left": left, "right": right})

    merged = merge(left, right)

    # tracker.record_action("merge_result", {"result": merged})
    tracker.record_phase("combine", {"result": merged})

    tracker.record_return(call_id, merged.copy())
    return merged

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

