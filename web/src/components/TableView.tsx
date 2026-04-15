import React, { useRef, useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Activity } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: any[]) {
  return twMerge(clsx(inputs));
}

interface TableViewProps {
  data: any[] | any[][];
  activeCells?: number[][];
  dependencyCells?: (number[] | number[][] | null)[];
  labels?: {
    rows?: string[];
    cols?: string[];
  };
}

const TableViewComponent: React.FC<TableViewProps> = ({
  data,
  activeCells = [],
  dependencyCells = [],
  labels
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cellRefs = useRef<Record<string, HTMLTableCellElement | null>>({});
  const [arrows, setArrows] = useState<{ x1: number, y1: number, x2: number, y2: number }[]>([]);

  if (!data || !Array.isArray(data) || data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-slate-500 gap-4">
        <Activity className="w-12 h-12 opacity-10" />
        <p className="font-mono text-xs opacity-20 uppercase tracking-widest">No Data Segment</p>
      </div>
    );
  }

  // Resilient Matrix Normalization
  const matrix: any[][] = useMemo(() => {
    if (!Array.isArray(data)) {
       return [[String(data)]]; // Fallback for primitive or object
    }
    if (data.length === 0) return [[]];
    if (!Array.isArray(data[0])) {
      return [data]; // Wrap 1D array into 2D
    }
    return data as any[][];
  }, [data]);

  const normActive = useMemo(() => (activeCells || []).map(cell => {
    if (typeof cell === 'number') return [0, cell];
    if (Array.isArray(cell) && cell.length === 2) return cell;
    return [-1, -1];
  }), [activeCells]);

  const rawDeps = useMemo(() => (dependencyCells || []).filter(Boolean).flatMap(cell => {
    if (Array.isArray(cell) && typeof cell[0] === 'number') return [[cell[0], cell[1]] as number[]];
    if (Array.isArray(cell) && Array.isArray(cell[0])) return cell as number[][];
    if (typeof cell === 'number') return [[0, cell]];
    return [];
  }), [dependencyCells]);

  // Calculate arrow coordinates
  useEffect(() => {
    if (!containerRef.current) return;
    const newArrows: any[] = [];
    const containerRect = containerRef.current.getBoundingClientRect();

    normActive.forEach(([ar, ac]) => {
      const activeEl = cellRefs.current[`${ar}-${ac}`];
      if (!activeEl) return;
      const activeRect = activeEl.getBoundingClientRect();

      rawDeps.forEach(([dr, dc]) => {
        const depEl = cellRefs.current[`${dr}-${dc}`];
        if (!depEl) return;
        const depRect = depEl.getBoundingClientRect();

        newArrows.push({
          x1: depRect.left + depRect.width / 2 - containerRect.left,
          y1: depRect.top + depRect.height / 2 - containerRect.top,
          x2: activeRect.left + activeRect.width / 2 - containerRect.left,
          y2: activeRect.top + activeRect.height / 2 - containerRect.top,
        });
      });
    });
    setArrows(newArrows);
  }, [data, normActive, rawDeps]);

  return (
    <div className="w-full h-full overflow-auto p-4 flex items-center justify-center z-10">
      <div ref={containerRef} className="relative inline-block max-w-full border border-slate-700/30 rounded-lg bg-slate-800/10 backdrop-blur-xl shadow-2xl overflow-auto">
        
        {/* SVG Layer for Arrows */}
        <svg className="absolute inset-0 pointer-events-none z-30 w-full h-full">
          <defs>
            <marker id="head" orient="auto" markerWidth="4" markerHeight="4" refX="2" refY="2">
              <path d="M0,0 L0,4 L4,2 Z" fill="#60a5fa" /> {/* blue-400 */}
            </marker>
          </defs>
          <AnimatePresence>
            {arrows.map((arrow, idx) => (
              <motion.line
                key={`${idx}-${arrow.x1}-${arrow.y1}`}
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                exit={{ opacity: 0 }}
                x1={arrow.x1} y1={arrow.y1}
                x2={arrow.x2} y2={arrow.y2}
                stroke="#60a5fa" /* blue-400 dependency line */
                strokeWidth="2"
                strokeDasharray="4,4"
                markerEnd="url(#head)"
                className="drop-shadow-[0_0_8px_rgba(96,165,250,0.5)]"
              />
            ))}
          </AnimatePresence>
        </svg>

        <table className="border-collapse table-auto text-sm text-slate-300 relative z-10">
          <thead>
            <tr className="bg-slate-800/40">
              <th className="p-3 border-b border-r border-slate-700/30"></th>
              {matrix[0]?.map((_, j) => (
                <th key={j} className="p-3 border-b border-slate-700/30 font-mono text-slate-400 text-xs uppercase tracking-tighter">
                  {labels?.cols?.[j] ?? `Col ${j}`}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {matrix.map((row, i) => (
              <tr key={i}>
                <th className="p-3 border-r border-slate-700/30 bg-slate-800/40 font-mono text-slate-400 text-xs text-nowrap">
                  {labels?.rows?.[i] ?? `Row ${i}`}
                </th>
                {row.map((cell, j) => {
                  const isActive = normActive.some(([r, c]) => r === i && c === j);
                  const isDep = rawDeps.some(([r, c]) => r === i && c === j);

                  return (
                    <motion.td
                      key={j}
                      ref={(el) => { cellRefs.current[`${i}-${j}`] = el; }}
                      animate={{
                        backgroundColor: isActive 
                          ? 'rgba(250, 204, 21, 0.2)' // yellow-400
                          : isDep ? 'rgba(96, 165, 250, 0.15)' : 'transparent', // blue-400
                        borderColor: isActive ? 'rgba(250, 204, 21, 0.6)' : 'rgba(30, 41, 59, 0.5)'
                      }}
                      className={cn(
                        "p-3 sm:p-4 border border-slate-800/50 text-center font-mono min-w-[52px] sm:min-w-[64px] relative transition-all",
                        isActive && "text-yellow-400 font-bold",
                        isDep && "text-blue-400 font-bold",
                        !isActive && !isDep && "text-slate-300"
                      )}
                    >
                      <span className="relative z-10">
                        {cell === null ? '-' : (typeof cell === 'number' && cell > 999999) ? "∞" : (typeof cell === 'object' ? JSON.stringify(cell) : String(cell))}
                      </span>
                    </motion.td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export const MemoizedTableView = React.memo(TableViewComponent);
