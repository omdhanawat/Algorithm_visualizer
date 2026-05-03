import React from 'react';
import type { NormalizedEvent } from '../utils/eventAdapter';

interface FormulaDef {
  formula: string;
  highlight: (event: NormalizedEvent) => string | null;
}

/**
 * FORMULA_MAP: All 16 algorithms.
 * Phase names MUST exactly match what the Python backend emits in tracker.record_phase().
 */
const FORMULA_MAP: Record<string, FormulaDef> = {

  // --- Role 3: Sequences & Searching ---

  fib: {
    formula: "F(n) = F(n-1) + F(n-2)",
    highlight: (event) => {
      if (event.phase === "call") return "F(n-1) + F(n-2)";
      if (event.phase === "return") return "F(n)";
      return null;
    }
  },

  mergeSort: {
    formula: "T(n) = 2T(n/2) + O(n)",
    highlight: (event) => {
      if (event.phase === "divide") return "2T(n/2)";
      if (event.phase === "merge_step") return "O(n)";
      if (event.phase === "merge_complete") return "T(n)";
      return null;
    }
  },

  quickSort: {
    formula: "T(n) = T(k) + T(n-k-1) + O(n)",
    highlight: (event) => {
      if (event.phase === "pivot") return "T(k) + T(n-k-1)";
      if (event.phase === "partition") return "O(n)";
      if (event.phase === "swap") return "T(n-k-1)";
      return null;
    }
  },

  binarySearch: {
    formula: "mid = (low + high) // 2",
    highlight: (event) => {
      if (event.phase === "mid") return "(low + high) // 2";
      if (event.phase === "found") return "mid";
      if (event.phase === "left") return "high = mid - 1";
      if (event.phase === "right") return "low = mid + 1";
      return null;
    }
  },

  nQueens: {
    formula: "Place Queen at (row, col) if no row/col/diagonal conflict",
    highlight: (event) => {
      if (event.phase === "check") return "no row/col/diagonal conflict";
      if (event.phase === "placed") return "Place Queen at (row, col)";
      if (event.phase === "backtrack") return "backtrack";
      return null;
    }
  },

  fractionalKnapsack: {
    formula: "ratio[i] = value[i] / weight[i] → Take highest ratio first",
    highlight: (event) => {
      if (event.phase === "greedy_sorting") return "value[i] / weight[i]";
      if (event.phase === "pick_full_item") return "Take highest ratio first";
      if (event.phase === "pick_fractional_item") return "Take highest ratio first";
      return null;
    }
  },

  // --- Role 2: Dynamic Programming ---

  fibDP: {
    formula: "dp[i] = dp[i-1] + dp[i-2]",
    highlight: (event) => {
      if (event.phase === "compute") return "dp[i-1] + dp[i-2]";
      if (event.phase === "complete") return "dp[i]";
      return null;
    }
  },

  knapsack: {
    formula: "dp[i][w] = max(val[i] + dp[i-1][w-wt[i]], dp[i-1][w])",
    highlight: (event) => {
      if (event.phase === "update_cell") return "max(val[i] + dp[i-1][w-wt[i]], dp[i-1][w])";
      if (event.phase === "complete") return "dp[i][w]";
      return null;
    }
  },

  lis: {
    formula: "dp[i] = 1 + max(dp[j]) for all j < i where arr[j] < arr[i]",
    highlight: (event) => {
      if (event.phase === "check_extension") return "arr[j] < arr[i]";
      if (event.phase === "update_lis") return "dp[j] + 1";
      if (event.phase === "complete") return "max(dp[i])";
      return null;
    }
  },

  lcs: {
    formula: "dp[i][j] = dp[i-1][j-1]+1 if match, else max(dp[i-1][j], dp[i][j-1])",
    highlight: (event) => {
      if (event.phase === "update_cell") return "dp[i-1][j-1]+1";
      if (event.phase === "backtrack_match") return "dp[i-1][j-1]+1";
      if (event.phase === "backtrack_move") return "max(dp[i-1][j], dp[i][j-1])";
      return null;
    }
  },

  obst: {
    formula: "cost[i][j] = min(cost[i][r-1] + cost[r+1][j]) + freq_sum[i..j]",
    highlight: (event) => {
      if (event.phase === "range_start") return "freq_sum[i..j]";
      if (event.phase === "eval_root") return "cost[i][r-1] + cost[r+1][j]";
      if (event.phase === "update_root") return "min(cost[i][r-1] + cost[r+1][j])";
      if (event.phase === "complete") return "cost[i][j]";
      return null;
    }
  },

  // --- Role 1: Graphs ---

  floyd_warshall: {
    formula: "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])",
    highlight: (event) => {
      if (event.phase === "check_shortcut") return "dist[i][k] + dist[k][j]";
      if (event.phase === "relax_shortcut") return "min(dist[i][j], dist[i][k] + dist[k][j])";
      if (event.phase === "complete") return "dist[i][j]";
      return null;
    }
  },

  dijkstra: {
    formula: "dist[v] = min(dist[v], dist[u] + weight(u, v))",
    highlight: (event) => {
      if (event.phase === "check_edge") return "dist[u] + weight(u, v)";
      if (event.phase === "relax_edge") return "min(dist[v], dist[u] + weight(u, v))";
      if (event.phase === "extract_min") return "dist[u]";
      return null;
    }
  },

  kruskal: {
    formula: "if find(u) != find(v) → union(u, v) and add edge",
    highlight: (event) => {
      if (event.phase === "sort_edges") return "sort by weight";
      if (event.phase === "check_cycle") return "find(u) != find(v)";
      if (event.phase === "accept_edge") return "union(u, v) and add edge";
      if (event.phase === "reject_edge") return "find(u) == find(v) → cycle!";
      return null;
    }
  },

  prim: {
    formula: "key[v] = min(key[v], weight(u, v)) for unvisited v",
    highlight: (event) => {
      if (event.phase === "pick_node_for_mst") return "min key among unvisited";
      if (event.phase === "check_neighbors") return "weight(u, v)";
      if (event.phase === "update_best_edge") return "key[v] = min(key[v], weight(u, v))";
      return null;
    }
  },

  tsp: {
    formula: "min cost(P) for all Hamiltonian Paths P starting at 0",
    highlight: (event) => {
      if (event.phase === "visit") return "cost(P)";
      if (event.phase === "prune") return "prune: partial cost > best";
      if (event.phase === "new_best") return "min cost(P)";
      if (event.phase === "backtrack") return "backtrack";
      return null;
    }
  },
};

