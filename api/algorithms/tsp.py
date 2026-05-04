from tracker.call_tracker import CallTracker
import math


def get_tsp_tracker():
    if not hasattr(get_tsp_tracker, "tracker"):
        get_tsp_tracker.tracker = CallTracker()
    return get_tsp_tracker.tracker


def tracked_tsp(n, dist_matrix, coords=None):
    tracker = get_tsp_tracker()
    tracker.reset()

    if not dist_matrix or not isinstance(dist_matrix, list):
        raise ValueError("TSP needs a square distance matrix.")

    matrix_size = len(dist_matrix)
    if matrix_size == 0 or any(len(row) != matrix_size for row in dist_matrix):
        raise ValueError("TSP distance matrix must be square, with the same number of rows and columns.")

    if n != matrix_size:
        n = matrix_size

    tracker.record_call("tsp_backtracking", {"n": n, "dist_matrix": dist_matrix, "coords": coords})

    best_path = []
    best_cost = math.inf

    def display_cost(value):
        return "inf" if value == math.inf else value

    def path_edges(path):
        return [[path[i], path[i + 1]] for i in range(len(path) - 1)]

    tracker.record_phase(
        "init",
        message=f"Starting TSP for {n} cities. Search begins at city 0. We try complete tours and keep the cheapest loop.",
        visual={
            "nodes": list(range(n)),
            "edges": [[i, j, dist_matrix[i][j]] for i in range(n) for j in range(n) if i != j]
        },
        state={
            "dist_matrix": dist_matrix,
            "current_path": [0],
            "current_cost": 0,
            "best_path": [],
            "best_cost": "inf"
        }
    )

    def solve(curr_node, visited_mask, current_path, current_cost):
        nonlocal best_cost, best_path

        if current_cost >= best_cost:
            tracker.record_phase(
                "prune_branch",
                message=f"Pruning this branch because current cost {current_cost} is already at least the best cost {best_cost}.",
                i=curr_node,
                visual={"nodes": [curr_node], "active_edges": path_edges(current_path)},
                state={
                    "dist_matrix": dist_matrix,
                    "current_path": list(current_path),
                    "current_cost": current_cost,
                    "best_path": list(best_path),
                    "best_cost": display_cost(best_cost)
                }
            )
            return

        if visited_mask == (1 << n) - 1:
            return_cost = dist_matrix[curr_node][0]
            total_cost = current_cost + return_cost
            final_path = current_path + [0]

            tracker.record_phase(
                "return_to_base",
                message=f"All cities are visited. Closing the loop from city {curr_node} back to city 0 gives tour cost {total_cost}.",
                i=curr_node,
                j=0,
                visual={"nodes": [0], "active_edges": [[curr_node, 0]]},
                state={
                    "dist_matrix": dist_matrix,
                    "current_path": final_path,
                    "current_cost": total_cost,
                    "best_path": list(best_path),
                    "best_cost": display_cost(best_cost)
                }
            )

            if total_cost < best_cost:
                old_best = best_cost
                best_cost = total_cost
                best_path = list(final_path)
                tracker.record_phase(
                    "update_best_tour",
                    message=f"New best tour found. Cost improves from {display_cost(old_best)} to {best_cost}.",
                    visual={"nodes": list(best_path), "active_edges": path_edges(best_path)},
                    state={
                        "dist_matrix": dist_matrix,
                        "current_path": list(final_path),
                        "current_cost": total_cost,
                        "best_path": list(best_path),
                        "best_cost": best_cost
                    }
                )
            return

        for next_node in range(n):
            if not (visited_mask & (1 << next_node)):
                edge_cost = dist_matrix[curr_node][next_node]
                next_path = current_path + [next_node]
                next_cost = current_cost + edge_cost

                tracker.record_phase(
                    "visit_city",
                    message=f"Trying city {next_node} after city {curr_node}. Edge cost {edge_cost}; path cost becomes {next_cost}.",
                    i=curr_node,
                    j=next_node,
                    visual={"nodes": [next_node], "active_edges": [[curr_node, next_node]]},
                    state={
                        "dist_matrix": dist_matrix,
                        "current_path": next_path,
                        "current_cost": next_cost,
                        "best_path": list(best_path),
                        "best_cost": display_cost(best_cost)
                    }
                )

                solve(next_node, visited_mask | (1 << next_node), next_path, next_cost)

                tracker.record_phase(
                    "backtrack",
                    message=f"Backtracking from city {next_node} to city {curr_node}. The search now tries another unvisited city.",
                    i=curr_node,
                    j=next_node,
                    visual={"nodes": [curr_node], "active_edges": [[next_node, curr_node]]},
                    state={
                        "dist_matrix": dist_matrix,
                        "current_path": list(current_path),
                        "current_cost": current_cost,
                        "best_path": list(best_path),
                        "best_cost": display_cost(best_cost)
                    }
                )

    solve(0, 1, [0], 0)

    tracker.record_phase(
        "complete",
        message=f"TSP exploration finished. Best tour: {' -> '.join(map(str, best_path))}. Total cost: {best_cost}.",
        visual={"nodes": list(best_path), "active_edges": path_edges(best_path)},
        state={
            "dist_matrix": dist_matrix,
            "current_path": list(best_path),
            "current_cost": best_cost,
            "best_path": list(best_path),
            "best_cost": best_cost
        }
    )
    tracker.record_return(0, best_cost)
    return best_cost, best_path
