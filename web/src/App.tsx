import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  GitPullRequest, 
  Settings, ChevronRight,
  Zap, Database, Binary,
  Network, Activity, LayoutPanelLeft, Layers,
  PanelLeftOpen, X, Search
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import { ParameterForm } from './components/ParameterForm';
import { VisualizerStage } from './components/VisualizerStage';

const ALGORITHMS = [
  { id: 'fib', name: 'Fibonacci (Recursive)', icon: Zap, type: 'search' },
  { id: 'fibDP', name: 'Fibonacci (DP)', icon: Zap, type: 'dp' },
  { id: 'knapsack', name: '0/1 Knapsack', icon: Database, type: 'dp' },
  { id: 'fractionalKnapsack', name: 'Fractional Knapsack', icon: Database, type: 'greedy' },
  { id: 'lis', name: 'LIS', icon: Binary, type: 'dp' },
  { id: 'lcs', name: 'LCS', icon: Layers, type: 'dp' },
  { id: 'mergeSort', name: 'Merge Sort', icon: LayoutPanelLeft, type: 'sort' },
  { id: 'quickSort', name: 'Quick Sort', icon: Zap, type: 'sort' },
  { id: 'binarySearch', name: 'Binary Search', icon: Binary, type: 'search' },
  { id: 'nQueens', name: 'N-Queens', icon: LayoutPanelLeft, type: 'backtracking' },
  { id: 'obst', name: 'Optimal BST', icon: Network, type: 'dp' },
  { id: 'dijkstra', name: 'Dijkstra', icon: Network, type: 'graph' },
  { id: 'prim', name: 'Prim', icon: Network, type: 'graph' },
  { id: 'kruskal', name: 'Kruskal', icon: Network, type: 'graph' },
  { id: 'floyd_warshall', name: 'Floyd-Warshall', icon: Database, type: 'graph' },
  { id: 'tsp', name: 'TSP (Backtracking)', icon: Activity, type: 'graph' },
];

