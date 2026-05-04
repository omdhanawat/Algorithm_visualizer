from tracker.call_tracker import CallTracker

def get_obst_tracker():
    if not hasattr(get_obst_tracker, "tracker"):
        get_obst_tracker.tracker = CallTracker()
    return get_obst_tracker.tracker

def tracked_obst(keys, freq):
    n = len(keys)
    tracker = get_obst_tracker()
    tracker.reset()
    call_id = tracker.record_call("optimal_binary_search_tree", {"keys": keys, "freq": freq})

    # cost[i][j] = Optimal cost of BST with keys from index i to j
    cost = [[0 for _ in range(n)] for _ in range(n)]
    root = [[None for _ in range(n)] for _ in range(n)]

    def copy_matrix(matrix):
        return [["inf" if cell == float('inf') else cell for cell in row] for row in matrix]
    
    # Initialize for length 1
    for i in range(n):
        cost[i][i] = freq[i]
        root[i][i] = i
        tracker.record_phase(
            "init_base", 
            message=f"Base case: Single key '{keys[i]}' has cost {freq[i]}.", 
            i=i, j=i, 
            visual={"active_cells": [[i, i]]},
            state={"cost_matrix": copy_matrix(cost), "root_matrix": copy_matrix(root)}
        )

    # Lengths from 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float('inf')
            
            # Sum of frequencies in range [i, j]
            f_sum = sum(freq[i:j+1])
            
            tracker.record_phase(
                "range_start", 
                message=f"Calculating optimal cost for range [{i}, {j}] (Keys: {keys[i:j+1]}). Frequency sum: {f_sum}.", 
                i=i, j=j,
                state={"cost_matrix": copy_matrix(cost), "root_matrix": copy_matrix(root)}
            )

            for r in range(i, j + 1):
                # Cost when keys[r] is root
                # left_cost = cost[i][r-1] if r > i else 0
                # right_cost = cost[r+1][j] if r < j else 0
                c = (cost[i][r-1] if r > i else 0) + \
                    (cost[r+1][j] if r < j else 0) + f_sum
                
                prev_cost = cost[i][j]
                if c < cost[i][j]:
                    cost[i][j] = c
                    root[i][j] = r
                    tracker.record_phase(
                        "try_root", 
                        message=f"Trying '{keys[r]}' as root. Cost {c} < {prev_cost if prev_cost != float('inf') else '∞'}. New min!", 
                        i=i, j=j, k=r,
                        visual={
                            "active_cells": [[i, j]],
                            "dependency_cells": [[i, r-1] if r > i else None, [r+1, j] if r < j else None]
                        },
                        state={"cost_matrix": copy_matrix(cost), "root_matrix": copy_matrix(root)}
                    )
                else:
                    tracker.record_phase(
                        "try_root_no_update", 
                        message=f"Trying '{keys[r]}' as root. Cost {c} >= current min {cost[i][j]}. Skipping.", 
                        i=i, j=j, k=r,
                        state={"cost_matrix": copy_matrix(cost), "root_matrix": copy_matrix(root)}
                    )

    tree_nodes = []
    optimal_path = []

    def build_tree(i, j, parent_id=None):
        if i > j:
            return None
        r = root[i][j]
        if r is None:
            return None
        node_id = f"{i}-{j}-{r}"
        left_id = build_tree(i, r - 1, node_id)
        right_id = build_tree(r + 1, j, node_id)
        children = [child for child in [left_id, right_id] if child]
        tree_nodes.append({
            "id": node_id,
            "label": f"{keys[r]}",
            "children": children,
            "isResult": True,
            "value": cost[i][j],
            "parent": parent_id
        })
        optimal_path.append(keys[r])
        return node_id

    root_id = build_tree(0, n - 1)

    tracker.record_phase(
        "complete",
        message=f"OBST complete. Optimal search cost: {cost[0][n-1]}. Root selection path: {' -> '.join(map(str, optimal_path))}.",
        visual={"tree_nodes": tree_nodes, "active_node_id": root_id},
        state={
            "cost_matrix": copy_matrix(cost),
            "root_matrix": copy_matrix(root),
            "optimal_path": optimal_path,
            "optimal_cost": cost[0][n-1],
            "root_key": keys[root[0][n-1]]
        }
    )
    tracker.record_return(call_id, cost[0][n-1])
    return cost[0][n-1]
