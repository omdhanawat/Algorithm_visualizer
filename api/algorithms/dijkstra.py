import math
import heapq
from tracker.call_tracker import CallTracker

def get_dijkstra_tracker():
    if not hasattr(get_dijkstra_tracker, "tracker"):
        get_dijkstra_tracker.tracker = CallTracker()
    return get_dijkstra_tracker.tracker

def tracked_dijkstra(V, edges, source=0):
    tracker = get_dijkstra_tracker()
    tracker.reset()
    tracker.record_call("dijkstra", {"V": V, "edges": edges, "source": source})

    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))

    dist = [math.inf] * V
    dist[source] = 0
    visited = [False] * V
    parent = [None] * V
    pq = [(0, source)]

    def snapshot():
        return [(d if d != math.inf else "∞") for d in dist]

    tracker.record_phase(
        "init",
        message=f"Initialized distances to ∞. Set source node {source} distance to 0.",
        visual={
            "nodes": list(range(V)),
            "edges": edges # [u, v, w]
        },
        state={"distances": snapshot()}
    )

    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]: continue
        
        visited[u] = True
        tracker.record_phase(
            "extract_min",
            message=f"Extracted node {u} with the smallest known distance ({d}) from the Priority Queue.",
            visual={"nodes": [u]},
            state={"distances": snapshot(), "visited": list(visited), "current_node": u}
        )

        for v, w in adj[u]:
            if visited[v]: continue
            
            old_dist = dist[v]
            new_dist = d + w
            
            tracker.record_phase(
                "check_edge",
                message=f"Checking edge {u}→{v} (weight {w}). Potential new path: {d} + {w} = {new_dist}.",
                i=u, j=v,
                visual={
                    "nodes": [u, v],
                    "active_edges": [[u, v]]
                },
                state={"distances": snapshot()}
            )

            if new_dist < old_dist:
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))
                
                tracker.record_phase(
                    "relax_edge",
                    message=f"Found a shorter path! {new_dist} < {old_dist if old_dist != math.inf else '∞'}. Updating node {v}.",
                    i=v,
                    visual={
                        "nodes": [v],
                        "active_edges": [[u, v]]
                    },
                    state={"distances": snapshot(), "parent": parent[v]}
                )

    tracker.record_phase("complete", message="All reachable nodes processed. Shortest paths from source have been found.", state={"distances": snapshot()})
    tracker.record_return(0, snapshot())
    return dist, parent
