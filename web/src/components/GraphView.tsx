import React, { useMemo, useRef } from 'react';
import { motion } from 'framer-motion';

interface Node {
  id: number;
  label?: string;
  value?: any;
  isVisited?: boolean;
  isActive?: boolean;
}

interface Edge {
  source: number | string;
  target: number | string;
  weight?: number;
  isActive?: boolean;
  isDependency?: boolean;
}

interface GraphViewProps {
  nodes: number[] | Node[];
  edges: Edge[];
  activeNodes?: number[];
  visitedNodes?: number[];
  activeEdges?: number[][]; // [[u, v]]
  dependencyEdges?: number[][];
}

const GraphViewComponent: React.FC<GraphViewProps> = ({
  nodes,
  edges,
  activeNodes = [],
  visitedNodes = [],
  activeEdges = [],
  dependencyEdges = []
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const visitedIds = useMemo(() => {
    if (!Array.isArray(visitedNodes)) return [];
    if (visitedNodes.some((value: any) => typeof value === 'boolean')) {
      return visitedNodes
        .map((value: any, idx: number) => value ? String(idx) : null)
        .filter(Boolean) as string[];
    }
    return visitedNodes.map(String);
  }, [visitedNodes]);

  // Normalize Nodes
  const normNodes = useMemo(() => {
    const providedNodes = nodes || [];
    const edgeNodes = (edges || []).flatMap((edge: any) => {
      const isArray = Array.isArray(edge);
      return [isArray ? edge[0] : edge.source, isArray ? edge[1] : edge.target];
    }).filter((node) => node !== undefined && node !== null);
    const resolvedNodes = providedNodes.length > 0 ? providedNodes : Array.from(new Set(edgeNodes));

    return resolvedNodes.map(n => {
      const id = String(typeof n === 'number' ? n : n.id);
      return {
        id,
        label: typeof n === 'object' ? n.label : `V${id}`,
        isActive: activeNodes.map(String).includes(id),
        isVisited: visitedIds.includes(id)
      };
    });
  }, [nodes, edges, activeNodes, visitedIds]);

  // Stable Circular Layout Logic
  const layout = useMemo(() => {
    const radius = 220; 
    const centerX = 400;
    const centerY = 300;
    const total = normNodes.length || 1;
    
    const nodeMap: Record<string, { x: number, y: number }> = {};
    normNodes.forEach((node, i) => {
      const angle = (i / total) * 2 * Math.PI - Math.PI / 2.5; 
      nodeMap[node.id] = {
        x: centerX + radius * Math.cos(angle),
        y: centerY + radius * Math.sin(angle)
      };
    });
    return nodeMap;
  }, [normNodes]);

  // Normalize Edges with active/dependency state
  const normEdges = useMemo(() => {
    return (edges || []).map((edge: any) => {
      const isArray = Array.isArray(edge);
      const s = String(isArray ? edge[0] : edge.source);
      const t = String(isArray ? edge[1] : edge.target);
      const weight = isArray ? edge[2] : edge.weight;
      
      const isActive = activeEdges.some(ae => 
        (String(ae[0]) === s && String(ae[1]) === t) ||
        (String(ae[0]) === t && String(ae[1]) === s)
      );
      const isDependency = dependencyEdges.some(de => 
        (String(de[0]) === s && String(de[1]) === t) ||
        (String(de[0]) === t && String(de[1]) === s)
      );
      return { ...(isArray ? {} : edge), source: s, target: t, weight, isActive, isDependency };
    });
  }, [edges, activeEdges, dependencyEdges]);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center z-10 overflow-hidden">
      <svg 
        ref={svgRef} 
        viewBox="0 0 800 600" 
        className="w-full h-full max-w-4xl"
      >
        <defs>
          <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
          </filter>
          <marker id="arrowhead-default" markerWidth="10" markerHeight="7" refX="25" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#1e293b" opacity="0.8" />
          </marker>
          <marker id="arrowhead-active" markerWidth="10" markerHeight="7" refX="25" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee" />
          </marker>
          <marker id="arrowhead-dep" markerWidth="10" markerHeight="7" refX="25" refY="3.5" orient="auto">
            <polygon points="0 0, 10 3.5, 0 7" fill="#6366f1" />
          </marker>
        </defs>

        {/* Edges */}
        {normEdges.map((edge, i) => {
          const start = layout[edge.source];
          const end = layout[edge.target];
          if (!start || !end) return null;

          const strokeColor = edge.isActive ? "#22d3ee" : (edge.isDependency ? "#6366f1" : "#1e293b");
          const markerEnd = edge.isActive ? "url(#arrowhead-active)" : (edge.isDependency ? "url(#arrowhead-dep)" : "url(#arrowhead-default)");

          return (
            <g key={`edge-${i}`}>
              <line
                x1={start.x} y1={start.y}
                x2={end.x} y2={end.y}
                stroke={strokeColor}
                strokeWidth={edge.isActive || edge.isDependency ? 3 : 1.5}
                markerEnd={markerEnd}
                className="transition-all duration-300"
              />
              {edge.weight !== undefined && (
                <text
                  x={(start.x + end.x) / 2}
                  y={(start.y + end.y) / 2 - 10}
                  fill={edge.isActive ? "#22d3ee" : "#475569"}
                  className="text-[10px] font-black font-mono select-none uppercase tracking-tighter"
                  textAnchor="middle"
                >
                  {edge.weight}
                </text>
              )}
              {/* Traveling Glow for Active Edges */}
              {(edge.isActive || edge.isDependency) && (
                <motion.circle
                  r={3}
                  fill={strokeColor}
                  initial={{ cx: start.x, cy: start.y }}
                  animate={{ cx: end.x, cy: end.y }}
                  transition={{ duration: 1.2, repeat: Infinity, ease: "linear" }}
                  filter="url(#glow)"
                />
              )}
            </g>
          );
        })}

        {/* Nodes */}
        {normNodes.map((node) => {
          const pos = layout[node.id];
          if (!pos) return null;
          const { x, y } = pos;
          return (
            <g key={`node-${node.id}`}>
              {node.isActive && (
                <motion.circle
                  cx={x} cy={y} r={28}
                  fill="rgba(34, 211, 238, 0.2)"
                  initial={{ scale: 0.8 }}
                  animate={{ scale: 1.2 }}
                  transition={{ repeat: Infinity, duration: 1.5, repeatType: "reverse" }}
                  className="blur-md"
                />
              )}
              <motion.circle
                cx={x} cy={y} r={22}
                initial={false}
                animate={{
                  fill: node.isActive ? "#083344" : (node.isVisited ? "#064e3b" : "#0f172a"),
                  stroke: node.isActive ? "#22d3ee" : (node.isVisited ? "#10b981" : "#1e293b"),
                  strokeWidth: node.isActive ? 3 : 2,
                  scale: node.isActive ? 1.05 : 1
                }}
                className="cursor-default drop-shadow-2xl"
              />
              <text
                x={x} y={y}
                dy=".35em"
                textAnchor="middle"
                className={`text-[10px] font-black uppercase tracking-widest select-none font-mono ${node.isActive ? 'fill-cyan-300' : (node.isVisited ? 'fill-emerald-400' : 'fill-slate-400')}`}
              >
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export const MemoizedGraphView = React.memo(GraphViewComponent);
