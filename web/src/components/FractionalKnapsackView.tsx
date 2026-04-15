import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface FractionalKnapsackViewProps {
  items: any[];
  selected: any[];
  capacity: number;
  remainingCapacity?: number;
  activeItemId?: number | string | null;
  totalValue?: number;
}

export const FractionalKnapsackView: React.FC<FractionalKnapsackViewProps> = ({
  items,
  selected,
  capacity,
  remainingCapacity,
  activeItemId,
  totalValue = 0,
}) => {
  const selectedById = useMemo(() => new Map((selected || []).map((item: any) => [item.id, item])), [selected]);
  const usedCapacity = Math.max(0, capacity - (remainingCapacity ?? capacity));
  const capacityPercent = capacity > 0 ? Math.min(100, (usedCapacity / capacity) * 100) : 0;

  if (!items || items.length === 0) {
    return (
      <div className="flex h-full w-full items-center justify-center text-slate-500">
        No item data available.
      </div>
    );
  }

  return (
    <div className="flex h-full w-full flex-col justify-center gap-8 p-6 lg:p-10">
      <div className="rounded-lg border border-white/10 bg-black/25 p-5">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-[10px] font-black uppercase tracking-[0.24em] text-slate-500">Knapsack Capacity</p>
            <h3 className="mt-1 text-2xl font-black text-white">
              {usedCapacity.toFixed(1)} / {capacity}
            </h3>
          </div>
          <div className="rounded-lg border border-cyan-400/25 bg-cyan-400/10 px-4 py-2 text-right">
            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-cyan-300">Total Value</p>
            <p className="font-mono text-lg font-black text-cyan-100">{Number(totalValue || 0).toFixed(2)}</p>
          </div>
        </div>
        <div className="h-7 overflow-hidden rounded-lg border border-white/10 bg-slate-950">
          <motion.div
            className="h-full bg-cyan-400"
            initial={{ width: 0 }}
            animate={{ width: `${capacityPercent}%` }}
            transition={{ type: 'spring', stiffness: 180, damping: 24 }}
          />
        </div>
      </div>

      <div className="grid min-h-0 grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-3">
        {items.map((item: any) => {
          const picked = selectedById.get(item.id) as any;
          const fraction = picked?.fraction ?? 0;
          const isActive = String(activeItemId) === String(item.id);

          return (
            <motion.div
              key={item.id}
              layout
              className={`rounded-lg border p-4 shadow-xl transition-colors ${
                isActive
                  ? 'border-yellow-300/70 bg-yellow-300/10'
                  : fraction > 0
                    ? 'border-emerald-400/40 bg-emerald-400/10'
                    : 'border-white/10 bg-white/[0.04]'
              }`}
            >
              <div className="mb-4 flex items-start justify-between gap-3">
                <div>
                  <p className="text-[10px] font-black uppercase tracking-[0.22em] text-slate-500">Item {item.id}</p>
                  <p className="mt-1 font-mono text-sm text-slate-300">ratio {Number(item.ratio).toFixed(2)}</p>
                </div>
                <span className="rounded bg-black/35 px-2 py-1 font-mono text-xs font-bold text-slate-200">
                  {Math.round(fraction * 100)}%
                </span>
              </div>

              <div className="mb-4 grid grid-cols-2 gap-2 text-xs font-mono">
                <span className="rounded border border-white/10 bg-black/20 px-2 py-2 text-slate-300">w = {item.w}</span>
                <span className="rounded border border-white/10 bg-black/20 px-2 py-2 text-slate-300">v = {item.v}</span>
              </div>

              <div className="h-5 overflow-hidden rounded border border-white/10 bg-slate-950">
                <motion.div
                  className={fraction >= 1 ? 'h-full bg-emerald-400' : 'h-full bg-yellow-300'}
                  initial={{ width: 0 }}
                  animate={{ width: `${fraction * 100}%` }}
                  transition={{ type: 'spring', stiffness: 180, damping: 24 }}
                />
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export const MemoizedFractionalKnapsackView = React.memo(FractionalKnapsackView);
