import math
import random
from visualizer.combined_view import animate_execution

# --- Import Standardized Algorithms and Trackers ---
from algorithms.fibonacci import tracked_fib, get_fib_tracker
from algorithms.mergesort import tracked_mergesort, get_mergesort_tracker
from algorithms.quicksort import tracked_quicksort, get_quicksort_tracker
from algorithms.fibonacci_dp import tracked_fib_dp, get_fib_dp_tracker
from algorithms.nqueens import tracked_nqueens, get_nqueens_tracker
from algorithms.binary_search import tracked_binary_search, get_binary_search_tracker
from algorithms.knapsack import tracked_knapsack, get_knapsack_tracker
from algorithms.lis import tracked_lis, get_lis_tracker
from algorithms.lcs import tracked_lcs, get_lcs_tracker
from algorithms.obst import tracked_obst, get_obst_tracker
from algorithms.floyd_warshall import tracked_floyd_warshall, get_fw_tracker
from algorithms.dijkstra import tracked_dijkstra, get_dijkstra_tracker
from algorithms.kruskal import tracked_kruskal, get_kruskal_tracker
from algorithms.prim import tracked_prim, get_prim_tracker
from algorithms.fractional_knapsack import tracked_fractional_knapsack, get_fractional_knapsack_tracker
from algorithms.tsp import tracked_tsp, get_tsp_tracker

def run_fibonacci():
    n = int(input("\nEnter n for Recursive Fibonacci: "))
    tracker = get_fib_tracker()
    tracker.reset()
    tracked_fib(n)
    animate_execution(tracker.events, tracker)

def run_mergesort():
    arr = list(map(int, input("\nEnter numbers separated by space: ").split()))
    tracker = get_mergesort_tracker()
    tracker.reset()
    tracked_mergesort(arr)
    animate_execution(tracker.events, tracker)

def run_quicksort():
    arr = list(map(int, input("\nEnter numbers separated by space: ").split()))
    tracker = get_quicksort_tracker()
    tracker.reset()
    tracked_quicksort(arr)
    animate_execution(tracker.events, tracker)

def run_fib_dp():
    n = int(input("\nEnter n for DP Fibonacci: "))
    tracker = get_fib_dp_tracker()
    tracker.reset()
    tracked_fib_dp(n)
    animate_execution(tracker.events, tracker)

def run_nqueens():
    n = int(input("\nEnter board size for N-Queens: "))
    tracker = get_nqueens_tracker()
    tracker.reset()
    tracked_nqueens(n)
    animate_execution(tracker.events, tracker)

def run_binary_search():
    arr = sorted(list(map(int, input("\nEnter sorted array: ").split())))
    target = int(input("Enter target: "))
    tracker = get_binary_search_tracker()
    tracker.reset()
    tracked_binary_search(arr, target)
    animate_execution(tracker.events, tracker)

def run_knapsack():
    n = int(input("\nEnter number of items: "))
    weights = list(map(int, input("Enter weights: ").split()))
    values = list(map(int, input("Enter values: ").split()))
    W = int(input("Enter capacity: "))
    tracker = get_knapsack_tracker()
    tracker.reset()
    tracked_knapsack(weights, values, W)
    animate_execution(tracker.events, tracker)

def run_lis():
    arr = list(map(int, input("\nEnter array for LIS: ").split()))
    tracker = get_lis_tracker()
    tracker.reset()
    tracked_lis(arr)
    animate_execution(tracker.events, tracker)

def run_lcs():
    s1 = input("\nEnter first string: ")
    s2 = input("Enter second string: ")
    tracker = get_lcs_tracker()
    tracker.reset()
    tracked_lcs(s1, s2)
    animate_execution(tracker.events, tracker)

def run_obst():
    keys = list(map(int, input("\nEnter keys (space separated): ").split()))
    freq = list(map(int, input("Enter frequencies (space separated): ").split()))
    tracker = get_obst_tracker()
    tracker.reset()
    tracked_obst(keys, freq)
    animate_execution(tracker.events, tracker)

def run_fw():
    print("\n--- FLOYD-WARSHALL ALL-PAIRS SHORTEST PATH ---")
    V = int(input("Enter number of TOTAL vertices: "))
    print("Enter edges as 'u v w' (comma separated): ")
    edge_input = input("Example: 0 1 3, 1 2 2, 0 2 10\nEdges: ")
    edges = []
    if edge_input.strip():
        for e in edge_input.split(','):
            u, v, w = map(int, e.strip().split())
            edges.append((u, v, w))
    tracker = get_fw_tracker()
    tracker.reset()
    tracked_floyd_warshall(V, edges)
    animate_execution(tracker.events, tracker)

