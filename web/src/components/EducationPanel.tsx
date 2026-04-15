import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, Variable, Activity } from 'lucide-react';
import type { NormalizedEvent } from '../utils/eventAdapter';

interface EducationPanelProps {
  event: NormalizedEvent | null;
  callStack?: any[];
  index: number;
  total: number;
  isPlaying: boolean;
  onTogglePlay: () => void;
  onNext: () => void;
  onPrev: () => void;
}

export const EducationPanel: React.FC<EducationPanelProps> = ({
  event,
  callStack = [],
  index,
}) => {
  if (!event) return null;

  const { phase, message, indices, values } = event;
  const state = event.state || {};

  // Render variables automatically based on what's available
  const activeVars = Object.entries(indices)
    .filter(([_, val]) => val !== null && val !== undefined)
    .map(([key, val]) => (
      <span key={key} className="px-2 py-1 bg-slate-800 rounded text-xs font-mono text-indigo-300 border border-slate-700">
        {key} = {typeof val === 'object' ? JSON.stringify(val) : String(val)}
      </span>
    ));

  // Determine what to show for explanation based on raw data
  const renderExplanation = () => {
    // If we have explicit new/old values (like in DP or Dijkstra weight updates)
    if (values.new !== null && values.old !== null) {
       const isUpdate = values.new < values.old; // Example logic, assuming smaller is better (like Dijkstra)
       
       return (
         <div className="flex flex-col gap-3 mt-4">
           <div className="p-4 rounded-xl border border-slate-700/50 bg-slate-800/30 font-mono text-sm">
             <div className="flex items-center gap-2 text-slate-400 mb-2">
               <span>Current value:</span>
               <span className="text-slate-200">
                 {typeof values.old === 'object' ? JSON.stringify(values.old) : (values.old > 999999 ? "∞" : String(values.old))}
               </span>
             </div>
             <div className="flex items-center gap-2 text-slate-400">
               <span>Proposed value:</span>
               <span className="text-yellow-400">
                 {typeof values.new === 'object' ? JSON.stringify(values.new) : String(values.new)}
               </span>
             </div>
           </div>
           
           {values.new !== values.old && (
             <div className={`p-3 rounded-lg flex items-center justify-center font-bold text-sm ${
               isUpdate ? 'bg-green-500/20 text-green-400 border border-green-500/30' : 'bg-red-500/20 text-red-400 border border-red-500/30'
             }`}>
               {isUpdate 
                 ? `${typeof values.new === 'object' ? JSON.stringify(values.new) : values.new} < ${values.old > 999999 ? '∞' : (typeof values.old === 'object' ? JSON.stringify(values.old) : values.old)} → Updating!`
                 : `${typeof values.new === 'object' ? JSON.stringify(values.new) : values.new} ≥ ${values.old > 999999 ? '∞' : (typeof values.old === 'object' ? JSON.stringify(values.old) : values.old)} → Keeping original`
               }
             </div>
           )}
         </div>
       );
    }
    
    return (
      <div className="mt-4 p-4 rounded-xl border border-slate-700/50 bg-slate-800/30 text-slate-300 leading-relaxed shadow-inner">
        {message}
      </div>
    );
  };

  const resultFacts = [
    state.current_path ? { label: 'Current path', value: Array.isArray(state.current_path) ? state.current_path.join(' -> ') : state.current_path } : null,
    state.current_cost !== undefined ? { label: 'Current cost', value: state.current_cost } : null,
    state.best_path?.length ? { label: 'Best path', value: state.best_path.join(' -> ') } : null,
    state.best_cost !== undefined ? { label: 'Best cost', value: state.best_cost } : null,
    state.optimal_path?.length ? { label: 'Root path', value: state.optimal_path.join(' -> ') } : null,
    state.optimal_cost !== undefined ? { label: 'Optimal cost', value: state.optimal_cost } : null,
    state.root_key !== undefined ? { label: 'Root key', value: state.root_key } : null,
    state.total_value !== undefined ? { label: 'Total value', value: state.total_value } : null,
    state.rem_capacity !== undefined ? { label: 'Remaining capacity', value: state.rem_capacity } : null,
  ].filter(Boolean) as { label: string; value: any }[];

  return (
    <div className="flex flex-col h-full bg-[#020617]/40 backdrop-blur-md text-slate-100 p-6 relative z-20">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.1)]">
            <BookOpen className="w-5 h-5 text-indigo-400" />
          </div>
          <h2 className="text-sm font-black tracking-[0.2em] text-white uppercase italic">Narrative</h2>
        </div>
        <span className="px-3 py-1 bg-cyan-500/10 text-cyan-400 text-[10px] font-black rounded-lg uppercase tracking-widest border border-cyan-500/20">
          {phase}
        </span>
      </div>

      {/* Dynamic Content */}
      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar flex flex-col gap-8">
        
        {/* Variables Section */}
        {(activeVars.length > 0 || resultFacts.length > 0) && (
          <div className="animate-in fade-in slide-in-from-left-2 duration-500">
            <div className="flex items-center gap-2 mb-4">
               <Variable className="w-3.5 h-3.5 text-slate-500" />
               <h3 className="text-[10px] uppercase tracking-[0.25em] text-slate-500 font-black">Live State</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {activeVars}
              {resultFacts.map((fact) => (
                <span key={fact.label} className="px-2 py-1 bg-cyan-500/10 rounded text-xs font-mono text-cyan-200 border border-cyan-500/20">
                  {fact.label}: {typeof fact.value === 'object' ? JSON.stringify(fact.value) : String(fact.value)}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Call Stack Visualization */}
        {callStack.length > 0 && (
          <div className="animate-in fade-in slide-in-from-left-2 duration-700 delay-100">
            <div className="flex items-center gap-2 mb-4">
               <Activity className="w-3.5 h-3.5 text-slate-500" />
               <h3 className="text-[10px] uppercase tracking-[0.25em] text-slate-500 font-black">Stack Trace</h3>
            </div>
            <div className="flex flex-col gap-1.5 p-4 rounded-2xl bg-[#020617]/60 border border-slate-800/80 font-mono text-[11px] relative overflow-hidden shadow-inner">
               {callStack.map((frame, i) => (
                 <motion.div 
                   key={frame.id}
                   initial={{ opacity: 0, x: -10 }}
                   animate={{ opacity: 1, x: 0 }}
                   className={`px-3 py-2 rounded-xl flex justify-between items-center z-10 transition-colors
                     ${i === callStack.length - 1 ? 'bg-indigo-500/20 border border-indigo-500/30 text-white font-bold' : 'text-slate-500 opacity-60'}
                   `}
                 >
                   <span className="truncate pr-4">
                     <span className={i === callStack.length - 1 ? "text-indigo-300" : ""}>{frame.func}</span>
                     <span className="opacity-40 ml-1">({Object.values(frame.args || {}).join(', ')})</span>
                   </span>
                   {i === callStack.length - 1 && (
                     <div className="flex items-center gap-1.5">
                       <span className="text-[9px] text-indigo-400 font-black tracking-tighter uppercase mr-1">Active</span>
                       <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse shadow-[0_0_8px_rgba(129,140,248,0.8)]" />
                     </div>
                   )}
                 </motion.div>
               ))}
            </div>
          </div>
        )}

        {/* Step Explanation */}
        <AnimatePresence mode="wait">
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.4 }}
            className="flex-1"
          >
             <div className="flex items-center gap-2 mb-4">
               <div className="w-1.5 h-1.5 rounded-full bg-indigo-500" />
               <h3 className="text-[10px] uppercase tracking-[0.25em] text-slate-500 font-black">Explanation</h3>
            </div>
            <div className="text-slate-300 leading-relaxed text-sm font-medium">
              {renderExplanation()}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Bottom info: progress indicator only */}
      <div className="mt-8 pt-6 border-t border-slate-900 flex items-center justify-between opacity-50">
        <span className="text-[9px] font-black text-slate-600 uppercase tracking-[0.25em]">Cognitive Phase</span>
        <div className="flex items-center gap-2">
          <Activity className="w-3 h-3 text-cyan-400/50" />
          <span className="text-[9px] font-mono text-slate-500 font-bold uppercase tracking-widest">{phase}</span>
        </div>
      </div>
    </div>
  );
};

export const MemoizedEducationPanel = React.memo(EducationPanel);
