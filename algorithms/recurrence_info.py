RECURRENCES = {
    "fib": "T(n) = T(n-1) + T(n-2) + O(1)",
    "mergeSort": "T(n) = 2T(n/2) + O(n)",
    "quickSort": "Best: T(n)=2T(n/2)+O(n), Worst: T(n)=T(n-1)+O(n)",
    "fibDP": "DP: T(n)=T(n-1)+O(1) → O(n)",
}

DP_FORMULAS = {
    "fibDP": "dp[n] = dp[n-1] + dp[n-2]",
    
    "lis": (
        "dp[i] = 1 + max(dp[j]) for all j < i where arr[j] < arr[i]\n"
        "else dp[i] = 1"
    ),

    "knapsack": (
        "dp[i][w] = max(\n"
        "  value[i] + dp[i-1][w-weight[i]],\n"
        "  dp[i-1][w]\n"
        ")"
    ),

    "lcs": (
        "if s1[i] == s2[j]: dp[i][j] = 1 + dp[i-1][j-1]\n"
        "else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])"
    ),

    "obst": (
        "cost[i][j] = min_{i<=k<=j} (cost[i][k-1] + cost[k+1][j]) + W[i][j]\n"
        "W[i][j] = sum(freq[i...j])"
    )
}