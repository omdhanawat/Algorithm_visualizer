from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_lis(arr):

    n = len(arr)
    dp = [1] * n

    tracker.record_call("lis", {"array": arr})

    for i in range(n):
        for j in range(i):

            tracker.record_phase("compare", {
                "i": i,
                "j": j,
                "a_i": arr[i],
                "a_j": arr[j]
            })

            if arr[j] < arr[i]:

                new_val = dp[j] + 1

                if new_val > dp[i]:
                    dp[i] = new_val

                    tracker.record_phase("update", {
                        "i": i,
                        "j": j,
                        "dp": dp[:]
                    })

    result = max(dp)

    tracker.record_return(0, result)

    return result