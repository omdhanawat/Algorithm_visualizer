from algorithms.fibonacci import tracked_fib, tracker as fib_tracker
from algorithms.mergesort import tracked_mergesort, tracker as merge_tracker
from visualizer.combined_view import animate_execution
from algorithms.quicksort import tracked_quicksort, tracker as quick_tracker
from algorithms.fibonacci_dp import tracked_fib_dp, tracker as dp_tracker
from algorithms.nqueens import solve_nqueens, tracker as nqueens_tracker

def run_fib_dp():
    n = int(input("Enter n for DP Fibonacci: "))
    dp_tracker.reset()
    tracked_fib_dp(n)
    animate_execution(dp_tracker.events)

def run_fibonacci():
    n = int(input("Enter n for Fibonacci: "))
    fib_tracker.reset()
    tracked_fib(n)
    animate_execution(fib_tracker.events)

def run_mergesort():
    arr = list(map(int, input("Enter numbers separated by space: ").split()))
    merge_tracker.reset()
    tracked_mergesort(arr)
    animate_execution(merge_tracker.events)

def run_quicksort():
    arr = list(map(int, input("Enter numbers separated by space: ").split()))
    quick_tracker.reset()
    tracked_quicksort(arr)
    animate_execution(quick_tracker.events)

def run_nqueens():

    n = int(input("Enter board size : "))
    nqueens_tracker.reset()
    solve_nqueens(n, nqueens_tracker)
    animate_execution(nqueens_tracker.events)

print("Choose Algorithm:")
print("1. Fibonacci")
print("2. Merge Sort")
print("3. Quick Sort")
print("4. Fibonacci (Dynamic Programming)")
print("5. N Queens (Backtracking)")


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
else:
    print("Invalid choice")