def run_dijkstra():
    print("\n--- DIJKSTRA SHORTEST PATH ---")
    V = int(input("Enter number of vertices: "))
    source = int(input(f"Enter source (0 to {V-1}): "))
    print("Enter edges as 'u v w' (comma separated): ")
    edge_input = input("Edges: ")
    edges = []
    if edge_input.strip():
        for e in edge_input.split(','):
            u, v, w = map(int, e.strip().split())
            edges.append((u, v, w))
    tracker = get_dijkstra_tracker()
    tracker.reset()
    tracked_dijkstra(V, edges, source)
    animate_execution(tracker.events, tracker)

def run_kruskal():
    print("\n--- KRUSKAL'S MST ---")
    V = int(input("Enter number of vertices: "))
    print("Enter edges as 'u v w' (comma separated): ")
    edge_input = input("Edges: ")
    edges = []
    if edge_input.strip():
        for e in edge_input.split(','):
            u, v, w = map(int, e.strip().split())
            edges.append((u, v, w))
    tracker = get_kruskal_tracker()
    tracker.reset()
    tracked_kruskal(V, edges)
    animate_execution(tracker.events, tracker)

def run_prim():
    print("\n--- PRIM'S MST ---")
    V = int(input("Enter number of vertices: "))
    source = int(input(f"Enter source (0 to {V-1}): "))
    print("Enter edges as 'u v w' (comma separated): ")
    edge_input = input("Edges: ")
    edges = []
    if edge_input.strip():
        for e in edge_input.split(','):
            u, v, w = map(int, e.strip().split())
            edges.append((u, v, w))
    tracker = get_prim_tracker()
    tracker.reset()
    tracked_prim(V, edges, source)
    animate_execution(tracker.events, tracker)

def run_fractional_knapsack():
    print("\n--- FRACTIONAL KNAPSACK ---")
    n = int(input("Enter number of items: "))
    weights = list(map(float, input("Weights: ").split()))
    values = list(map(float, input("Values: ").split()))
    capacity = float(input("Capacity: "))
    tracker = get_fractional_knapsack_tracker()
    tracker.reset()
    tracked_fractional_knapsack(weights, values, capacity)
    animate_execution(tracker.events, tracker)

def run_tsp():
    print("\n--- TRAVELLING SALESPERSON PROBLEM ---")
    n = int(input("Enter number of cities (4-6 recommended): "))
    coords = [(random.randint(50, 450), random.randint(50, 450)) for _ in range(n)]
    dist_matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j: continue
            dist_matrix[i][j] = math.sqrt((coords[i][0]-coords[j][0])**2 + (coords[i][1]-coords[j][1])**2)
    tracker = get_tsp_tracker()
    tracker.reset()
    tracked_tsp(n, dist_matrix, coords)
    animate_execution(tracker.events, tracker)

def main():
    while True:
        print("\n--- ALGORITHM VISUALIZER ---")
        print("1. Fibonacci (Rec)")
        print("2. Merge Sort")
        print("3. Quick Sort")
        print("4. Fibonacci (DP)")
        print("5. N-Queens")
        print("6. Binary Search")
        print("7. 0/1 Knapsack")
        print("8. LIS")
        print("9. LCS")
        print("10. Optimal BST")
        print("11. Floyd Warshall")
        print("12. Dijkstra")
        print("13. Kruskal")
        print("14. Prim")
        print("15. Fractional Knapsack")
        print("16. TSP")
        print("Q. Quit")
        
        choice = input("\nEnter choice: ").strip().lower()
        if choice == 'q': break
        
        actions = {
            "1": run_fibonacci, "2": run_mergesort, "3": run_quicksort,
            "4": run_fib_dp, "5": run_nqueens, "6": run_binary_search,
            "7": run_knapsack, "8": run_lis, "9": run_lcs, "10": run_obst,
            "11": run_fw, "12": run_dijkstra, "13": run_kruskal,
            "14": run_prim, "15": run_fractional_knapsack, "16": run_tsp
        }
        
        if choice in actions:
            try:
                actions[choice]()
            except Exception as e:
                print(f"\n[Error] Execution failed: {e}")
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
