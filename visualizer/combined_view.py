import matplotlib.pyplot as plt
import networkx as nx
import math
from algorithms.recurrence_info import RECURRENCES, DP_FORMULAS, ALGO_METADATA
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

def animate_execution(events, tracker=None):
    if not events: return
    
    has_dp = any(
        e.get("type") == "phase" and ("table" in e.get("details", {}) or "dp" in e.get("details", {}))
        for e in events
    )
    is_dp_only = events[0]["func"] in ["knapsack", "lis", "lcs"]
    is_fw = events[0]["func"] == "floyd_warshall"
    is_dijkstra = events[0]["func"] == "dijkstra"
    is_kruskal = events[0]["func"] == "kruskal"
    is_prim = events[0]["func"] == "prim"
    is_fk = events[0]["func"] == "fractionalKnapsack"
    is_tsp = events[0]["func"] == "tsp"

    
    fig = plt.figure(figsize=(13,7))
    dp_table = None
    dp_cell = None
    ax_info = None
    dp_dependencies = []

    board_state = None
    is_nqueens = events[0]["func"] == "nQueens"
    is_obst = events[0]["func"] == "obst"
    current_cell = None
    invalid_cell = None
    active_edge = None
    dijkstra_pq = []

    # MST specific (Kruskal/Prim)
    mst_edges = []
    mst_active = None
    mst_reject = None
    mst_parent = []
    kruskal_sorted = []

    # Fractional Knapsack specific
    fk_items = []
    fk_capacity = 0
    fk_current_w = 0
    fk_selected = []
    fk_active_id = None
    
    # TSP specific
    tsp_n = 0
    tsp_coords = []
    tsp_path = []
    tsp_cost = 0
    tsp_best_path = []
    tsp_best_cost = float('inf')
    tsp_active_id = -1

    
    if is_nqueens:
        gs = GridSpec(2,2, width_ratios=[1,2.8], height_ratios=[1,1], figure=fig)
        ax_stack = fig.add_subplot(gs[0,0])
        ax_board = fig.add_subplot(gs[1,0])
        ax_tree = fig.add_subplot(gs[:,1])
        ax_dp = None
        ax_info = ax_board # Reuse board area for messages if needed, but we'll add text on top
    elif is_dp_only and not is_obst:
        # Knapsack, LCS, LIS: Table (Left) + Info (Right)
        gs = GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1], figure=fig)
        ax_dp = fig.add_subplot(gs[:, 0])
        ax_info = fig.add_subplot(gs[:, 1])
        ax_dp.set_facecolor("#fafafa")
        ax_stack = None
        ax_tree = None
    elif is_kruskal:
        # Kruskal: Graph (Left) + Info (Right)
        gs = GridSpec(1, 2, width_ratios=[2, 1], figure=fig)
        ax_tree = fig.add_subplot(gs[0, 0])
        ax_info = fig.add_subplot(gs[0, 1])
        ax_dp = None
        ax_stack = None
    elif is_fw or is_dijkstra or is_prim:
        # Graph + Table: Graph (Left) + Table/Info (Right)
        gs = GridSpec(2, 2, width_ratios=[1.8, 1], height_ratios=[1, 1], figure=fig)
        ax_tree = fig.add_subplot(gs[:, 0])
        ax_dp = fig.add_subplot(gs[0, 1])
        ax_info = fig.add_subplot(gs[1, 1])
        ax_stack = None
        ax_dp.set_facecolor("#fafafa")
    elif is_obst or (has_dp and not is_dp_only):
        # Recursive DP: Table (Left) + Tree/Info (Right)
        gs = GridSpec(2, 2, width_ratios=[1, 1.2], height_ratios=[1.2, 1], figure=fig)
        ax_dp = fig.add_subplot(gs[:, 0])
        ax_tree = fig.add_subplot(gs[0, 1])
        ax_info = fig.add_subplot(gs[1, 1])
        ax_stack = None
        ax_dp.set_facecolor("#fafafa")
    elif is_fk:
        # Fractional Knapsack: Table (Left) + Meter (Top Right) + Info (Bottom Right)
        gs = GridSpec(2, 2, width_ratios=[1.5, 1], height_ratios=[0.6, 1.4], figure=fig)
        ax_dp = fig.add_subplot(gs[:, 0]) # Table
        ax_stack = fig.add_subplot(gs[0, 1]) # Meter
        ax_info = fig.add_subplot(gs[1, 1]) # Text
        ax_tree = None
    elif is_tsp:
        # TSP: Graph (Left) + Info (Right)
        gs = GridSpec(2, 2, width_ratios=[1.5, 1], height_ratios=[1, 1], figure=fig)
        ax_tree = fig.add_subplot(gs[:, 0]) # Graph
        ax_dp = None
        ax_stack = None
        ax_info = fig.add_subplot(gs[:, 1]) # Info
    else:
        # Generic Recursion: Stack (Left) + Tree (Right) + Info (Bottom)
        gs = GridSpec(2, 2, width_ratios=[1, 2], height_ratios=[2, 1], figure=fig)
        ax_stack = fig.add_subplot(gs[0, 0])
        ax_tree = fig.add_subplot(gs[0, 1])
        ax_info = fig.add_subplot(gs[1, :])
        ax_dp = None

    call_id_stack = []
    node_result = {}
    node_original = {}
    stack = []
    # G = nx.DiGraph() # Initialized later
    labels = {}
    node_status = {}

    step_index = next((i for i, e in enumerate(events) if e["type"] == "call"), 0)
    algo_name = events[0]["func"] if events else ""
    recurrence_text = RECURRENCES.get(algo_name, "")
    dp_formula = DP_FORMULAS.get(algo_name, "")

    bottom_text = []
    if recurrence_text: bottom_text.append(f"Logic: {recurrence_text}")
    if dp_formula:
        clean_formula = dp_formula.replace("\n", " | ")
        bottom_text.append(f"Formula: {clean_formula}")
    
    if bottom_text:
        fig.text(0.5, 0.02, "\n".join(bottom_text), ha="center", va="bottom", fontsize=10, color="#1565c0", wrap=True)
        fig.subplots_adjust(bottom=0.15)

    def draw_step():
        nonlocal stack, labels, node_status, dp_table, board_state, current_cell, invalid_cell, ax_info, dp_dependencies, dp_cell, active_edge, dijkstra_pq
        nonlocal mst_edges, mst_active, mst_reject, mst_parent, kruskal_sorted
        nonlocal fk_items, fk_capacity, fk_current_w, fk_selected, fk_active_id
        nonlocal tsp_n, tsp_coords, tsp_path, tsp_cost, tsp_best_path, tsp_best_cost, tsp_active_id

        tsp_n = 0
        tsp_coords = []
        tsp_path = []
        tsp_cost = 0
        tsp_best_path = []
        tsp_best_cost = float('inf')
        tsp_active_id = -1


        call_id_stack.clear()
        if ax_stack: ax_stack.clear()
        if ax_tree: ax_tree.clear()
        if ax_dp: ax_dp.clear()
        if ax_info: ax_info.clear()

        def get_dp_table(det):
            return det.get("table", det.get("dp"))

        stack = []
        G = nx.Graph() if (is_kruskal or is_prim) else nx.DiGraph()
        labels = {}
        node_status = {}
        mst_edges = []
        message = ""
        phase = None
        active_call_id = None

        for i in range(step_index + 1):
            event = events[i]
            if event["type"] == "call":
                args = list(event["args"].values())[0] if event["args"] else ""
                func = f"row={args}" if event['func'] == "nQueens" else f"{event['func']}({args})"
                stack.append(func)
                call_id_stack.append(event["id"])
                active_call_id = call_id_stack[-1]
                G.add_node(event["id"])
                labels[event["id"]] = f"[{event['args']['low']}, {event['args']['high']}]" if event["func"] == "binarySearch" else func
                node_original[event["id"]] = args
                node_result[event["id"]] = None
                node_status[event["id"]] = "normal"
                if event["parent"] is not None: G.add_edge(event["parent"], event["id"])
                message = f"Calling {func}"

            elif event["type"] == "return":
                call_id = event["id"]
                result = event["value"]
                if stack: stack.pop()
                if call_id_stack: call_id_stack.pop()
                active_call_id = call_id_stack[-1] if call_id_stack else None
                node_status[call_id] = "done"
                node_result[call_id] = result
                message = f"Return -> {result}"

            elif event["type"] == "phase":
                details = event.get("details", {})
                dp_table = details.get("table", details.get("dp", dp_table))
                phase = event["phase"]
                if active_call_id is None and not (is_kruskal or is_prim) and phase != "init_graph": continue

                if phase == "init_graph":
                    message = "Initializing Graph Representation"
                    if algo_name in ["floyd_warshall", "dijkstra", "kruskal", "prim"]:
                        G.clear()
                        V = details.get("V", 0)
                        edges = details.get("edges", [])
                        for v in range(V):
                            G.add_node(v); labels[v] = str(v); node_status[v] = "normal"
                        for u, v, w in edges:
                            G.add_edge(u, v, weight=w)
                    if is_kruskal or is_prim: mst_parent = details.get("parent", [])

                elif phase == "sort_edges" and is_kruskal:
                    kruskal_sorted = details["sorted"]
                    mst_parent = details["parent"]
                    sorted_str = "\n".join([f"({u},{v}) w={w}" for u,v,w in kruskal_sorted[:5]])
                    if len(kruskal_sorted) > 5: sorted_str += "\n..."
                    message = f"SORTING EDGES (Greedy Choice):\n{sorted_str}"

                elif phase == "check_edge" and (is_kruskal or is_prim):
                    u, v, w = details["u"], details["v"], details["w"]
                    mst_active = (u,v); mst_reject = None; mst_parent = details["parent"]; mst_edges = details.get("mst", [])
                    message = f"CHECKING EDGE: {u} -- {v} (weight {w})\nDoes this form a cycle (Kruskal) or min weight (Prim)?"

                elif phase == "accept_edge" and is_kruskal:
                    u, v, w = details["u"], details["v"], details["w"]
                    mst_active = None; mst_reject = None; mst_parent = details["parent"]; mst_edges = details["mst"]
                    message = f"ACCEPTED: {u} -- {v}\nMerging components using Union-Find."

                elif phase == "reject_edge" and is_kruskal:
                    u, v, w = details["u"], details["v"], details["w"]
                    mst_active = None; mst_reject = (u,v); mst_parent = details["parent"]; mst_edges = details["mst"]
                    message = f"REJECTED: {u} -- {v}\nCycle Detected! Already in same component."

                elif phase == "mst_complete":
                    mst_parent = details["parent"]; mst_edges = details.get("mst", []); mst_active = None; mst_reject = None
                    message = f"MST DONE!\nTotal weight: {details.get('mst_weight', details.get('weight', '?'))}"

                elif phase == "visit_node":
                    if is_prim:
                        u = details["u"]; mst_active = None; dijkstra_pq = details.get("pq", [])
                        message = f"VISITING NODE: {u}\nShortest edge to MST: {details.get('weight', 0)}"
                        mst_parent = details.get("parent", [])
                        # Mark visited for coloring
                        for i, v_s in enumerate(details["visited"]): node_status[i] = "done" if v_s else "normal"
                        node_status[u] = "explore"
                        # Reconstruct MST edges from parent array for visited nodes
                        mst_edges = []
                        for i, p in enumerate(mst_parent):
                            if p is not None and details["visited"][i]: mst_edges.append((i, p))
                    elif is_dijkstra:
                        u = details["u"]; active_edge = None; dijkstra_pq = details.get("pq", [])
                        message = f"VISITING NODE: {u}\nMin dist in PQ: {details['dist_u']}"
                        for i, v_s in enumerate(details["visited"]): node_status[i] = "done" if v_s else "normal"
                        node_status[u] = "explore"
                
                elif is_tsp:
                    tsp_n = details.get("n", tsp_n)
                    tsp_coords = details.get("coords", tsp_coords)
                    tsp_path = details.get("current_path", tsp_path)
                    tsp_cost = details.get("current_cost", tsp_cost)
                    tsp_best_path = details.get("best_path", tsp_best_path)
                    tsp_best_cost = details.get("best_cost", tsp_best_cost)
                    tsp_active_id = details.get("active_id", tsp_active_id)
                    
                    p_str = " -> ".join(map(str, tsp_path))
                    message = f"PHASE: {phase.upper()}\nPath: [{p_str}]\nCost: {tsp_cost:.1f}\nBest: {tsp_best_cost:.1f}"

                elif phase == "relax_edge":
                    if is_prim:
                        u, v, w = details["u"], details["v"], details["w"]
                        active_edge = (u,v); dijkstra_pq = details.get("pq", [])
                        message = f"RELAXING EDGE: {u} -- {v}\nWeight {w} < current dist[{v}] ({details['dist_v']})?"
                        node_status[v] = "split"
                    elif is_dijkstra:
                        u, v, w = details["u"], details["v"], details["w"]
                        active_edge = (u,v); dijkstra_pq = details.get("pq", [])
                        message = f"RELAXING: {u}->{v}\n{details['dist_u']} + {w} < {details['dist_v']}?"
                        node_status[v] = "split"

                elif phase == "update_dist":
                    if is_prim:
                        v, new_dist = details["v"], details["new_dist"]
                        active_edge = None; dijkstra_pq = details.get("pq", [])
                        message = f"✅ UPDATE! New edge to node {v} has weight {new_dist}"
                        node_status[v] = "solution"
                    elif is_dijkstra:
                        v, new_dist = details["v"], details["new_dist"]
                        active_edge = None; dijkstra_pq = details.get("pq", [])
                        message = f"✅ UPDATE! New dist[{v}] = {new_dist}"; node_status[v] = "solution"

                elif phase == "divide":
                    node_status[active_call_id] = "split"
                    message = "Dividing subproblem"

                elif phase == "combine":
                    node_status[active_call_id] = "done"
                    message = f"Combining -> {details.get('result', '')}"

                elif phase == "explore" and is_nqueens:
                        board_state = details["board"]
                        current_cell = (details["row"], details["col"])
                        message = f"Trying Col {details['col']} for Row {details['row']}"
                
                elif phase == "invalid" and is_nqueens:
                    board_state = details["board"]
                    invalid_cell = (details["row"], details["col"])
                    message = f"❌ Conflict at ({details['row']},{details['col']})"

                elif phase == "consider_root" and is_obst:
                    i,j,k = details['i'], details['j'], details['k']
                    dp_cell = (i, j); dp_dependencies = [(i, k-1), (k+1, j)]
                    message = f"Trying root k={k} for range [{i}..{j}]\nCost = {details['left']} + {details['right']} + {details['weight']} = {details['cost']}"

                elif phase == "mid" and algo_name == "binarySearch":
                    low, high, mid = details['low'], details['high'], details['mid']
                    message = f"mid = ({low}+{high})//2 = {mid}\nValue = {details['value']}"

                elif phase == "update":
                    dp_table = get_dp_table(details)
                    if algo_name == "knapsack" and "w" in details:
                        i, w = details["i"], details["w"]; dp_cell = (i, w); dp_dependencies = [(i-1, w), (i-1, w-details.get("i_weight", 0))]
                        message = f"DP UPDATE: (i={i}, w={w})\nMax: {details.get('chosen', 0)}"
                    elif algo_name == "floyd_warshall":
                        i,j,k = details["i"], details["j"], details["k"]; dp_cell=(i,j); dp_dependencies=[(i,k),(k,j)]
                        message = f"FW UPDATE: dist[{i}][{j}] = {details['new_dist']}"; node_status[i] = "split"
                
                elif is_fk:
                    fk_items = details.get("items", [])
                    fk_capacity = details.get("W", fk_capacity)
                    fk_current_w = fk_capacity - details.get("currentW", fk_capacity) if "currentW" in details else fk_current_w
                    fk_selected = details.get("selected", [])
                    fk_active_id = details.get("active_id")
                    
                    if phase == "init": message = "Initializing Items & Ratios"
                    elif phase == "sort": message = "Greedy Step: Sorting by Value/Weight Ratio (Descending)"
                    elif phase == "check": message = f"Checking Item {fk_active_id}\nCan we add it?"
                    elif phase == "pick": message = f"Picked Item {fk_active_id} (Full)\nAdded {details.get('fraction', 1.0)*100}% of it."
                    elif phase == "pick_fraction": message = f"Picked Item {fk_active_id} (Fractional)\nFilled remaining {details.get('fraction', 0.0)*100:.1f}% space."
                    elif phase == "complete": message = f"COMPLETED!\nTotal Value: {details.get('totalV', 0.0):.2f}"

        # ---------- DRAWING ----------
        if ax_stack:
            for idx, frame in enumerate(reversed(stack)):
                ax_stack.text(0.5, idx, frame, ha='center', va='center', bbox=dict(boxstyle="round", facecolor="orange" if idx==0 else "lightblue"), fontsize=9)
            ax_stack.set_title("Call Stack", fontsize=10); ax_stack.axis('off')

        if ax_tree:
            edge_colors = []
            edge_widths = []
            for u, v in G.edges():
                if (u,v) == active_edge or (v,u) == active_edge: edge_colors.append("#ef5350"); edge_widths.append(4.0)
                elif is_kruskal or is_prim:
                    if (u,v) in [(m[0],m[1]) for m in mst_edges] or (v,u) in [(m[0],m[1]) for m in mst_edges]:
                        edge_colors.append("#43a047"); edge_widths.append(5.0)
                    elif (u,v) == mst_active or (v,u) == mst_active: edge_colors.append("#1e88e5"); edge_widths.append(5.0)
                    elif (u,v) == mst_reject or (v,u) == mst_reject: edge_colors.append("#e53935"); edge_widths.append(5.0)
                    else: edge_colors.append("#cfd8dc"); edge_widths.append(1.5)
                else: edge_colors.append("#cfd8dc"); edge_widths.append(1.5)

            pos = nx.circular_layout(G) if (is_fw or is_dijkstra or is_kruskal or is_prim) else hierarchy_layout(G, list(G.nodes)[0]) if G.nodes else {}
            if pos:
                v_count = len(G.nodes)
                n_size = 2200 if v_count < 6 else 1600 if v_count < 12 else 1000
                nx.draw_networkx_nodes(G, pos, ax=ax_tree, node_color=[( "#fff176" if node_status.get(n)=="split" else "#66bb6a" if node_status.get(n)=="solution" else "#81c784" if node_status.get(n)=="done" else "#64b5f6" if node_status.get(n)=="explore" else "#ef5350" if node_status.get(n)=="invalid" else "#90caf9") for n in G.nodes], node_size=n_size)
                nx.draw_networkx_labels(G, pos, labels={n: labels.get(n, str(n)) for n in G.nodes}, ax=ax_tree, font_size=9, font_weight='bold')
                nx.draw_networkx_edges(G, pos, ax=ax_tree, edge_color=edge_colors, width=edge_widths, arrows=not (is_kruskal or is_prim), alpha=0.8)
            if (is_fw or is_dijkstra or is_kruskal or is_prim) and pos:
                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax_tree, font_size=8)
            ax_tree.set_title("ALGORITHM VISUALIZATION", fontsize=11, fontweight='bold', pad=10)
            ax_tree.axis('off')

        if is_nqueens and ax_board:
            n = len(board_state) if board_state else 0
            for r in range(n):
                for c in range(n):
                    col = "#ef5350" if invalid_cell==(r,c) else "#f0d9b5" if (r+c)%2==0 else "#b58863"
                    ax_board.add_patch(plt.Rectangle((c,r), 1, 1, color=col))
                    if current_cell == (r,c): ax_board.add_patch(plt.Rectangle((c,r), 1, 1, fill=False, edgecolor="blue", linewidth=2))
                    if board_state[r] == c: ax_board.text(c+0.5, r+0.5, "Q", ha="center", va="center", fontsize=16, fontweight='bold')
            if n > 0:
                ax_board.set_xlim(0,n); ax_board.set_ylim(n,0)
            ax_board.axis('off')

        if is_tsp and ax_tree and tsp_coords:
            ax_tree.clear()
            ax_tree.set_title("TSP CITY GRAPH", fontsize=12, fontweight='bold', pad=15)
            
            # 1. Draw All Possible Edges (Light)
            for i in range(tsp_n):
                for j in range(i+1, tsp_n):
                    c1, c2 = tsp_coords[i], tsp_coords[j]
                    ax_tree.plot([c1[0], c2[0]], [c1[1], c2[1]], color='#eeeeee', lw=0.5, zorder=1)
            
            # 2. Draw Best Path Found So Far (Green)
            if len(tsp_best_path) > 1:
                for i in range(len(tsp_best_path)-1):
                    u, v = tsp_best_path[i], tsp_best_path[i+1]
                    c1, c2 = tsp_coords[u], tsp_coords[v]
                    ax_tree.plot([c1[0], c2[0]], [c1[1], c2[1]], color='#c8e6c9', lw=4, ls='--', zorder=2)

            # 3. Draw Current Exploration Path (Blue)
            if len(tsp_path) > 1:
                for i in range(len(tsp_path)-1):
                    u, v = tsp_path[i], tsp_path[i+1]
                    c1, c2 = tsp_coords[u], tsp_coords[v]
                    ax_tree.plot([c1[0], c2[0]], [c1[1], c2[1]], color='#1e88e5', lw=2.5, zorder=3)
            
            # 4. Draw Nodes
            for i, (x, y) in enumerate(tsp_coords):
                color = '#ffffff'
                edge = '#000000'
                if i == 0: color = '#fff9c4'; edge = '#fbc02d' # Start Node
                if i == tsp_active_id: color = '#ff8a65'; edge = '#e64a19' # Active
                
                ax_tree.scatter(x, y, s=500, color=color, edgecolor=edge, linewidth=2, zorder=5)
                ax_tree.text(x, y, str(i), ha='center', va='center', fontsize=12, fontweight='bold', zorder=6)

            ax_tree.axis('off')
            ax_tree.set_aspect('equal')

        if ax_dp and dp_table is not None:
            if isinstance(dp_table, list) and len(dp_table) > 0:
                data = dp_table if isinstance(dp_table[0], list) else [dp_table]
            else:
                data = [[str(dp_table)]]
            
            # Determine labels based on algorithm
            row_labels = None
            col_labels = None
            
            if algo_name == "knapsack":
                row_labels = [f"I{i}" for i in range(len(data))]
                col_labels = [str(j) for j in range(len(data[0]))]
            elif algo_name == "lcs":
                s1 = next((e["args"].get("s1", "") for e in events if e["func"] == "lcs"), "")
                s2 = next((e["args"].get("s2", "") for e in events if e["func"] == "lcs"), "")
                row_labels = ["Ø"] + list(s1)
                col_labels = ["Ø"] + list(s2)
            elif algo_name == "lis":
                col_labels = [str(i) for i in range(len(data[0]))]
                row_labels = ["Len"]
            elif algo_name in ["floyd_warshall", "obst"]:
                row_labels = [str(i) for i in range(len(data))]
                col_labels = [str(i) for i in range(len(data[0]))]
            elif algo_name in ["dijkstra", "prim"]:
                row_labels = ["W" if algo_name == "prim" else "D"]
                col_labels = [str(i) for i in range(len(data[0]))]

            tab = ax_dp.table(
                cellText=[["∞" if x==float('inf') else str(x) for x in row] for row in data],
                rowLabels=row_labels,
                colLabels=col_labels,
                loc='center', 
                cellLoc='center'
            )
            tab.auto_set_font_size(False); tab.set_fontsize(9)
            tab.scale(1.1, 1.8)
            
            if dp_cell:
                r, c = dp_cell
                if r < len(data) and c < len(data[0]): tab[(r, c)].set_facecolor("#fff176")
            for r, c in dp_dependencies:
                if 0 <= r < len(data) and 0 <= c < len(data[0]): tab[(r, c)].set_facecolor("#e3f2fd")
            ax_dp.set_title("STATE / DP TABLE", fontsize=10, fontweight='bold')
            ax_dp.axis('off')
            
        if is_fk and ax_dp:
            # Item Table
            table_data = []
            row_colors = []
            for it in fk_items:
                # Determine color
                color = "#ffffff"
                if it["id"] == fk_active_id: color = "#fff9c4" # Active
                elif any(s["id"] == it["id"] for s in fk_selected): color = "#c8e6c9" # Taken
                
                # Determine percentage taken
                sel = next((s for s in fk_selected if s["id"] == it["id"]), None)
                perc = round(sel["fraction"] * 100, 1) if sel else 0
                
                table_data.append([
                    f"Item {it['id']}",
                    f"{it['w']}",
                    f"{it['v']}",
                    f"{it['ratio']:.2f}",
                    f"{perc}%"
                ])
                row_colors.append(color)

            if table_data:
                tab = ax_dp.table(
                    cellText=table_data,
                    colLabels=["Item ID", "Weight", "Value", "Ratio (V/W)", "% Taken"],
                    loc="center",
                    cellLoc="center"
                )
                tab.auto_set_font_size(False)
                tab.set_fontsize(9)
                tab.scale(1.2, 2.5)
                # Apply row colors
                for i in range(len(table_data)):
                    for j in range(5):
                        tab[(i+1, j)].set_facecolor(row_colors[i])
                ax_dp.set_title("GREEDY ITEM SELECTION", fontsize=11, fontweight='bold')
                ax_dp.axis('off')
            else:
                ax_dp.clear()
                ax_dp.text(0.5, 0.5, "Initializing items...", ha="center", va="center", fontsize=12, color="gray")
                ax_dp.axis('off')

        # 4. Knapsack Meter (Top Right)
        if is_fk and ax_stack and fk_items:
            ax_stack.clear()
            ax_stack.set_title(f"Capacity Usage: {round(fk_current_w, 1)} / {fk_capacity}", pad=10)
            ax_stack.barh(0, fk_capacity, color="#eeeeee", height=0.4, label="Remaining Capacity")
            ax_stack.barh(0, fk_current_w, color="#4caf50", height=0.4, label="Filled")
            ax_stack.set_xlim(0, fk_capacity)
            ax_stack.set_yticks([])
            ax_stack.legend(loc="upper right", fontsize=8)

        if ax_info:
            ax_info.clear()
            # Fetch Metadata
            meta = ALGO_METADATA.get(events[0]["func"], {})
            name = meta.get("name", events[0]["func"].upper())
            complexity = meta.get("complexity", "N/A")
            formula = meta.get("formula", "N/A")
            
            # Phase Explanation
            phase_map = meta.get("phases", {})
            current_explanation = phase_map.get(phase, phase_map.get("default", f"Executing phase: {phase}")) if phase else "Initializing algorithm..."
            
            # 1. Header Information (Top Left)
            ax_info.text(0.01, 0.95, f"ALGORITHM: {name}\nCOMPLEXITY: {complexity}", 
                         fontsize=11, fontweight='bold', color="#1b5e20", va='top')
            
            # 2. Formula Box (Top Right)
            formula_text = f"MODEL / FORMULA:\n{formula}"
            ax_info.text(0.99, 0.95, formula_text, fontsize=10, fontweight='bold', color="#b71c1c", 
                         va='top', ha='right', bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffebee", alpha=0.8, edgecolor="#ef9a9a"))
            
            # 3. Dynamic Step Status (Center-Left)
            status_text = f"STEP {step_index + 1}: {message.upper()}\n\n➤ EXPLANATION: {current_explanation}"
            if (is_dijkstra or is_prim) and dijkstra_pq:
                status_text += "\n\nPRIORITY QUEUE: " + ", ".join([f"({w},{n})" for w,n in sorted(dijkstra_pq)])
            
            ax_info.text(0.01, 0.60, status_text, fontsize=11, wrap=True, va='top', fontfamily='sans-serif', 
                         bbox=dict(boxstyle="round,pad=0.5", facecolor="#fff9c4", alpha=0.9, edgecolor="#fbc02d"))

            # 4. Legend (Bottom Right)
            legend_elements = []
            if is_kruskal or is_prim: 
                legend_elements = [Patch(facecolor='#1e88e5', label='Active'), Patch(facecolor='#43a047', label='MST'), 
                                 Patch(facecolor='#e53935', label='Cycle'), Patch(facecolor='#cfd8dc', label='Other')]
            elif is_dijkstra: 
                legend_elements = [Patch(facecolor='#64b5f6', label='Current'), Patch(facecolor='#81c784', label='Done'), 
                                 Patch(facecolor='#fff176', label='Neighbor'), Patch(facecolor='#ef5350', label='Relaxing')]
            elif is_fw: 
                legend_elements = [Patch(facecolor='#fff176', label='Node I'), Patch(facecolor='#66bb6a', label='Node J'), 
                                 Patch(facecolor='#64b5f6', label='Node K')]
            
            if legend_elements: 
                ax_info.legend(handles=legend_elements, loc='lower right', title="Color Legend", fontsize=8, frameon=True)

            ax_info.axis("off")

        fig.suptitle(f"[Algorithm Step {step_index + 1}] - {algo_name.upper()}", fontsize=14, color="#2e7d32", fontweight='bold', y=0.98)
        plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.08, wspace=0.25, hspace=0.3)
        fig.canvas.draw_idle()

    def on_key(event):
        nonlocal step_index
        if event.key == " ": step_index = min(step_index + 1, len(events)-1); draw_step()
        elif event.key == "b": step_index = max(step_index - 1, 0); draw_step()
        elif event.key == "q": plt.close()

    fig.canvas.mpl_connect('key_press_event', on_key)
    draw_step()
    plt.show()

def hierarchy_layout(G, root, width=1., vert_gap=0.25, vert_loc=0, xcenter=0.5):
    pos = {root:(xcenter,vert_loc)}
    neighbors = list(G.neighbors(root))
    if neighbors:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos.update(hierarchy_layout(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx))
    return pos