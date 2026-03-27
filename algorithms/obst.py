from tracker.call_tracker import CallTracker

tracker = CallTracker()

def tracked_obst(keys, freq):
    n = len(keys)
    
    # 1-indexed conversion internally to match standard OBST DP formula exactly
    keys_1 = [None] + keys
    freq_1 = [0] + freq
    
    # cost[i][j] will store optimal cost of BST for keys i..j
    # size is (n+2) x (n+1) to accommodate i up to n+1 and j up to n
    cost = [[0]*(n+1) for _ in range(n+2)]
    root = [[0]*(n+1) for _ in range(n+2)]

    tracker.record_call("obst", {"keys": keys, "freq": freq})

    # Length 1 trees and empty trees
    for i in range(1, n+2):
        cost[i][i-1] = 0
        
    for i in range(1, n+1):
        cost[i][i] = freq_1[i]
        root[i][i] = i
        
        # We can record the initialization update
        tracker.record_phase("update", {
            "i": i,
            "j": i,
            "value": cost[i][i],
            "table": [row[:] for row in cost]
        })

    # Lengths L from 2 up to n
    for L in range(2, n+1):
        for i in range(1, n - L + 2):
            j = i + L - 1
            cost[i][j] = float('inf')
            
            # Sum of frequencies from i to j
            weight = sum(freq_1[r] for r in range(i, j+1))
            
            for k in range(i, j+1):
                c = cost[i][k-1] + cost[k+1][j] + weight
                
                tracker.record_phase("consider_root", {
                    "i": i,
                    "j": j,
                    "k": k,
                    "cost": c,
                    "best_so_far": cost[i][j] if cost[i][j] != float('inf') else "∞"
                })
                
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = k
                    
            # After checking all roots 'k', we update the optimal cost for this range.
            tracker.record_phase("update", {
                "i": i,
                "j": j,
                "value": cost[i][j],
                "table": [row[:] for row in cost]
            })

    # Construct the tree recursively from the root table
    def build_tree_events(i, j, parent_id=None, side=None):
        if i > j:
            return None
        
        # Getting the optimal root for the range i..j
        k = root[i][j]
        node_id = f"node_{i}_{j}"
        
        tracker.record_phase("build_tree", {
            "id": node_id,
            "label": str(keys_1[k]),
            "parent": parent_id,
            "side": side
        })
        
        # Recursively build left and right subtrees
        build_tree_events(i, k-1, node_id, "left")
        build_tree_events(k+1, j, node_id, "right")

    build_tree_events(1, n)

    tracker.record_return(0, cost[1][n])
    return cost[1][n]
