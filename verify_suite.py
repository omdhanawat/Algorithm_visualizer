import math
import random
import os
import sys

# Add current path to sys.path
sys.path.append(os.getcwd())

from tracker.call_tracker import CallTracker
from algorithms.recurrence_info import ALGO_METADATA

def verify_all():
    print("--- ALGORITHM SUITE VERIFICATION ---")
    results = []
    
    # 1. Fibonacci (Recursive)
    try:
        from algorithms.fibonacci import tracked_fib, get_fib_tracker
        tracker = get_fib_tracker()
        tracker.reset()
        tracked_fib(5)
        results.append(("Fibonacci (Recursive)", len(tracker.events), "fib"))
    except Exception as e: results.append(("Fibonacci (Recursive)", f"ERROR: {e}", "fib"))

    # 2. Merge Sort
    try:
        from algorithms.mergesort import tracked_mergesort, get_mergesort_tracker
        tracker = get_mergesort_tracker()
        tracker.reset()
        tracked_mergesort([5, 2, 8, 1, 9])
        results.append(("Merge Sort", len(tracker.events), "mergeSort"))
    except Exception as e: results.append(("Merge Sort", f"ERROR: {e}", "mergeSort"))

    # 3. Quick Sort
    try:
        from algorithms.quicksort import tracked_quicksort, get_quicksort_tracker
        tracker = get_quicksort_tracker()
        tracker.reset()
        tracked_quicksort([5, 2, 8, 1, 9])
        results.append(("Quick Sort", len(tracker.events), "quickSort"))
    except Exception as e: results.append(("Quick Sort", f"ERROR: {e}", "quickSort"))

    # 4. Fibonacci (DP)
    try:
        from algorithms.fibonacci_dp import tracked_fib_dp, get_fib_dp_tracker
        tracker = get_fib_dp_tracker()
        tracker.reset()
        tracked_fib_dp(5)
        results.append(("Fibonacci (DP)", len(tracker.events), "fibDP"))
    except Exception as e: results.append(("Fibonacci (DP)", f"ERROR: {e}", "fibDP"))

    # 5. N Queens
    try:
        from algorithms.nqueens import tracked_nqueens, get_nqueens_tracker
        tracker = get_nqueens_tracker()
        tracker.reset()
        tracked_nqueens(4)
        results.append(("N Queens", len(tracker.events), "nQueens"))
    except Exception as e: results.append(("N Queens", f"ERROR: {e}", "nQueens"))

    # 6. Binary Search
    try:
        from algorithms.binary_search import tracked_binary_search, get_binary_search_tracker
        tracker = get_binary_search_tracker()
        tracker.reset()
        tracked_binary_search([1, 2, 3, 4, 10], 10)
        results.append(("Binary Search", len(tracker.events), "binarySearch"))
    except Exception as e: results.append(("Binary Search", f"ERROR: {e}", "binarySearch"))

    # 7. 0/1 Knapsack
    try:
        from algorithms.knapsack import tracked_knapsack, get_knapsack_tracker
        tracker = get_knapsack_tracker()
        tracker.reset()
        tracked_knapsack([2, 3, 4], [3, 4, 5], 5)
        results.append(("0/1 Knapsack", len(tracker.events), "knapsack"))
    except Exception as e: results.append(("0/1 Knapsack", f"ERROR: {e}", "knapsack"))

    # 8. LIS
    try:
        from algorithms.lis import tracked_lis, get_lis_tracker
        tracker = get_lis_tracker()
        tracker.reset()
        tracked_lis([10, 22, 9, 33, 21, 50, 41, 60])
        results.append(("LIS", len(tracker.events), "lis"))
    except Exception as e: results.append(("LIS", f"ERROR: {e}", "lis"))

    # 9. LCS
    try:
        from algorithms.lcs import tracked_lcs, get_lcs_tracker
        tracker = get_lcs_tracker()
        tracker.reset()
        tracked_lcs("ABCBDAB", "BDCABA")
        results.append(("LCS", len(tracker.events), "lcs"))
    except Exception as e: results.append(("LCS", f"ERROR: {e}", "lcs"))

    # 10. Optimal BST
    try:
        from algorithms.obst import tracked_obst, get_obst_tracker
        tracker = get_obst_tracker()
        tracker.reset()
        tracked_obst([10, 12, 20], [34, 8, 50])
        results.append(("Optimal BST", len(tracker.events), "obst"))
    except Exception as e: results.append(("Optimal BST", f"ERROR: {e}", "obst"))

    # 11. Floyd Warshall
    try:
        from algorithms.floyd_warshall import tracked_floyd_warshall, get_fw_tracker
        tracker = get_fw_tracker()
        tracker.reset()
        tracked_floyd_warshall(3, [[0, 1, 5], [1, 2, 3], [0, 2, 10]])
        results.append(("Floyd Warshall", len(tracker.events), "floyd_warshall"))
    except Exception as e: results.append(("Floyd Warshall", f"ERROR: {e}", "floyd_warshall"))

    # 12. Dijkstra
    try:
        from algorithms.dijkstra import tracked_dijkstra, get_dijkstra_tracker
        tracker = get_dijkstra_tracker()
        tracker.reset()
        tracked_dijkstra(3, [[0, 1, 5], [1, 2, 3], [0, 2, 10]])
        results.append(("Dijkstra", len(tracker.events), "dijkstra"))
    except Exception as e: results.append(("Dijkstra", f"ERROR: {e}", "dijkstra"))

    # 13. Kruskal
    try:
        from algorithms.kruskal import tracked_kruskal, get_kruskal_tracker
        tracker = get_kruskal_tracker()
        tracker.reset()
        tracked_kruskal(3, [[0, 1, 5], [1, 2, 3], [0, 2, 10]])
        results.append(("Kruskal", len(tracker.events), "kruskal"))
    except Exception as e: results.append(("Kruskal", f"ERROR: {e}", "kruskal"))

    # 14. Prim
    try:
        from algorithms.prim import tracked_prim, get_prim_tracker
        tracker = get_prim_tracker()
        tracker.reset()
        tracked_prim(3, [[0, 1, 5], [1, 2, 3], [0, 2, 10]])
        results.append(("Prim", len(tracker.events), "prim"))
    except Exception as e: results.append(("Prim", f"ERROR: {e}", "prim"))

    # 15. Fractional Knapsack
    try:
        from algorithms.fractional_knapsack import tracked_fractional_knapsack, get_fractional_knapsack_tracker
        tracker = get_fractional_knapsack_tracker()
        tracker.reset()
        tracked_fractional_knapsack([10, 20, 30], [60, 100, 120], 50)
        results.append(("Fractional Knapsack", len(tracker.events), "fractionalKnapsack"))
    except Exception as e: results.append(("Fractional Knapsack", f"ERROR: {e}", "fractionalKnapsack"))

    # 16. TSP
    try:
        from algorithms.tsp import tracked_tsp, get_tsp_tracker
        tracker = get_tsp_tracker()
        tracker.reset()
        tracked_tsp(3, [[0, 2, 9], [2, 0, 6], [9, 6, 0]])
        results.append(("TSP", len(tracker.events), "tsp"))
    except Exception as e: results.append(("TSP", f"ERROR: {e}", "tsp"))

    # Final Table Output
    print(f"{'Algorithm':<30} | {'Events':<10} | {'Metadata Check'}")
    print("-" * 65)
    for name, events, metadata_key in results:
        meta_exists = "YES" if metadata_key in ALGO_METADATA else "NO"
        print(f"{name:<30} | {events:<10} | {meta_exists}")

if __name__ == "__main__":
    verify_all()
