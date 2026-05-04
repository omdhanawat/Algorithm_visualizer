import math
from tracker.call_tracker import CallTracker

def get_fw_tracker():
    if not hasattr(get_fw_tracker, "tracker"):
        get_fw_tracker.tracker = CallTracker()
    return get_fw_tracker.tracker

def tracked_floyd_warshall(V, edges):
    tracker = get_fw_tracker()
    tracker.reset()
    tracker.record_call("floyd_warshall", {"V": V, "edges": edges})

    dist = [[math.inf] * V for _ in range(V)]
    for i in range(V):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = w

    def snapshot():
        return [[(d if d != math.inf else "∞") for d in row] for row in dist]

    tracker.record_phase(
        "init",
        message=f"Initialized the distance matrix with {len(edges)} direct edges and 0s on the diagonal.",
        state={"table": snapshot()}
    )

    for k in range(V):
        tracker.record_phase(
            "intermediate_node_k", 
            message=f"Considering node {k} as an intermediate step to find shortcuts between all pairs.", 
            k=k,
            visual={"nodes": [k]}
        )
        for i in range(V):
            for j in range(V):
                old_val = dist[i][j]
                thru_k = dist[i][k] + dist[k][j] if (dist[i][k] != math.inf and dist[k][j] != math.inf) else math.inf
                
                tracker.record_phase(
                    "check_shortcut",
                    message=f"Checking if going through {k} ({i}→{k} + {k}→{j}) is shorter than direct {i}→{j}.",
                    i=i, j=j, k=k,
                    visual={
                        "active_cells": [[i, j]],
                        "dependency_cells": [[i, k], [k, j]],
                        "active_edges": [[i, k], [k, j]]
                    },
                    state={"table": snapshot()}
                )

                if thru_k < old_val:
                    dist[i][j] = thru_k
                    tracker.record_phase(
                        "relax_shortcut",
                        message=f"Shortcut found! New shortest distance {i}→{j} is {thru_k} (improved from {old_val}).",
                        i=i, j=j, k=k,
                        visual={
                            "active_cells": [[i, j]],
                            "dependency_cells": [[i, k], [k, j]],
                            "active_edges": [[i, k], [k, j]]
                        },
                        state={"table": snapshot()}
                    )

    tracker.record_phase("complete", message="All-pairs shortest paths found. The distance matrix is now finalized.", state={"table": snapshot()})
    tracker.record_return(0, snapshot())
    return dist