export default function App() {
  const [selectedAlgo, setSelectedAlgo] = useState(ALGORITHMS[0]);
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [showConfig, setShowConfig] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAlgorithm = async (algoId: string, paramsObj?: any) => {
    setLoading(true);
    setError(null);
    
    try {
      const apiUrl = import.meta.env.VITE_API_URL || '';
      const endpoint = apiUrl ? `${apiUrl}/solve/${algoId}` : `/solve/${algoId}`;
      const { data } = await axios.post(endpoint, {
        params: paramsObj || {} 
      });
      setEvents(data.events || []);
      setShowConfig(false);
      setSidebarOpen(false);
    } catch (err) {
      console.error("API Error:", err);
      const message = axios.isAxiosError(err)
        ? err.response?.data?.detail || err.message
        : 'Unable to run this algorithm.';
      setError(String(message));
      setEvents([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Auto fetch when selection changes to fallback defaults
    fetchAlgorithm(selectedAlgo.id);
    setShowConfig(false);
  }, [selectedAlgo.id]);

  return (
    <div className="relative flex h-screen bg-[#05070a] text-slate-200 overflow-hidden selection:bg-cyan-500/30">
      <AnimatePresence>
        {sidebarOpen && (
          <>
            <motion.button
              type="button"
              aria-label="Close algorithm drawer"
              className="absolute inset-0 z-30 bg-black/50 backdrop-blur-[2px] lg:hidden"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setSidebarOpen(false)}
            />

            <motion.aside
              initial={{ x: -330, opacity: 0.6 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: -330, opacity: 0.6 }}
              transition={{ type: 'spring', damping: 28, stiffness: 260 }}
              className="absolute left-0 top-0 bottom-0 z-40 w-[320px] bg-[#0b0f14]/95 border-r border-white/10 flex flex-col shadow-2xl shadow-black/50 backdrop-blur-xl"
            >
              <div className="px-5 pt-5 pb-4 border-b border-white/10">
                <div className="flex items-center justify-between gap-3 mb-5">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="p-2 bg-cyan-500 rounded-lg shadow-lg shadow-cyan-500/20">
                      <GitPullRequest className="w-5 h-5 text-slate-950" />
                    </div>
                    <div className="min-w-0">
                      <h1 className="text-lg font-black tracking-tight text-white truncate">Algorithm Studio</h1>
                      <p className="text-[10px] uppercase tracking-[0.22em] text-slate-500 font-bold">Choose a model</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => setSidebarOpen(false)}
                    className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-colors"
                    aria-label="Close algorithms"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>

                <div className="flex items-center gap-2 rounded-lg border border-white/10 bg-black/25 px-3 py-2">
                  <Search className="w-4 h-4 text-slate-500" />
                  <span className="text-xs text-slate-500">Pick an algorithm and the drawer clears the stage</span>
                </div>
              </div>

              <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto custom-scrollbar">
                {ALGORITHMS.map((algo) => (
                  <button
                    key={algo.id}
                    onClick={() => setSelectedAlgo(algo)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group ${
                      selectedAlgo.id === algo.id 
                        ? 'bg-cyan-500 text-slate-950 shadow-xl shadow-cyan-500/20' 
                        : 'text-slate-400 hover:bg-white/[0.08] hover:text-slate-100'
                    }`}
                  >
                    <algo.icon className={`w-5 h-5 ${selectedAlgo.id === algo.id ? 'text-slate-950' : 'group-hover:text-cyan-300'}`} />
                    <span className="font-semibold text-sm text-nowrap">{algo.name}</span>
                    {selectedAlgo.id === algo.id && <ChevronRight className="w-4 h-4 ml-auto opacity-70" />}
                  </button>
                ))}
              </nav>

              <div className="p-5 border-t border-white/10">
                <div className="flex items-center gap-2 text-slate-500 px-2">
                  <Settings className="w-4 h-4" />
                  <span className="text-xs font-medium">Configure inputs from the stage header.</span>
                </div>
              </div>
            </motion.aside>
          </>
        )}
      </AnimatePresence>

      {!sidebarOpen && (
        <motion.button
          type="button"
          onClick={() => setSidebarOpen(true)}
          initial={{ opacity: 0, x: -8 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute left-4 bottom-4 z-50 flex items-center gap-2 rounded-lg border border-white/10 bg-[#0b0f14]/90 px-3 py-2 text-sm font-bold text-slate-200 shadow-xl shadow-black/30 backdrop-blur-xl hover:border-cyan-400/50 hover:text-white transition-colors lg:hidden"
        >
          <PanelLeftOpen className="w-4 h-4 text-cyan-300" />
          Algorithms
        </motion.button>
      )}

      {/* Main Content Area [Visualization] */}
      <main className="flex-1 relative flex flex-col min-w-0 h-screen overflow-hidden">
         {/* Config Overlay - Only when showConfig is true */}
         <AnimatePresence>
           {showConfig && (
             <motion.div 
               initial={{ opacity: 0, y: -20 }}
               animate={{ opacity: 1, y: 0 }}
               exit={{ opacity: 0, y: -20 }}
               className="absolute inset-0 z-50 bg-slate-950/80 backdrop-blur-sm p-8"
             >
               <ParameterForm 
                 algoId={selectedAlgo.id} 
                 onRun={(params) => fetchAlgorithm(selectedAlgo.id, params)} 
                 onCancel={() => setShowConfig(false)}
               />
             </motion.div>
           )}
         </AnimatePresence>
         
         {loading ? (
            <div className="w-full h-full flex flex-col items-center justify-center gap-6 bg-[#020617]">
               <div className="relative">
                 <div className="w-16 h-16 border-4 border-indigo-500/20 border-t-indigo-500 rounded-full animate-spin shadow-[0_0_20px_rgba(99,102,241,0.3)]" />
                 <Activity className="absolute inset-0 m-auto w-6 h-6 text-indigo-400 animate-pulse" />
               </div>
               <p className="text-slate-400 animate-pulse font-mono uppercase tracking-[0.2em] text-xs">Synthesizing {selectedAlgo.name}</p>
            </div>
         ) : (
           error ? (
             <div className="flex h-full w-full items-center justify-center bg-[#05070a] p-8">
               <div className="max-w-lg rounded-lg border border-red-400/30 bg-red-950/30 p-6 text-center shadow-2xl shadow-black/30">
                 <p className="mb-2 text-xs font-black uppercase tracking-[0.25em] text-red-300">Algorithm failed</p>
                 <h2 className="mb-4 text-2xl font-black text-white">{selectedAlgo.name}</h2>
                 <p className="mb-6 text-sm leading-relaxed text-red-100">{error}</p>
                 <div className="flex justify-center gap-3">
                   <button
                     type="button"
                     onClick={() => setShowConfig(true)}
                     className="rounded-lg bg-red-400 px-4 py-2 text-sm font-bold text-red-950 hover:bg-red-300"
                   >
                     Fix Inputs
                   </button>
                   <button
                     type="button"
                     onClick={() => setSidebarOpen(true)}
                     className="rounded-lg border border-white/10 px-4 py-2 text-sm font-bold text-slate-200 hover:bg-white/10"
                   >
                     Algorithms
                   </button>
                 </div>
               </div>
             </div>
           ) : (
             <VisualizerStage 
               key={selectedAlgo.id} 
               events={events} 
               algoId={selectedAlgo.id} 
               algoName={selectedAlgo.name}
               onOpenConfig={() => setShowConfig(true)}
               onOpenLibrary={() => setSidebarOpen(true)}
             />
           )
         )}
      </main>
    </div>
  );
}
