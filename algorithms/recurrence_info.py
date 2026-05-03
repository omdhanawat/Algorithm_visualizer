# Algorithm Metadata for Visualizer

ALGO_METADATA = {
    "fib": {
        "name": "Fibonacci (Recursive)",
        "complexity": "Time: O(2^n), Space: O(n)",
        "formula": "F(n) = F(n-1) + F(n-2)",
        "strategy": "Divide & Conquer (Naive Recursion)",
        "phases": {
            "default": "Computing F(n) by branching into sub-tasks.",
            "returning": "Returning computed result to caller."
        }
    },
    "mergeSort": {
        "name": "Merge Sort",
        "complexity": "Time: O(n log n), Space: O(n)",
        "formula": "T(n) = 2T(n/2) + O(n)",
        "strategy": "Divide & Conquer",
        "phases": {
            "split": "Splitting the current array into two halves.",
            "merge": "Merging two sorted subarrays into one.",
            "compare": "Comparing elements from both halves.",
            "copy": "Copying the smallest element into the merged array."
        }
    },
    "quickSort": {
        "name": "Quick Sort",
        "complexity": "Time: O(n log n) [Avg], Space: O(log n)",
        "formula": "T(n) = T(k) + T(n-k-1) + O(n)",
        "strategy": "Divide & Conquer (Partitioning)",
        "phases": {
            "pivot": "Selecting an element as the 'Pivot'.",
            "partition": "Rearranging: < Pivot on left, > Pivot on right.",
            "swap": "Swapping elements to maintain partitioning."
        }
    },
    "fibDP": {
        "name": "Fibonacci (Dynamic Programming)",
        "complexity": "Time: O(n), Space: O(n)",
        "formula": "dp[i] = dp[i-1] + dp[i-2]",
        "strategy": "Dynamic Programming (Tabulation)",
        "phases": {
            "compute": "Calculating F(i) using previous cached results.",
            "complete": "Calculation finished! F(n) is the last stored value."
        }
    },
    "binarySearch": {
        "name": "Binary Search",
        "complexity": "Time: O(log n), Space: O(1)",
        "formula": "mid = (low + high) // 2",
        "strategy": "Divide & Conquer (Sorted Search)",
        "phases": {
            "mid": "Calculating middle index and checking its value.",
            "found": "Target found! Returning the matching index.",
            "left": "Target is smaller; discarding the right half.",
            "right": "Target is larger; discarding the left half."
        }
    },
    "nQueens": {
        "name": "N-Queens",
        "complexity": "Time: O(N!), Space: O(N)",
        "formula": "Place Q(row,col) where no Q shares row, col, or diagonal",
        "strategy": "Backtracking",
        "phases": {
            "check": "Checking if placing Queen at current cell is safe.",
            "placed": "Position is safe! Placing Queen and moving to next row.",
            "backtrack": "Conflict detected or no solution found. Removing Queen."
        }
    },
    "knapsack": {
        "name": "0/1 Knapsack",
        "complexity": "Time: O(n*W), Space: O(n*W)",
        "formula": "dp[i][w] = max(val[i] + dp[i-1][w-wt[i]], dp[i-1][w])",
        "strategy": "Dynamic Programming",
        "phases": {
            "compare": "Choosing: Include item vs. Exclude item.",
            "include": "Item fits! Maximum value updated by including it.",
            "exclude": "Item too heavy or suboptimal; skipping it.",
            "complete": "Tabulation complete. Backtracking to find selection."
        }
    },
    "lis": {
        "name": "Longest Increasing Subsequence",
        "complexity": "Time: O(n^2), Space: O(n)",
        "formula": "dp[i] = 1 + max(dp[j] for j < i if arr[j] < arr[i])",
        "strategy": "Dynamic Programming",
        "phases": {
            "compare": "Checking if arr[i] can extend subsequence ending at j.",
            "update": "New longest record found for current element.",
            "complete": "LIS calculation finished for all indices."
        }
    },
    "lcs": {
        "name": "Longest Common Subsequence",
        "complexity": "Time: O(m*n), Space: O(m*n)",
        "formula": "Match: 1+dp[i-1][j-1], Mismatch: max(top, left)",
        "strategy": "Dynamic Programming",
        "phases": {
            "match": "Characters match! Adding 1 to diagonal length.",
            "mismatch": "Characters differ. Inheriting best value from neighbors.",
            "complete": "Table full. LCS string found in bottom-right."
        }
    },
    "obst": {
        "name": "Optimal Binary Search Tree",
        "complexity": "Time: O(n^3), Space: O(n^2)",
        "formula": "c[i][j] = min(c[i][k-1] + c[k+1][j]) + sum(freq[i...j])",
        "strategy": "Dynamic Programming",
        "phases": {
            "cost": "Evaluating subtree root candidate 'k' for range [i, j].",
            "update": "Found a better root candidate for current subtree.",
            "complete": "Tree cost minimized and structure optimized."
        }
    },
    "floyd_warshall": {
        "name": "Floyd-Warshall",
        "complexity": "Time: O(V^3), Space: O(V^2)",
        "formula": "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])",
        "strategy": "Dynamic Programming (All-Pairs Shortest Path)",
        "phases": {
            "update": "Checking if path through node 'k' is a shortcut.",
            "found": "New shortest path found via intermediate node!",
            "complete": "All shortest paths between all pairs computed."
        }
    },
    "dijkstra": {
        "name": "Dijkstra's Algorithm",
        "complexity": "Time: O(E log V), Space: O(V)",
        "formula": "dist[v] = min(dist[v], dist[u] + weight(u, v))",
        "strategy": "Greedy (Single-Source Shortest Path)",
        "phases": {
            "extract": "Picking vertex with minimum distance from Priority Queue.",
            "relax": "Checking all neighbors: Can we find a shorter path?",
            "updated": "Distance to neighbor vertex updated successfully.",
            "complete": "Shortest paths from source determined."
        }
    },
    "kruskal": {
        "name": "Kruskal's MST",
        "complexity": "Time: O(E log E), Space: O(E)",
        "formula": "if find(u) != find(v) → union(u,v), add edge (sorted by weight)",
        "strategy": "Greedy (Minimum Spanning Tree)",
        "phases": {
            "sort": "Sorting all edges by weight in ascending order.",
            "check": "Checking if adding current edge forms a cycle.",
            "add": "No cycle formed! Adding edge to the Spanning Tree.",
            "complete": "Minimum Spanning Tree construction complete."
        }
    },
    "prim": {
        "name": "Prim's MST",
        "complexity": "Time: O(V^2) or O(E log V), Space: O(V)",
        "formula": "key[v] = min(key[v], weight(u,v)) for all unvisited v",
        "strategy": "Greedy (Minimum Spanning Tree)",
        "phases": {
            "pick": "Searching for smallest edge connecting MST to external nodes.",
            "add": "Smallest edge found! Adding new vertex to MST.",
            "update": "Updating keys of neighboring vertices.",
            "complete": "Greedy MST construction finished."
        }
    },
    "fractionalKnapsack": {
        "name": "Fractional Knapsack",
        "complexity": "Time: O(n log n), Space: O(n)",
        "formula": "ratio[i] = v[i]/w[i]; greedily take highest ratio items first",
        "strategy": "Greedy",
        "phases": {
            "sort": "Sorting items by their Value/Weight ratio (descending).",
            "check": "Evaluating the next best item by ratio.",
            "pick": "Item fits! Adding the entire item to the knapsack.",
            "pick_fraction": "Item partially fits! Taking a fraction to fill capacity.",
            "complete": "Knapsack filled with maximum possible greedy value."
        }
    },
    "tsp": {
        "name": "Traveling Salesperson Problem",
        "complexity": "Time: O(n!), Space: O(n)",
        "formula": "min Σ dist(path[i], path[i+1]) over all Hamiltonian circuits",
        "strategy": "Backtracking (Branch and Bound)",
        "phases": {
            "init": "Initializing cities and distance matrix.",
            "visit": "Traveling to next city. Current path cost updated.",
            "prune": "Pruning: Current partial path already exceeds best found cost.",
            "backtrack": "Dead end or optimal found. Backtracking to explore other paths.",
            "new_best": "New shorter circuit found! Updating global optimum.",
            "complete_path": "Hamiltonian Circuit completed! Evaluating total cost.",
            "final": "Optimal tour found. Visualization complete."
        }
    }
}

RECURRENCES = {k: v["complexity"] for k, v in ALGO_METADATA.items()}
DP_FORMULAS = {k: v["formula"] for k, v in ALGO_METADATA.items()}