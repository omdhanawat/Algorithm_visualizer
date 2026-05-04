from tracker.call_tracker import CallTracker

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j
                self.rank[root_j] += 1
            return True
        return False

def get_kruskal_tracker():
    if not hasattr(get_kruskal_tracker, "tracker"):
        get_kruskal_tracker.tracker = CallTracker()
    return get_kruskal_tracker.tracker

def tracked_kruskal(V, edges):
    tracker = get_kruskal_tracker()
    tracker.reset()
    call_id = tracker.record_call("kruskal_mst", {"V": V, "edges": edges})

    ds = DisjointSet(V)
    mst = []
    mst_weight = 0
    
    tracker.record_phase(
        "init",
        message=f"Initialized Disjoint Set. Each node starts in its own component.",
        visual={
            "nodes": list(range(V)),
            "edges": edges # [u, v, w]
        },
        state={"parent": ds.parent[:]}
    )

    sorted_edges = sorted(edges, key=lambda x: x[2])
    tracker.record_phase(
        "sort_edges",
        message="Sorted edges by weight (greedy choice). We will process the smallest edges first.",
        state={"sorted_edges": sorted_edges}
    )

    for u, v, w in sorted_edges:
        root_u = ds.find(u)
        root_v = ds.find(v)

        tracker.record_phase(
            "check_cycle",
            message=f"Checking edge {u}—{v} (weight {w}). Node {u}'s root is {root_u}, node {v}'s root is {root_v}.",
            i=u, j=v,
            visual={
                "nodes": [u, v],
                "active_edges": [[u, v]]
            },
            state={"parent": ds.parent[:], "mst": mst[:]}
        )

        if root_u != root_v:
            ds.union(root_u, root_v)
            mst.append((u, v, w))
            mst_weight += w
            tracker.record_phase(
                "accept_edge",
                message=f"Roots are different! No cycle detected. Adding edge {u}—{v} to the MST.",
                i=u, j=v,
                visual={
                    "nodes": [u, v],
                    "active_edges": [[u, v]]
                },
                state={"parent": ds.parent[:], "mst": mst[:], "mst_weight": mst_weight}
            )
        else:
            tracker.record_phase(
                "reject_edge",
                message=f"Roots are already the same ({root_u} == {root_v}). Adding this edge would create a cycle. Skipping.",
                i=u, j=v,
                visual={
                    "nodes": [u, v],
                    "active_edges": [[u, v]]
                },
                state={"parent": ds.parent[:], "mst": mst[:], "mst_weight": mst_weight}
            )

    tracker.record_phase("complete", message=f"Kruskal's algorithm complete. Found Minimum Spanning Tree with total weight {mst_weight}.", state={"mst": mst})
    tracker.record_return(call_id, {"mst": mst, "weight": mst_weight})
    return mst, mst_weight
