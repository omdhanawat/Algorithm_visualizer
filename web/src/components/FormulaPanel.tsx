import React from 'react';
import type { NormalizedEvent } from '../utils/eventAdapter';

interface FormulaDef {
  formula: string;
  highlight: (event: NormalizedEvent) => string | null;
}

const FORMULA_MAP: Record<string, FormulaDef> = {
  fibDP: {
    formula: "dp[i] = dp[i-1] + dp[i-2]",
    highlight: (event) => {
      if (event.phase === "compute") return "dp[i-1] + dp[i-2]";
      if (event.phase === "write") return "dp[i]";
      return null;
    }
  },
  knapsack: {
    formula: "dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])",
    highlight: (event) => {
      if (event.phase === "take") return "val[i] + dp[i-1][w-wt[i]]";
      if (event.phase === "skip") return "dp[i-1][w]";
      if (event.phase === "update") return "dp[i][w]";
      return null;
    }
  },
  dijkstra: {
    formula: "dist[v] = min(dist[v], dist[u] + weight(u, v))",
    highlight: (event) => {
      if (event.phase === "relax_edge") return "min(dist[v], dist[u] + weight(u, v))";
      if (event.phase === "check_edge") return "dist[u] + weight(u, v)";
      return null;
    }
  },
  floyd_warshall: {
    formula: "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])",
    highlight: (event) => {
      if (event.phase === "check_path") return "dist[i][k] + dist[k][j]";
      if (event.phase === "update_path") return "dist[i][j] = min(...)";
      return null;
    }
  },
  prim: {
    formula: "key[v] = min(key[v], weight(u, v))",
    highlight: (event) => {
      if (event.phase === "relax_edge") return "min(key[v], weight(u, v))";
      return null;
    }
  },
  kruskal: {
    formula: "if find(u) != find(v) then union(u, v)",
    highlight: (event) => {
      if (event.phase === "check_cycle") return "find(u) != find(v)";
      if (event.phase === "add_edge") return "union(u, v)";
      return null;
    }
  },
  lis: {
    formula: "dp[i] = max(dp[i], dp[j] + 1) for j < i if arr[j] < arr[i]",
    highlight: (event) => {
      if (event.phase === "check_j") return "arr[j] < arr[i]";
      if (event.phase === "update_dp") return "dp[j] + 1";
      return null;
    }
  },
  lcs: {
    formula: "dp[i][j] = if X[i]==Y[j] then dp[i-1][j-1]+1 else max(dp[i-1][j], dp[i][j-1])",
    highlight: (event) => {
      if (event.phase === "match") return "dp[i-1][j-1]+1";
      if (event.phase === "mismatch") return "max(dp[i-1][j], dp[i][j-1])";
      return null;
    }
  },
  binarySearch: {
    formula: "mid = (low + high) / 2",
    highlight: (event) => {
      if (event.phase === "calculate_mid") return "(low + high) / 2";
      if (event.phase === "found") return "mid";
      return null;
    }
  }
};

interface FormulaPanelProps {
  algoId: string;
  currentEvent: NormalizedEvent | null;
}

export const FormulaPanel: React.FC<FormulaPanelProps> = ({ algoId, currentEvent }) => {
  const def = FORMULA_MAP[algoId];
  if (!def) return null; // Or return a generic stub

  const activePart = currentEvent ? def.highlight(currentEvent) : null;
  
  // Basic substring replacement to render active part
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
