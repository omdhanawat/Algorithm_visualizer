import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface TreeNode {
  id: string;
  label: string;
  detail?: string;
  children?: string[];
  isActive?: boolean;
  isResult?: boolean;
  value?: any;
}

interface TreeViewProps {
  nodes: TreeNode[];
  activeId?: string;
  rootId?: string;
  activeEdges?: { from: string, to: string }[];
}

const TreeViewComponent: React.FC<TreeViewProps> = ({
  nodes,
  activeId,
  rootId,
  activeEdges = []
}) => {
  // Simple hierarchical layout helper
  const layout = useMemo(() => {
    const coords: Record<string, { x: number, y: number }> = {};
    const levels: Record<number, string[]> = {};
    const nodeMap = new Map(nodes.map(n => [n.id, n]));
    
    const visited = new Set<string>();
    const calculateDepth = (id: string, depth: number) => {
      if (visited.has(id)) return;
      visited.add(id);
      
      if (!levels[depth]) levels[depth] = [];
      if (!levels[depth].includes(id)) {
        levels[depth].push(id);
      }
      const node = nodeMap.get(id);
      node?.children?.forEach(childId => calculateDepth(childId, depth + 1));
    };

    if (rootId) calculateDepth(rootId, 0);
    else if (nodes.length > 0) calculateDepth(nodes[0].id, 0);

    const canvasWidth = 1200;
    const canvasHeight = 760;
    const totalLevels = Object.keys(levels).length || 1;
    const verticalGap = canvasHeight / (totalLevels + 1);

    Object.entries(levels).forEach(([lvl, ids]) => {
      const depth = parseInt(lvl);
      const horizontalGap = canvasWidth / (ids.length + 1);
      ids.forEach((id, i) => {
        coords[id] = {
          x: horizontalGap * (i + 1),
          y: verticalGap * (depth + 1)
        };
      });
    });

    return coords;
  }, [nodes, rootId]);

  const edges = useMemo(() => {
    const result: { from: string, to: string, isActive: boolean }[] = [];
    nodes.forEach(node => {
      node.children?.forEach(childId => {
        const isActive = activeEdges.some(e => 
            (e.from === node.id && e.to === childId) || 
            (e.from === childId && e.to === node.id)
        );
        result.push({ from: node.id, to: childId, isActive });
      });
    });
    return result;
  }, [nodes, activeEdges]);

    return (
    <div className="w-full h-full flex flex-col items-center justify-center p-2 overflow-auto z-10">
      <svg viewBox="0 0 1200 760" className="w-full h-full min-w-[860px]">
        <defs>
          <filter id="nodeGlow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
        </defs>

        {/* Connections */}
        {edges.map((edge, i) => {
          const start = layout[edge.from];
          const end = layout[edge.to];
          if (!start || !end) return null;
          return (
            <motion.line
              key={`edge-${i}`}
              x1={start.x} y1={start.y}
              x2={end.x} y2={end.y}
              stroke={edge.isActive ? "#22d3ee" : "#1e293b"} 
              strokeWidth={edge.isActive ? 2 : 1}
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 1 }}
              transition={{ duration: 0.5 }}
            />
          );
        })}

        {/* Nodes */}
        {nodes.map(node => {
          const pos = layout[node.id];
          if (!pos) return null;
          const isActive = node.id === activeId || node.isActive;
          const isResult = node.isResult;
          
          // Responsive node size based on label length
          const nodeWidth = Math.max(130, Math.min(320, Math.max(node.label.length, node.detail?.length || 0) * 7 + 28));
          const nodeHeight = node.detail ? 64 : 48;

          return (
            <g key={node.id}>
              {/* Glow Effect for Active Node */}
              {isActive && (
                <motion.rect
                  x={pos.x - nodeWidth/2 - 4} y={pos.y - nodeHeight/2 - 4}
                  width={nodeWidth + 8} height={nodeHeight + 8}
                  rx={14} ry={14}
                  fill="rgba(34, 211, 238, 0.2)"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ repeat: Infinity, duration: 2, repeatType: "reverse" }}
                  className="blur-md"
                />
              )}

              {/* Node Body */}
              <motion.rect
                x={pos.x - nodeWidth/2} y={pos.y - nodeHeight/2}
                width={nodeWidth} height={nodeHeight}
                rx={12} ry={12}
                initial={{ scale: 0 }}
                animate={{ 
                  scale: 1,
                  fill: isActive ? "#083344" : "#0f172a",
                  stroke: isActive ? "#22d3ee" : (isResult ? "#22c55e" : "#1e293b"),
                  strokeWidth: isActive ? 2 : 1.5
                }}
                className="drop-shadow-2xl cursor-pointer"
              />

              {/* Node Label (Function Call) */}
              <text
                x={pos.x} y={node.detail ? pos.y - 9 : pos.y}
                textAnchor="middle"
                dy=".35em"
                className={`text-[13px] font-black font-mono select-none pointer-events-none tracking-tight ${isActive ? 'fill-cyan-300' : (isResult ? 'fill-green-400' : 'fill-slate-200')}`}
              >
                {node.label}
              </text>
              {node.detail && (
                <text
                  x={pos.x}
                  y={pos.y + 14}
                  textAnchor="middle"
                  dy=".35em"
                  className="text-[10px] font-bold font-mono select-none pointer-events-none fill-slate-400"
                >
                  {node.detail.length > 42 ? `${node.detail.slice(0, 39)}...` : node.detail}
                </text>
              )}

              {/* Result Value Badge */}
              {node.value !== undefined && (
                <g transform={`translate(${pos.x + nodeWidth/2 - 10}, ${pos.y - nodeHeight/2})`}>
                  <circle r={10} fill="#22c55e" className="drop-shadow" />
                  <text
                    textAnchor="middle"
                    dy=".35em"
                    className="text-[9px] font-black fill-white"
                  >
                    {typeof node.value === 'object' ? '✓' : String(node.value)}
                  </text>
                </g>
              )}
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export const MemoizedTreeView = React.memo(TreeViewComponent);
