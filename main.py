from algorithms.fibonacci import tracked_fib, tracker as fib_tracker
from algorithms.mergesort import tracked_mergesort, tracker as merge_tracker
from visualizer.combined_view import animate_execution
from algorithms.quicksort import tracked_quicksort, tracker as quick_tracker
from algorithms.fibonacci_dp import tracked_fib_dp, tracker as dp_tracker
from algorithms.nqueens import solve_nqueens, tracker as nqueens_tracker
from algorithms.binary_search import tracked_binary_search, tracker as bs_tracker
from algorithms.knapsack import tracked_knapsack, tracker as knapsack_tracker
from algorithms.lis import tracked_lis, tracker as lis_tracker
from algorithms.lcs import tracked_lcs, tracker as lcs_tracker
from algorithms.obst import tracked_obst, tracker as obst_tracker

def run_obst():
    keys = list(map(int, input("Enter keys (space separated): ").split()))
    freq = list(map(int, input("Enter frequencies (space separated): ").split()))
    
    if len(keys) != len(freq):
        print("Error: number of keys and frequencies must match")
        return

    obst_tracker.reset()
    tracked_obst(keys, freq)
    animate_execution(obst_tracker.events, obst_tracker)

def run_lcs():
    s1 = input("Enter first string: ")
    s2 = input("Enter second string: ")

    lcs_tracker.reset()
    tracked_lcs(s1, s2)
    animate_execution(lcs_tracker.events, lcs_tracker)

def run_lis():
    arr = list(map(int, input("Enter array: ").split()))
    lis_tracker.reset()
    tracked_lis(arr)
    animate_execution(lis_tracker.events, lis_tracker)

def run_knapsack():

    n = int(input("Enter number of items: "))

    weights = list(map(int, input("Enter weights: ").split()))
    values = list(map(int, input("Enter values: ").split()))

    if len(weights) != n or len(values) != n:
        print("Error: number of weights/values must match n")
        return


    cap_input = input("Enter capacity: ").split()

    if len(cap_input) != 1:
        print("Error: capacity must be a single number")
        return

    W = int(cap_input[0])

    knapsack_tracker.reset()
    tracked_knapsack(weights, values, W)
    animate_execution(knapsack_tracker.events, knapsack_tracker)


def run_binary_search():
    arr = list(map(int, input("Enter sorted array: ").split()))
    target = int(input("Enter target: "))

    bs_tracker.reset()
    tracked_binary_search(arr, target)
    animate_execution(bs_tracker.events, bs_tracker)

def run_fib_dp():
    n = int(input("Enter n for DP Fibonacci: "))
    dp_tracker.reset()
    tracked_fib_dp(n)
    animate_execution(dp_tracker.events, dp_tracker)

def run_fibonacci():
    n = int(input("Enter n for Fibonacci: "))
    fib_tracker.reset()
    tracked_fib(n)
    animate_execution(fib_tracker.events, fib_tracker)

def run_mergesort():
    arr = list(map(int, input("Enter numbers separated by space: ").split()))
    merge_tracker.reset()
    tracked_mergesort(arr)
    animate_execution(merge_tracker.events, merge_tracker)

def run_quicksort():
    arr = list(map(int, input("Enter numbers separated by space: ").split()))
    quick_tracker.reset()
    tracked_quicksort(arr)
    animate_execution(quick_tracker.events, quick_tracker)

def run_nqueens():

    n = int(input("Enter board size : "))
    nqueens_tracker.reset()
    solve_nqueens(n, nqueens_tracker)
    animate_execution(nqueens_tracker.events, nqueens_tracker)

print("Choose Algorithm:")
print("1. Fibonacci")
print("2. Merge Sort")
print("3. Quick Sort")
print("4. Fibonacci (DP)")
print("5. N Queens (Backtracking)")
print("6. Binary Search")
print("7. 0/1 Knapsack (DP)")
print("8. Longest Increasing Subsequence (DP)")
print("9. Longest Common Subsequence (DP)")
print("10. Optimal Binary Search Tree (DP)")


choice = input("Enter choice: ")

if choice == "1":
    run_fibonacci()
elif choice == "2":
    run_mergesort()
elif choice == "3":
    run_quicksort()
elif choice == "4":
    run_fib_dp()
elif choice == "5":
    run_nqueens()
elif choice == "6":
    run_binary_search()
elif choice == "7":
    run_knapsack()
elif choice == "8":
    run_lis()
elif choice == "9":
    run_lcs()
elif choice == "10":
    run_obst()
else:
    print("Invalid choice")


