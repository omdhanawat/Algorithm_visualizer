import React, { useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity, SkipBack, SkipForward, Play, Pause, PanelLeftOpen, SlidersHorizontal } from 'lucide-react';

import { usePlayback } from '../hooks/usePlayback';
import type { AlgoEvent } from '../hooks/usePlayback';

import { MemoizedTableView } from './TableView';
import { MemoizedGraphView } from './GraphView';
import { MemoizedTreeView } from './TreeView';
import { MemoizedArrayView } from './ArrayView';
import { MemoizedGridView } from './GridView';
import { MemoizedFractionalKnapsackView } from './FractionalKnapsackView';

import { MemoizedEducationPanel } from './EducationPanel';
import { FormulaPanel } from './FormulaPanel';
import { ErrorBoundary } from './ErrorBoundary';

const GRAPH_ALGOS = new Set(['dijkstra', 'prim', 'kruskal', 'floyd_warshall', 'tsp']);
const ARRAY_ALGOS = new Set(['binarySearch']);
const TABLE_ALGOS = new Set(['fibDP', 'knapsack', 'fractionalKnapsack', 'lis', 'lcs', 'obst', 'floyd_warshall', 'dijkstra', 'prim']);
const RECURSION_TREE_ALGOS = new Set(['fib', 'mergeSort', 'quickSort', 'binarySearch', 'nQueens']);
const GRAPH_TABLE_ALGOS = new Set(['dijkstra', 'prim', 'floyd_warshall']);
const DP_TREE_ALGOS = new Set(['obst']);

interface VisualizerStageProps {
  events: AlgoEvent[];
  algoId: string;
  algoName: string;
  onOpenConfig: () => void;
  onOpenLibrary: () => void;
}

