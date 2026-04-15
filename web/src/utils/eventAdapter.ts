export interface NormalizedIndices {
  i?: number | string | null;
  j?: number | string | null;
  k?: number | string | null;
}

export interface NormalizedValues {
  old?: any;
  new?: any;
}

export interface NormalizedVisuals {
  active_cells?: number[][] | number[];
  dependency_cells?: (number[][] | number[] | null)[];
  nodes?: number[];
  edges?: any[];
  active_edges?: number[][];
  active_node_id?: string | number;
  tree_nodes?: any[];
  [key: string]: any;
}

export interface NormalizedEvent {
  type: string;
  phase: string;
  message: string;
  indices: NormalizedIndices;
  values: NormalizedValues;
  visuals: NormalizedVisuals;
  state: any;
  raw: any; // Keep the original just in case
}

export function normalizeEvent(event: any): NormalizedEvent {
  const data = event.data || event.details || {};

  return {
    type: event.type || event.event || "unknown",
    phase: event.phase || "ongoing",
    message: event.message || "",
    indices: {
      i: event.i ?? data.i ?? null,
      j: event.j ?? data.j ?? null,
      k: event.k ?? data.k ?? null,
    },
    values: {
      old: event.old_val ?? event.data?.old ?? null,
      new: event.new_val ?? event.data?.new ?? event.data?.value ?? null,
    },
    visuals: event.visual || {},
    state: event.state || {},
    raw: event
  };
}
