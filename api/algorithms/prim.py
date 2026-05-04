import math
import heapq
from tracker.call_tracker import CallTracker

def get_prim_tracker():
    if not hasattr(get_prim_tracker, "tracker"):
        get_prim_tracker.tracker = CallTracker()
    return get_prim_tracker.tracker

def tracked_prim(V, edges, source=0):
    tracker = get_prim_tracker()
    tracker.reset()
    tracker.record_call("prim_mst", {"V": V, "edges": edges, "source": source})

    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    dist = [math.inf] * V
    dist[source] = 0
    visited = [False] * V
    parent = [None] * V
    pq = [(0, source)]
    mst_weight = 0

    def snapshot():
        return [(d if d != math.inf else "∞") for d in dist]

    tracker.record_phase(
        "init",
        message=f"Starting Prim's algorithm from node {source}. Distances to the MST cut set are initialized to ∞.",
        visual={
            "nodes": list(range(V)),
            "edges": edges # [u, v, w]
        },
        state={"distances": snapshot()}
    )

    while pq:
        w, u = heapq.heappop(pq)
        if visited[u]: continue
        
        visited[u] = True
        mst_weight += w
        
        # Determine the edge that brought node 'u' into the MST
        mst_edge = []
        if parent[u] is not None:
            mst_edge = [[parent[u], u]]

        tracker.record_phase(
            "pick_node_for_mst",
            message=f"Node {u} has the smallest cut distance ({w}). Adding it to the MST. Total MST weight: {mst_weight}.",
            visual={
                "nodes": [u],
                "active_edges": mst_edge
            },
            state={"distances": snapshot(), "visited": list(visited), "mst_weight": mst_weight}
        )

        for v, weight in adj[u]:
            if not visited[v]:
                tracker.record_phase(
                    "check_neighbors",
                    message=f"Checking neighbor {v} of node {u}. Edge weight {u}—{v} is {weight}. Current best edge to {v} is {dist[v] if dist[v] != math.inf else '∞'}.",
                    i=u, j=v,
                    visual={
                        "nodes": [u, v],
                        "active_edges": [[u, v]]
                    },
                    state={"distances": snapshot()}
                )

                if weight < dist[v]:
                    old_best = dist[v]
                    dist[v] = weight
                    parent[v] = u
                    heapq.heappush(pq, (weight, v))
                    
                    tracker.record_phase(
                        "update_best_edge",
                        message=f"Found a cheaper connection! {weight} < {old_best if old_best != math.inf else '∞'}. Node {v}'s best edge is now from {u}.",
                        i=v,
                        visual={
                            "nodes": [v],
                            "active_edges": [[u, v]]
                        },
                        state={"distances": snapshot(), "parent": list(parent)}
                    )

    tracker.record_phase("complete", message=f"Prim's algorithm finished. The Minimum Spanning Tree is formed with total weight {mst_weight}.", state={"mst_weight": mst_weight})
    tracker.record_return(mst_weight, snapshot())
    return mst_weight, parent
