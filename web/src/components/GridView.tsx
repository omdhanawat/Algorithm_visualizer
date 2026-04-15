import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Crown } from 'lucide-react';

interface GridViewProps {
  size: number;
  // representation: board[row] = col, if -1 then empty
  board: number[];
  activeRow?: number;
  activeCol?: number;
  isValid?: boolean;
}

export const GridView: React.FC<GridViewProps> = ({ 
  size, 
  board = [], 
  activeRow = -1, 
  activeCol = -1,
  isValid = true
}) => {
  if (size <= 0) return null;

  const rows = Array.from({ length: size }, (_, i) => i);
  const cols = Array.from({ length: size }, (_, i) => i);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-8 overflow-hidden z-10">
      <div 
        className="grid gap-[2px] bg-slate-700/50 p-2 rounded-xl shadow-2xl border border-slate-700" 
        style={{ gridTemplateColumns: `repeat(${size}, minmax(0, 1fr))` }}
      >
        {rows.map((row) => (
          cols.map((col) => {
            const isDark = (row + col) % 2 === 1;
            const hasQueen = board[row] === col;
            const isActive = row === activeRow && col === activeCol;

            let bgColor = isDark ? 'bg-slate-800' : 'bg-slate-300';
            
            if (isActive) {
               bgColor = isValid ? 'bg-yellow-400' : 'bg-red-500';
            } else if (hasQueen && row === activeRow) {
               // Showing currently evaluated queen that might be bad
               bgColor = isValid ? 'bg-blue-400' : 'bg-red-400';
            }

            return (
              <div 
                key={`${row}-${col}`} 
                className={`relative w-12 h-12 sm:w-16 sm:h-16 flex items-center justify-center transition-colors duration-300 ${bgColor}`}
              >
                <AnimatePresence>
                  {hasQueen && (
                    <motion.div
                      key={`queen-${row}-${col}`}
                      initial={{ scale: 0, opacity: 0, y: -20 }}
                      animate={{ scale: 1, opacity: 1, y: 0 }}
                      exit={{ scale: 0, opacity: 0 }}
                      transition={{ type: "spring", stiffness: 300, damping: 20 }}
                    >
                      <Crown className={`w-8 h-8 sm:w-10 sm:h-10 ${isActive && !isValid ? 'text-white' : (isDark ? 'text-amber-400' : 'text-slate-800')} drop-shadow-md`} />
                    </motion.div>
                  )}
                </AnimatePresence>
                
                {/* Highlight Overlay for Active Cell without queen */}
                {isActive && !hasQueen && (
                  <motion.div
                     initial={{ opacity: 0 }}
                     animate={{ opacity: 1 }}
                     className="absolute inset-0 bg-yellow-400/50 border-2 border-yellow-300 z-10"
                  />
                )}
              </div>
            );
          })
        ))}
      </div>
    </div>
  );
};

export const MemoizedGridView = React.memo(GridView);