interface FormulaPanelProps {
  algoId: string;
  currentEvent: NormalizedEvent | null;
}

export const FormulaPanel: React.FC<FormulaPanelProps> = ({ algoId, currentEvent }) => {
  const def = FORMULA_MAP[algoId];
  if (!def) return null;

  const activePart = currentEvent ? def.highlight(currentEvent) : null;
  
  const renderFormula = () => {
    if (!activePart) return <span className="font-mono text-slate-300">{def.formula}</span>;
    
    const parts = def.formula.split(activePart);
    if (parts.length === 1) return <span className="font-mono text-slate-300">{def.formula}</span>;

    return (
      <span className="font-mono text-slate-300">
        {parts.map((part, i) => (
          <React.Fragment key={i}>
            {part}
            {i < parts.length - 1 && (
              <span className="text-yellow-400 font-bold bg-yellow-400/10 px-1 rounded mx-0.5">
                {activePart}
              </span>
            )}
          </React.Fragment>
        ))}
      </span>
    );
  };

  return (
    <div className="bg-slate-900 rounded-2xl p-4 border border-slate-800 shadow-inner flex flex-col gap-2">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">Live Formula</span>
        <div className="flex-1 h-px bg-slate-800" />
      </div>
      <div className="overflow-x-auto custom-scrollbar text-sm py-1">
        {renderFormula()}
      </div>
    </div>
  );
};