export const VisualizerStage: React.FC<VisualizerStageProps> = ({ events, algoId, algoName, onOpenConfig, onOpenLibrary }) => {
  const {
    events: normalizedEvents,
    currentEvent,
    index,
    total,
    isPlaying,
    setIsPlaying,
    next,
    prev,
    jumpTo,
    speed,
    setSpeed
  } = usePlayback(events);

  // [Memoized graph/tree synthesis logic omitted for length - see previous view_file for full code]
  // Note: I will keep the synthesis logic identical to the previous version but wrap it in the new layout.

  // ... (Keeping the synthesis logic as seen in the previous view_file) ...
  // [I will use the exact logic from lines 40-119 in the final write but condense here for the tool call]

  const baseVisual = useMemo(() => {
    return normalizedEvents.find(e => e.visuals?.nodes || e.visuals?.edges)?.visuals || {};
  }, [normalizedEvents]);

  const firstCallArgs = useMemo(() => {
    return normalizedEvents.find(e => e.raw?.args)?.raw?.args || {};
  }, [normalizedEvents]);

  const cumulativeState = useMemo(() => {
    const state: Record<string, any> = {};
    for (let i = 0; i <= index; i++) {
      const eventState = normalizedEvents[i]?.state;
      if (eventState && typeof eventState === 'object') {
        Object.assign(state, eventState);
      }
    }
    return state;
  }, [normalizedEvents, index]);

  const graphBase = useMemo(() => {
    if (algoId === 'tsp') {
      const matrix = firstCallArgs.dist_matrix || cumulativeState.dist_matrix || [];
      const n = firstCallArgs.n || matrix.length || 0;
      const nodes = Array.from({ length: n }, (_, i) => i);
      const edges = baseVisual.edges || [];
      return {
        nodes,
        edges: edges.length > 0 ? edges : matrix.flatMap((row: any[], i: number) =>
          (row || []).map((weight, j) => i !== j ? [i, j, weight] : null).filter(Boolean)
        )
      };
    }

    const V = firstCallArgs.V || cumulativeState.V;
    const argEdges = firstCallArgs.edges || baseVisual.edges || [];
    const nodesFromEdges = Array.from(new Set(
      (argEdges || []).flatMap((edge: any) => Array.isArray(edge) ? [edge[0], edge[1]] : [edge.source, edge.target])
    )).filter((node) => node !== undefined && node !== null);
    const nodes = baseVisual.nodes || (typeof V === 'number' ? Array.from({ length: V }, (_, i) => i) : nodesFromEdges);
    return { nodes, edges: argEdges };
  }, [algoId, firstCallArgs, cumulativeState, baseVisual]);

  const baseNodes = graphBase.nodes as any[];
  const baseEdges = graphBase.edges as any[];

  const tableModel = useMemo(() => {
    if (algoId === 'fractionalKnapsack') {
      const items = cumulativeState.items || (
        firstCallArgs.weights && firstCallArgs.values
          ? firstCallArgs.weights.map((w: number, id: number) => ({
              id,
              w,
              v: firstCallArgs.values[id],
              ratio: Number((firstCallArgs.values[id] / w).toFixed(2))
            }))
          : []
      );
      const selected = cumulativeState.selected || [];
      const selectedById = new Map(selected.map((item: any) => [item.id, item]));
      const rows = items.map((item: any) => {
        const picked = selectedById.get(item.id) as any;
        return [
          item.id,
          item.w,
          item.v,
          item.ratio,
          picked ? `${Math.round((picked.fraction || 0) * 100)}%` : '0%'
        ];
      });
      return {
        data: rows,
        labels: { rows: rows.map((row: any[]) => `Item ${row[0]}`), cols: ['ID', 'Weight', 'Value', 'Ratio', 'Taken'] }
      };
    }

    if (algoId === 'lis') {
      const lis = cumulativeState.lis || currentEvent?.state?.lis || firstCallArgs.arr;
      return {
        data: lis ? [lis] : null,
        labels: lis ? { rows: ['LIS'], cols: lis.map((_: any, i: number) => String(i)) } : undefined
      };
    }

    const table = cumulativeState.dp || cumulativeState.table || cumulativeState.cost_matrix || cumulativeState.distances || currentEvent?.state?.arr;
    if (Array.isArray(table) && !Array.isArray(table[0]) && (algoId === 'dijkstra' || algoId === 'prim')) {
      return {
        data: [table],
        labels: { rows: [algoId === 'prim' ? 'Key' : 'Dist'], cols: table.map((_: any, i: number) => String(i)) }
      };
    }

    return { data: table, labels: currentEvent?.visuals?.labels };
  }, [algoId, cumulativeState, currentEvent, firstCallArgs]);

  const fractionalModel = useMemo(() => {
    const items = cumulativeState.items || (
      firstCallArgs.weights && firstCallArgs.values
        ? firstCallArgs.weights.map((w: number, id: number) => ({
            id,
            w,
            v: firstCallArgs.values[id],
            ratio: Number((firstCallArgs.values[id] / w).toFixed(2))
          }))
        : []
    );
    return {
      items,
      selected: cumulativeState.selected || [],
      capacity: firstCallArgs.capacity ?? cumulativeState.capacity ?? 0,
      remainingCapacity: cumulativeState.rem_capacity,
      activeItemId: currentEvent?.indices?.i ?? currentEvent?.visuals?.nodes?.[0] ?? null,
      totalValue: cumulativeState.total_value ?? 0,
    };
  }, [cumulativeState, firstCallArgs, currentEvent]);

  const graphHighlights = useMemo(() => {
    const mstEdges = Array.isArray(cumulativeState.mst)
      ? cumulativeState.mst.map((edge: any) => [edge[0], edge[1]])
      : [];
    const parentEdges = Array.isArray(cumulativeState.parent)
      ? cumulativeState.parent
          .map((parent: any, child: number) => parent !== null && parent !== undefined ? [parent, child] : null)
          .filter(Boolean)
      : [];
    const bestTourEdges = Array.isArray(cumulativeState.best_path)
      ? cumulativeState.best_path.slice(0, -1).map((node: number, idx: number) => [node, cumulativeState.best_path[idx + 1]])
      : [];
    return algoId === 'kruskal' ? mstEdges : algoId === 'prim' ? parentEdges : algoId === 'tsp' ? bestTourEdges : [];
  }, [algoId, cumulativeState]);

  const arrayModel = useMemo(() => {
    if (algoId === 'quickSort') {
      const state = currentEvent?.state || {};
      const arr = state.arr || state.result || (
        state.left || state.middle || state.right
          ? [...(state.left || []), ...(state.middle || []), ...(state.right || [])]
          : firstCallArgs.arr
      );
      const pivotIndex = Array.isArray(arr) && state.pivot !== undefined ? arr.indexOf(state.pivot) : currentEvent?.indices?.i;
      return { data: arr, active: pivotIndex !== -1 && pivotIndex !== undefined ? [Number(pivotIndex)] : [] };
    }

    const arr = cumulativeState.arr || firstCallArgs.arr || currentEvent?.state?.result || currentEvent?.state?.merged;
    const active = currentEvent?.visuals?.active_cells || currentEvent?.visuals?.nodes || (
      currentEvent?.indices?.i !== null && currentEvent?.indices?.i !== undefined ? [Number(currentEvent.indices.i)] : []
    );
    const deps = currentEvent?.visuals?.dependency_cells || [];
    return { data: arr, active, deps };
  }, [algoId, currentEvent, cumulativeState, firstCallArgs]);

  const { callStack, treeNodes, activeTreeEdges } = useMemo(() => {
    const stack: any[] = [];
    // nodeMap for O(1) lookup instead of repeated find()
    const nodeMap = new Map<string, any>();
    const tNodes: any[] = [];
    const tEdges: any[] = [];

    for (let i = 0; i <= index; i++) {
      const e = normalizedEvents[i];
      if (!e) continue;

      // Only process true 'call' type events for the stack/tree
      if (e.type === 'call' && e.raw) {
        const raw = e.raw;
        stack.push(raw);
        const label = raw.func || 'anonymous';
        const args = raw.args || {};
        const argsStr = args.n !== undefined ? String(args.n)
          : args.row !== undefined ? `row ${args.row}`
          : args.low !== undefined ? `[${args.low}, ${args.high}]`
          : Array.isArray(args.arr) ? `[${args.arr.join(', ')}]`
          : args.V !== undefined ? `${args.V} nodes`
          : Object.values(args).map((v: any) => Array.isArray(v) ? `[${v.join(', ')}]` : typeof v === 'object' ? JSON.stringify(v) : String(v)).join(', ');

        const node = { id: String(raw.id), label: `${label}(${argsStr})`, children: [] as string[], isActive: false };
        tNodes.push(node);
        nodeMap.set(node.id, node);

        if (raw.parent !== null && raw.parent !== undefined) {
          tEdges.push({ from: String(raw.parent), to: String(raw.id) });
          const pNode = nodeMap.get(String(raw.parent));
          if (pNode && !pNode.children.includes(String(raw.id))) {
            pNode.children.push(String(raw.id));
          }
        }

      } else if (e.type === 'return' && e.raw) {
        // Pop the matching call off the stack (find by id, not blind pop)
        const returnId = String(e.raw.id);
        const stackIdx = stack.map((s: any) => String(s.id)).lastIndexOf(returnId);
        if (stackIdx !== -1) stack.splice(stackIdx, 1);

        // Update the tree node directly using the return's own id
        const node = nodeMap.get(returnId);
        if (node) { node.isResult = true; node.value = e.raw.value; }

      } else if (e.type === 'phase') {
        const activeFrame = stack[stack.length - 1];
        const node = activeFrame ? nodeMap.get(String(activeFrame.id)) : null;
        if (node) {
          const state = e.state || {};
          if (e.phase === 'partition') {
            node.detail = `pivot ${state.pivot}; L[${(state.left || []).join(',')}] R[${(state.right || []).join(',')}]`;
          } else if (e.phase === 'sorted' || e.phase === 'merge_complete') {
            node.detail = `result [${(state.result || state.merged || []).join(',')}]`;
          } else if (e.phase === 'divide') {
            node.detail = `split [${(state.left || []).join(',')}] | [${(state.right || []).join(',')}]`;
          } else if (e.phase === 'merge_start') {
            node.detail = `merge [${(state.left || []).join(',')}] + [${(state.right || []).join(',')}]`;
          } else if (e.phase === 'base_case') {
            node.detail = state.result !== undefined ? `= ${state.result}` : `n=${e.indices?.i}`;
          } else if (e.phase === 'sum_results') {
            node.detail = state.result !== undefined ? `= ${state.result}` : '';
          } else if (e.phase === 'check_middle') {
            node.detail = `mid ${state.mid}; range [${state.low}, ${state.high}]`;
          } else if (e.phase === 'target_found') {
            node.detail = `found at ${state.found_index}`;
          }
        }
      }
    }

    const activeFrame = stack[stack.length - 1];
    if (activeFrame) {
      const activeNode = nodeMap.get(String(activeFrame.id));
      if (activeNode) activeNode.isActive = true;
    }
    return { callStack: stack, treeNodes: tNodes, activeTreeEdges: tEdges };
  }, [normalizedEvents, index]);


  const visualMode = useMemo(() => {
    if (!currentEvent) return 'loading';
    if (algoId === 'obst' && currentEvent.phase === 'complete' && currentEvent.visuals?.tree_nodes) return 'tree';
    if (GRAPH_ALGOS.has(algoId) && baseNodes.length > 0) return 'graph';
    if (ARRAY_ALGOS.has(algoId) && arrayModel.data) return 'array';
    if (TABLE_ALGOS.has(algoId) && tableModel.data) return 'table';
    const hasAnyTableState = normalizedEvents.slice(0, index + 1).some(e => e.state?.dp || e.state?.table || e.state?.cost_matrix || e.state?.lis);
    if (hasAnyTableState) return 'table';
    if (arrayModel.data) return 'array';
    if (currentEvent?.state?.board) return 'grid';
    if (currentEvent?.visuals?.nodes || currentEvent?.visuals?.edges || baseNodes.length > 0) return 'graph';
    if (currentEvent?.visuals?.tree_nodes || treeNodes.length > 0) return 'tree';
    return 'empty';
  }, [currentEvent, normalizedEvents, index, treeNodes.length, baseNodes.length, algoId, arrayModel.data, tableModel.data]);

  const stageLayout = useMemo(() => {
    if (algoId === 'obst' && currentEvent?.phase === 'complete') return 'tree';
    if (algoId === 'fractionalKnapsack') return 'fractional';
    if (algoId === 'binarySearch' && treeNodes.length > 0) return 'binary-tree-state';
    if (GRAPH_TABLE_ALGOS.has(algoId) && tableModel.data) return 'graph-table';
    if (algoId === 'nQueens' && treeNodes.length > 0) return 'grid-tree';
    if (RECURSION_TREE_ALGOS.has(algoId) && treeNodes.length > 0) return 'tree';
    if (DP_TREE_ALGOS.has(algoId) && tableModel.data) return 'table';
    return visualMode;
  }, [algoId, currentEvent?.phase, tableModel.data, treeNodes.length, arrayModel.data, visualMode]);

  if (events.length === 0) {
    return (
      <div className="flex h-full w-full items-center justify-center bg-[#05070a] p-8 text-center">
        <div className="max-w-md rounded-lg border border-white/10 bg-white/[0.04] p-6">
          <p className="mb-2 text-xs font-black uppercase tracking-[0.25em] text-slate-500">No events</p>
          <h2 className="mb-3 text-2xl font-black text-white">{algoName}</h2>
          <p className="text-sm leading-relaxed text-slate-400">The algorithm did not return visualization steps. Open the parameters and run it again.</p>
        </div>
      </div>
    );
  }

  const renderGraphView = () => (
    <MemoizedGraphView
      nodes={baseNodes}
      edges={baseEdges}
      activeNodes={currentEvent?.visuals?.nodes}
      visitedNodes={cumulativeState.visited}
      activeEdges={currentEvent?.visuals?.active_edges}
      dependencyEdges={[...(graphHighlights as number[][]), ...((currentEvent?.visuals?.dependency_cells as number[][]) || [])]}
    />
  );

  const renderTreeView = () => (
    <MemoizedTreeView
      nodes={currentEvent?.visuals?.tree_nodes || treeNodes}
      activeId={currentEvent?.visuals?.active_node_id as string}
      activeEdges={activeTreeEdges}
    />
  );

  const renderTableView = () => (
    <MemoizedTableView
      data={tableModel.data}
      activeCells={currentEvent?.visuals?.active_cells as number[][]}
      dependencyCells={currentEvent?.visuals?.dependency_cells as number[][]}
      labels={tableModel.labels}
    />
  );

  const renderArrayView = () => (
    <MemoizedArrayView
      data={arrayModel.data}
      activeIndices={arrayModel.active as number[]}
      dependencyIndices={arrayModel.deps as unknown as number[]}
      rangeStart={cumulativeState.low ?? cumulativeState.new_low}
      rangeEnd={cumulativeState.high ?? cumulativeState.new_high}
      pivotValue={currentEvent?.state?.pivot}
      targetValue={cumulativeState.target}
    />
  );

  const renderFractionalView = () => (
    <MemoizedFractionalKnapsackView
      items={fractionalModel.items}
      selected={fractionalModel.selected}
      capacity={fractionalModel.capacity}
      remainingCapacity={fractionalModel.remainingCapacity}
      activeItemId={fractionalModel.activeItemId}
      totalValue={fractionalModel.totalValue}
    />
  );

  const renderBinarySearchStrip = () => (
    <div className="h-full w-full rounded-lg border border-white/10 bg-black/25 px-4 py-3">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <span className="text-[10px] font-black uppercase tracking-[0.22em] text-cyan-200">Current Search State</span>
        <div className="flex flex-wrap gap-2 font-mono text-xs">
          <span className="rounded border border-white/10 bg-white/[0.04] px-2 py-1 text-slate-300">target {cumulativeState.target}</span>
          <span className="rounded border border-white/10 bg-white/[0.04] px-2 py-1 text-slate-300">low {cumulativeState.low ?? cumulativeState.new_low}</span>
          <span className="rounded border border-white/10 bg-white/[0.04] px-2 py-1 text-slate-300">high {cumulativeState.high ?? cumulativeState.new_high}</span>
          {cumulativeState.mid !== undefined && <span className="rounded border border-yellow-300/30 bg-yellow-300/10 px-2 py-1 text-yellow-100">mid {cumulativeState.mid}</span>}
        </div>
      </div>
      <div className="flex h-20 items-end justify-center gap-2 overflow-hidden">
        {(arrayModel.data || []).map((value: number, idx: number) => {
          const low = cumulativeState.low ?? cumulativeState.new_low ?? 0;
          const high = cumulativeState.high ?? cumulativeState.new_high ?? (arrayModel.data?.length || 1) - 1;
          const mid = cumulativeState.mid ?? currentEvent?.indices?.i;
          const active = idx === mid;
          const inRange = idx >= low && idx <= high;
          return (
            <div key={idx} className={`flex min-w-10 flex-col items-center gap-1 rounded border px-2 py-1 font-mono text-xs ${active ? 'border-yellow-300 bg-yellow-300/20 text-yellow-100' : inRange ? 'border-cyan-400/30 bg-cyan-400/10 text-cyan-100' : 'border-white/10 bg-white/[0.03] text-slate-600'}`}>
              <span className="font-black">{value}</span>
              <span className="text-[9px] opacity-70">{idx}</span>
            </div>
          );
        })}
      </div>
    </div>
  );

  const renderGridView = () => (
    <MemoizedGridView
      size={currentEvent?.state?.board?.length || 4}
      board={currentEvent?.state?.board}
      activeRow={currentEvent?.indices?.i as number}
      activeCol={currentEvent?.indices?.j as number}
      isValid={currentEvent?.state?.is_valid}
    />
  );

  const renderEmptyView = () => (
    <div className="w-full h-full flex flex-col items-center justify-center text-slate-800 gap-4 opacity-40">
      <div className="p-4 rounded-full bg-slate-800/10 border border-slate-800/20">
        <Activity className="w-10 h-10" />
      </div>
      <div className="text-center">
        <p className="font-mono text-[10px] uppercase tracking-[0.3em] font-black text-slate-600">Cognitive Engine Idle</p>
        <p className="text-[9px] text-slate-700 mt-1 uppercase tracking-widest font-bold">Waiting for computational signals...</p>
      </div>
    </div>
  );

  const renderSingleView = (mode: string) => {
    if (mode === 'graph') return renderGraphView();
    if (mode === 'tree') return renderTreeView();
    if (mode === 'table') return renderTableView();
    if (mode === 'array') return renderArrayView();
    if (mode === 'fractional') return renderFractionalView();
    if (mode === 'grid') return renderGridView();
    return renderEmptyView();
  };

  const renderPanel = (title: string, subtitle: string, content: React.ReactNode) => (
    <section className="relative min-h-0 overflow-hidden rounded-lg border border-white/10 bg-black/20">
      <div className="absolute left-4 top-3 z-20 flex items-center gap-2">
        <span className="rounded bg-black/70 px-2 py-1 text-[10px] font-black uppercase tracking-[0.2em] text-cyan-200">{title}</span>
        <span className="hidden rounded bg-black/50 px-2 py-1 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-500 sm:inline">{subtitle}</span>
      </div>
      <div className="h-full w-full pt-8">
        {content}
      </div>
    </section>
  );

  const renderStageView = () => {
    if (stageLayout === 'graph-table') {
      return (
        <div className={`grid h-full w-full grid-cols-1 gap-4 ${algoId === 'floyd_warshall' ? 'xl:grid-cols-[0.95fr_1.25fr]' : 'xl:grid-cols-[1fr_1.05fr]'}`}>
          {renderPanel('Graph', 'nodes and edges', renderGraphView())}
          {renderPanel(algoId === 'floyd_warshall' ? 'Distance Table' : 'State Table', 'live values', renderTableView())}
        </div>
      );
    }

    if (stageLayout === 'binary-tree-state') {
      return (
        <div className="grid h-full w-full grid-rows-[1fr_132px] gap-4">
          {renderPanel('Recursion Tree', 'range decisions', renderTreeView())}
          {renderBinarySearchStrip()}
        </div>
      );
    }

    if (stageLayout === 'grid-tree') {
      return (
        <div className="grid h-full w-full grid-cols-1 gap-4 xl:grid-cols-[1fr_1fr]">
          {renderPanel('Board', 'placement state', renderGridView())}
          {renderPanel('Backtracking Tree', 'row decisions', renderTreeView())}
        </div>
      );
    }

    return renderSingleView(stageLayout);
  };

  return (
    <div className="flex flex-col w-full h-full text-slate-200">
      
      {/* --- PREMIUM COMPACT HEADER --- */}
      <header className="min-h-16 shrink-0 border-b border-white/10 bg-[#0b0f14]/85 backdrop-blur-xl flex flex-wrap items-center justify-between gap-3 px-5 py-3 z-40">
        <div className="flex items-center gap-3 min-w-0">
          <button
            type="button"
            onClick={onOpenLibrary}
            className="flex items-center gap-2 rounded-lg border border-white/10 bg-white/[0.04] px-3 py-2 text-sm font-bold text-slate-200 hover:border-cyan-400/50 hover:text-white transition-colors"
          >
            <PanelLeftOpen className="w-4 h-4 text-cyan-300" />
            <span className="hidden sm:inline">Algorithms</span>
          </button>

          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-bold mb-0.5 truncate max-w-[220px] sm:max-w-none">{algoName}</span>
            <h2 className="text-lg font-black text-white tracking-tight leading-none uppercase">Step {index + 1} <span className="text-slate-500 font-normal">/ {total}</span></h2>
          </div>
          <div className="w-px h-8 bg-white/10 mx-1 hidden md:block" />
          
          {/* Progress Bar Mini */}
          <div className="w-48 h-1 bg-white/10 rounded-full overflow-hidden relative hidden md:block">
            <motion.div 
              className="absolute inset-0 bg-cyan-400 shadow-[0_0_12px_rgba(34,211,238,0.45)]"
              initial={{ width: 0 }}
              animate={{ width: `${((index + 1) / total) * 100}%` }}
              transition={{ ease: "circOut" }}
            />
          </div>
        </div>

        {/* Global Playback Controls */}
        <div className="flex items-center bg-white/[0.04] border border-white/10 rounded-full px-2 py-1 gap-1 shadow-xl shadow-black/20">
          <button onClick={prev} disabled={index === 0} className="p-2 hover:bg-white/10 rounded-full disabled:opacity-30 transition-colors">
            <SkipBack className="w-4 h-4" />
          </button>
          <button 
            onClick={() => setIsPlaying(!isPlaying)}
            className="p-2.5 bg-cyan-400 hover:bg-cyan-300 text-slate-950 rounded-full shadow-lg shadow-cyan-500/20 transition-all active:scale-90"
          >
            {isPlaying ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current translate-x-0.5" />}
          </button>
          <button onClick={next} disabled={index === total - 1} className="p-2 hover:bg-white/10 rounded-full disabled:opacity-30 transition-colors">
            <SkipForward className="w-4 h-4" />
          </button>
        </div>

        <div className="flex items-center gap-3 min-w-0">
           {/* Step Jump Input */}
           <div className="hidden sm:flex items-center bg-white/[0.04] rounded-lg px-3 py-1.5 border border-white/10">
             <span className="text-[10px] font-bold text-slate-500 mr-2 uppercase tracking-tighter">Go to</span>
             <input 
               type="text"
               placeholder={`1-${total}`}
               className="bg-transparent w-12 text-xs font-mono focus:outline-none text-cyan-300 placeholder-slate-600 border-none p-0"
               onKeyDown={(e) => {
                 if (e.key === 'Enter') {
                   const val = parseInt((e.target as HTMLInputElement).value);
                   if (!isNaN(val) && val >= 1 && val <= total) {
                     jumpTo(val - 1);
                     (e.target as HTMLInputElement).value = '';
                   }
                 }
               }}
             />
           </div>

           <button 
             onClick={onOpenConfig}
             className="flex items-center gap-2 px-4 py-2 bg-white/[0.04] hover:bg-white/10 rounded-lg text-sm font-bold border border-white/10 shadow-lg text-slate-300 transition-all active:scale-95"
           >
             <SlidersHorizontal className="w-4 h-4 text-cyan-300" />
             <span className="hidden sm:inline">Configure</span>
           </button>
        </div>
      </header>

      {/* --- CONTENT AREA: SPLIT SCREEN --- */}
      <div className="flex-1 flex overflow-hidden lg:flex-row flex-col min-h-0 min-w-0 bg-[#05070a]">
        
        {/* Main Canvas (BIG) */}
        <div className="flex-1 relative overflow-hidden flex items-center justify-center p-4 lg:p-6">
          {/* Professional Background Mesh/Gradient */}
          <div className="absolute inset-0 pointer-events-none z-0">
             <div className="absolute inset-0 bg-[#05070a]" />
             <div className="absolute inset-0 opacity-70" style={{ backgroundImage: 'linear-gradient(rgba(255,255,255,0.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.035) 1px, transparent 1px)', backgroundSize: '42px 42px' }} />
             <div className="absolute inset-x-0 top-0 h-44 bg-gradient-to-b from-cyan-500/10 to-transparent" />
          </div>

          <AnimatePresence mode="wait">
            <ErrorBoundary>
              <motion.div 
                key={`${algoId}-${index}-${stageLayout}`}
                initial={{ opacity: 0, scale: 0.99 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 1.01 }}
                className="w-full h-full z-10"
              >
                {renderStageView()}
              </motion.div>
            </ErrorBoundary>
          </AnimatePresence>
        </div>

        {/* Smart Sidebar (RIGHT) */}
        <aside className="w-full lg:w-[400px] border-l border-white/10 bg-[#0b0f14] overflow-hidden flex flex-col shrink-0 lg:h-full h-[300px]">
          <div className="flex-1 overflow-y-auto custom-scrollbar p-1">
             {/* Education Panel (Pass current controls to keep it interactive) */}
             <MemoizedEducationPanel 
                event={currentEvent} 
                callStack={callStack} 
                isPlaying={isPlaying} 
                onTogglePlay={() => setIsPlaying(!isPlaying)} 
                onNext={next} 
                onPrev={prev} 
                index={index} 
                total={total} 
             />
             
             {/* Dynamic Formula Overlay — shown for all algorithms */}
             <div className="px-6 py-4 border-t border-slate-800/50">
               <h3 className="text-xs uppercase tracking-widest text-slate-500 font-bold mb-4">Formula Context</h3>
               <FormulaPanel currentEvent={currentEvent} algoId={algoId} />
             </div>

          </div>
          
          {/* Quick Stats / Speed at Bottom of Sidebar */}
          <div className="p-6 bg-black/25 border-t border-white/10 flex flex-col gap-4">
             <div className="flex items-center justify-between">
                <span className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">Playback Speed</span>
                <span className="text-xs font-mono text-cyan-300">{speed}ms</span>
             </div>
             <input 
                type="range" min="100" max="2000" step="100"
                value={2100 - speed}
                onChange={(e) => setSpeed(2100 - parseInt(e.target.value))}
                className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-cyan-400"
             />
          </div>
        </aside>

      </div>
    </div>
  );
};
