import React, { useState, useEffect } from 'react';
import { RefreshCcw, Settings2 } from 'lucide-react';

interface FieldDef {
  name: string;
  label: string;
  type: 'number' | 'text' | 'array' | 'edges' | 'matrix';
  defaultValue: any;
}

const ALGO_FIELDS: Record<string, FieldDef[]> = {
  fib: [{ name: 'n', label: 'N (Fibonacci Number)', type: 'number', defaultValue: 5 }],
  fibDP: [{ name: 'n', label: 'N (Fibonacci Number)', type: 'number', defaultValue: 8 }],
  nQueens: [{ name: 'n', label: 'Board Size (N x N)', type: 'number', defaultValue: 4 }],
  mergeSort: [{ name: 'arr', label: 'Array (comma-separated)', type: 'array', defaultValue: '5, 2, 8, 1, 9' }],
  quickSort: [{ name: 'arr', label: 'Array (comma-separated)', type: 'array', defaultValue: '5, 2, 8, 1, 9' }],
  lis: [{ name: 'arr', label: 'Array (comma-separated)', type: 'array', defaultValue: '10, 22, 9, 33, 21, 50, 41, 60' }],
  binarySearch: [
     { name: 'arr', label: 'Sorted Array', type: 'array', defaultValue: '1, 3, 5, 8, 12, 15, 18, 21, 25' },
     { name: 'target', label: 'Target', type: 'number', defaultValue: 18 }
  ],
  knapsack: [
     { name: 'weights', label: 'Weights', type: 'array', defaultValue: '2, 3, 4, 5' },
     { name: 'values', label: 'Values', type: 'array', defaultValue: '3, 4, 5, 8' },
     { name: 'capacity', label: 'Capacity', type: 'number', defaultValue: 8 }
  ],
  fractionalKnapsack: [
     { name: 'weights', label: 'Weights', type: 'array', defaultValue: '10, 20' },
     { name: 'values', label: 'Values', type: 'array', defaultValue: '60, 100' },
     { name: 'capacity', label: 'Capacity', type: 'number', defaultValue: 50 }
  ],
  lcs: [
     { name: 'X', label: 'String X', type: 'text', defaultValue: 'AGGTAB' },
     { name: 'Y', label: 'String Y', type: 'text', defaultValue: 'GXTXAYB' }
  ],
  obst: [
     { name: 'keys', label: 'Keys (must be sorted)', type: 'array', defaultValue: '10, 12, 20' },
     { name: 'freq', label: 'Frequencies', type: 'array', defaultValue: '34, 8, 50' }
  ],
  dijkstra: [
     { name: 'V', label: 'Vertices Count', type: 'number', defaultValue: 6 },
     { name: 'source', label: 'Source Node', type: 'number', defaultValue: 0 },
     { name: 'edges', label: 'Edges (u, v, w per line)', type: 'edges', defaultValue: '0,1,7\n0,2,9\n0,5,14\n1,2,10\n1,3,15\n2,3,11\n2,5,2\n3,4,6\n4,5,9' }
  ],
  prim: [
     { name: 'V', label: 'Vertices Count', type: 'number', defaultValue: 6 },
     { name: 'source', label: 'Source Node', type: 'number', defaultValue: 0 },
     { name: 'edges', label: 'Edges (u, v, w per line)', type: 'edges', defaultValue: '0,1,4\n0,2,3\n1,2,1\n1,3,2\n2,3,4\n3,4,2\n4,5,6' }
  ],
  kruskal: [
     { name: 'V', label: 'Vertices Count', type: 'number', defaultValue: 6 },
     { name: 'edges', label: 'Edges (u, v, w per line)', type: 'edges', defaultValue: '0,1,4\n0,2,3\n1,2,1\n1,3,2\n2,3,4\n3,4,2\n4,5,6' }
  ],
  floyd_warshall: [
     { name: 'V', label: 'Vertices Count', type: 'number', defaultValue: 4 },
     { name: 'edges', label: 'Edges (u, v, w per line)', type: 'edges', defaultValue: '0,1,5\n0,3,10\n1,2,3\n2,3,1' }
  ],
  tsp: [
     { name: 'n', label: 'Cities Count', type: 'number', defaultValue: 3 },
     { name: 'distMatrix', label: 'Distance Matrix (Row per line)', type: 'matrix', defaultValue: '0, 2, 9\n2, 0, 6\n9, 6, 0' }
  ]
};

