import React from 'react';
import { motion } from 'framer-motion';

interface ArrayViewProps {
  data: number[];
  activeIndices?: any[];
  dependencyIndices?: any[];
  resultIndices?: number[];
  rangeStart?: number;
  rangeEnd?: number;
  pivotValue?: number;
  targetValue?: number;
}

export const ArrayView: React.FC<ArrayViewProps> = ({ 
  data, 
  activeIndices = [], 
  dependencyIndices = [], 
  resultIndices = [],
  rangeStart,
  rangeEnd,
  pivotValue,
  targetValue
}) => {
  if (!data || data.length === 0) {
    return (
      <div className="w-full h-full flex items-center justify-center text-slate-500">
        No array data available.
      </div>
    );
  }

  const maxValue = Math.max(...data, 1); // Avoid div by zero
  const activeSet = new Set(
    activeIndices.flatMap((idx: any) => Array.isArray(idx) ? idx : [idx]).map((idx) => Number(idx))
  );
  const dependencySet = new Set(
    dependencyIndices.flatMap((idx: any) => Array.isArray(idx) ? idx : [idx]).map((idx) => Number(idx))
  );

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8">
      {(targetValue !== undefined || pivotValue !== undefined || rangeStart !== undefined) && (
        <div className="mb-8 flex flex-wrap items-center justify-center gap-3 text-xs font-mono">
          {targetValue !== undefined && <span className="rounded-lg border border-cyan-400/30 bg-cyan-400/10 px-3 py-2 text-cyan-200">target = {targetValue}</span>}
          {pivotValue !== undefined && <span className="rounded-lg border border-yellow-400/30 bg-yellow-400/10 px-3 py-2 text-yellow-200">pivot = {pivotValue}</span>}
          {rangeStart !== undefined && rangeEnd !== undefined && <span className="rounded-lg border border-white/10 bg-white/[0.04] px-3 py-2 text-slate-300">range = [{rangeStart}, {rangeEnd}]</span>}
        </div>
      )}
      <div className="flex items-end justify-center w-full h-64 gap-2">
        {data.map((value, idx) => {
          let bgColor = 'bg-slate-700'; // default
          let borderColor = 'border-slate-600';
          const outOfRange = rangeStart !== undefined && rangeEnd !== undefined && (idx < rangeStart || idx > rangeEnd);

          if (resultIndices.includes(idx)) {
            bgColor = 'bg-green-500/80';
            borderColor = 'border-green-400';
          } else if (activeSet.has(idx)) {
            bgColor = 'bg-yellow-400/80';
            borderColor = 'border-yellow-300';
          } else if (dependencySet.has(idx)) {
            bgColor = 'bg-blue-500/80';
            borderColor = 'border-blue-400';
          }

          const heightPercent = `${(value / maxValue) * 100}%`;

          return (
            <div key={idx} className={`flex flex-col items-center gap-2 group flex-1 max-w-16 transition-opacity ${outOfRange ? 'opacity-25' : 'opacity-100'}`}>
              <motion.div
                layout
                initial={{ height: 0 }}
                animate={{ height: heightPercent }}
                transition={{ type: 'spring', stiffness: 300, damping: 25 }}
                className={`w-full rounded-t-md border-t-2 border-l border-r ${bgColor} ${borderColor} relative`}
              >
                {/* Tooltip tooltip on hover */}
                <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-slate-900 text-slate-200 text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10 border border-slate-700 shadow-xl">
                  value: {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                </div>
              </motion.div>
              <span className="text-slate-400 font-mono text-sm">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
              <span className="text-slate-600 font-mono text-[10px] mt-1">[{idx}]</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const MemoizedArrayView = React.memo(ArrayView);
