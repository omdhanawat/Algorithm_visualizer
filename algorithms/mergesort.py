from tracker.call_tracker import CallTracker

def get_mergesort_tracker():
    if not hasattr(get_mergesort_tracker, "tracker"):
        get_mergesort_tracker.tracker = CallTracker()
    return get_mergesort_tracker.tracker

def tracked_mergesort(arr, depth=0):
    tracker = get_mergesort_tracker()
    
    if depth == 0:
        tracker.reset()

    n = len(arr)
    call_id = tracker.record_call("merge_sort", {"arr": arr, "n": n})

    if n <= 1:
        tracker.record_phase("base_case", message=f"Array size {n} is already sorted.", state={"arr": arr})
        tracker.record_return(call_id, arr)
        return arr

    mid = n // 2
    left = arr[:mid]
    right = arr[mid:]

    tracker.record_phase(
        "divide", 
        message=f"Splitting array of size {n} into two halves.",
        i=0, j=n-1, k=mid,
        visual={"nodes": list(range(n))},
        state={"left": left, "right": right}
    )

    left_sorted = tracked_mergesort(left, depth + 1)
    right_sorted = tracked_mergesort(right, depth + 1)

    # Merge logic
    merged = []
    i = j = 0
    tracker.record_phase("merge_start", message=f"Merging two sorted halves: {left_sorted} and {right_sorted}.", state={"left": left_sorted, "right": right_sorted})

    while i < len(left_sorted) and j < len(right_sorted):
        if left_sorted[i] <= right_sorted[j]:
            tracker.record_phase("merge_step", message=f"{left_sorted[i]} <= {right_sorted[j]}. Taking from left.", i=i, state={"merged": merged + [left_sorted[i]]})
            merged.append(left_sorted[i])
            i += 1
        else:
            tracker.record_phase("merge_step", message=f"{right_sorted[j]} < {left_sorted[i]}. Taking from right.", j=j, state={"merged": merged + [right_sorted[j]]})
            merged.append(right_sorted[j])
            j += 1

    merged.extend(left_sorted[i:])
    merged.extend(right_sorted[j:])

    tracker.record_phase("merge_complete", message=f"Merge complete. Result: {merged}", state={"merged": merged})
    tracker.record_return(call_id, merged)
    return merged