interface ParameterFormProps {
  algoId: string;
  onRun: (params: any) => void;
  onCancel: () => void;
}

export const ParameterForm: React.FC<ParameterFormProps> = ({ algoId, onRun, onCancel }) => {
  const fields = ALGO_FIELDS[algoId] || [];
  const [formData, setFormData] = useState<Record<string, string>>({});

  // Initialize defaults
  useEffect(() => {
    const initial: Record<string, string> = {};
    fields.forEach(f => {
      initial[f.name] = String(f.defaultValue);
    });
    setFormData(initial);
  }, [algoId, fields]);

  const handleChange = (name: string, value: string) => {
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const parseParams = () => {
    const parsed: Record<string, any> = {};
    for (const field of fields) {
      const val = formData[field.name];
      if (val === undefined || val === '') continue;

      if (field.type === 'number') {
        parsed[field.name] = parseInt(val, 10);
      } else if (field.type === 'text') {
        parsed[field.name] = val;
      } else if (field.type === 'array') {
        parsed[field.name] = val.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
      } else if (field.type === 'edges' || field.type === 'matrix') {
        parsed[field.name] = val.split('\n').map(line => 
          line.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n))
        ).filter(row => row.length > 0);
      }
    }
    return parsed;
  };

  const handleRun = () => {
    const parsed = parseParams();
    onRun(parsed);
  };

  if (fields.length === 0) return null;

  return (
    <div className="absolute top-2 right-2 z-50 bg-[#0f172a]/95 backdrop-blur-xl border border-slate-700 shadow-2xl shadow-indigo-900/20 rounded-2xl p-6 w-96 max-h-[80vh] overflow-y-auto custom-scrollbar">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg">
          <Settings2 className="w-5 h-5" />
        </div>
        <h3 className="text-xl font-bold text-slate-100">Parameters</h3>
      </div>

      <div className="flex flex-col gap-5">
        {fields.map(f => (
          <div key={f.name} className="flex flex-col gap-1.5">
            <label className="text-xs font-bold text-slate-400 tracking-wider uppercase">
              {f.label}
            </label>
            
            {f.type === 'edges' || f.type === 'matrix' ? (
              <textarea 
                value={formData[f.name] || ''}
                onChange={e => handleChange(f.name, e.target.value)}
                className="w-full h-32 bg-[#020617] border border-slate-700/80 rounded-xl px-4 py-3 font-mono text-sm text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 placeholder-slate-700 resize-none transition-all"
                spellCheck="false"
              />
            ) : (
              <input 
                type="text"
                value={formData[f.name] || ''}
                onChange={e => handleChange(f.name, e.target.value)}
                className="w-full bg-[#020617] border border-slate-700/80 rounded-xl px-4 py-2.5 font-mono text-sm text-slate-200 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none transition-all"
              />
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-3 justify-end mt-8 border-t border-slate-800 pt-5">
        <button 
          onClick={onCancel}
          className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
        >
          Cancel
        </button>
        <button 
          onClick={handleRun}
          className="flex items-center gap-2 px-5 py-2 text-sm font-bold text-white bg-indigo-600 hover:bg-indigo-500 shadow-lg shadow-indigo-600/20 rounded-lg transition-all active:scale-95"
        >
          <RefreshCcw className="w-4 h-4" />
          Update Output
        </button>
      </div>
    </div>
  );
};
