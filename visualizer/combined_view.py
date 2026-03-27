import matplotlib.pyplot as plt
import networkx as nx
from algorithms.recurrence_info import RECURRENCES, DP_FORMULAS
from matplotlib.gridspec import GridSpec

def animate_execution(events, tracker=None):
    
    has_dp = any(
        e.get("type") == "phase" and ("table" in e.get("details", {}) or "dp" in e.get("details", {}))
        # e.get("phase") in ["dp_update", "update", "skip"]
        for e in events
    )
    is_dp_only = events[0]["func"] in ["knapsack", "lis", "lcs"]
    fig = plt.figure(figsize=(13,7))
    dp_table = None   # ← ALWAYS defined
    dp_cell = None
    ax_info = None
    dp_dependencies = []

    board_state = None
    is_nqueens = events[0]["func"] == "nQueens"
    is_obst = events[0]["func"] == "obst"
    current_cell = None
    invalid_cell = None
   
    
    if is_nqueens:

        gs = GridSpec(
            2,2,
            width_ratios=[1,2.8],
            height_ratios=[1,1],
            figure=fig
        )

        ax_stack = fig.add_subplot(gs[0,0])
        ax_board = fig.add_subplot(gs[1,0])
        ax_tree = fig.add_subplot(gs[:,1])
        ax_dp = None

    elif is_dp_only and not is_obst:
        gs = GridSpec(1,2, width_ratios=[2,1], figure=fig)
        ax_dp = fig.add_subplot(gs[0,0])
        ax_info = fig.add_subplot(gs[0,1])
        ax_dp.set_facecolor("#fafafa")
        ax_stack = None
        ax_tree = None
        
    elif is_obst:
        gs = GridSpec(2, 2, width_ratios=[1.2, 1], height_ratios=[1.5, 1], figure=fig)
        ax_dp = fig.add_subplot(gs[:, 0])
        ax_tree = fig.add_subplot(gs[0, 1])
        ax_info = fig.add_subplot(gs[1, 1])
        ax_stack = None
        ax_dp.set_facecolor("#fafafa")

    elif has_dp and not is_dp_only:
        gs = GridSpec(
            2,2,
            width_ratios=[1,2.2],
            height_ratios=[1,1],
            figure=fig
        )

        ax_stack = fig.add_subplot(gs[0,0])
        ax_dp = fig.add_subplot(gs[1,0])
        ax_tree = fig.add_subplot(gs[:,1])

    else:

        gs = GridSpec(1,2,width_ratios=[1,2.2],figure=fig)

        ax_stack = fig.add_subplot(gs[0,0])
        ax_tree = fig.add_subplot(gs[0,1])
        ax_dp = None

    call_id_stack = []
    node_result = {}
    node_original = {}
    stack = []
    G = nx.DiGraph()
    labels = {}
    node_status = {}

    # start at first CALL event
    step_index = next(
        (i for i, e in enumerate(events) if e["type"] == "call"),
        0
    )

    algo_name = events[0]["func"] if events else ""
    recurrence_text = RECURRENCES.get(algo_name, "")
    dp_formula = DP_FORMULAS.get(algo_name, "")

    bottom_text = []
    if recurrence_text:
        bottom_text.append(f"Recurrence: {recurrence_text}")
    if dp_formula:
        # separate max function newlines with pipes to make it single/clean lines
        clean_formula = dp_formula.replace("\n", "  |  ")
        bottom_text.append(f"Formula: {clean_formula}")
    
    if bottom_text:
        fig.text(
            0.5, 0.02,
            "\n".join(bottom_text),
            ha="center", va="bottom", fontsize=11, color="blue", wrap=True
        )
        fig.subplots_adjust(bottom=0.15)

    def draw_step():
        nonlocal stack, G, labels, node_status, dp_table, board_state, current_cell, invalid_cell, ax_info, dp_dependencies, dp_cell

        call_id_stack.clear()
        # dp_cell = None
        if ax_stack:
            ax_stack.clear()
        if ax_tree:
            ax_tree.clear()

        # ---------- DRAW FORMULA (FIXED POSITION) ----------
        if "lis" in algo_name.lower() and ax_tree is not None:
            ax_tree.text(
                0.5, 1.05,
                "dp[i] = 1 + max(dp[j]) where j < i and arr[j] < arr[i]\nelse dp[i] = 1",
                ha="center",
                fontsize=11,
                color="blue",
                transform=ax_tree.transAxes
            )

        stack = []
        G = nx.DiGraph()
        labels = {}
        node_status = {}

        message = ""
        active_call_id = None

        for i in range(step_index + 1):
            event = events[i]

            # ---------- CALL ----------
            if event["type"] == "call":
                args = list(event["args"].values())[0]
                if event['func'] == "nQueens":
                    func = f"row={args}"
                else:
                    func = f"{event['func']}({args})"

                stack.append(func)
                call_id_stack.append(event["id"])
                active_call_id = call_id_stack[-1]

                G.add_node(event["id"])

                if event["func"] == "binarySearch":
                    low = event["args"]["low"]
                    high = event["args"]["high"]
                    labels[event["id"]] = f"[{low}, {high}]"
                else:
                    labels[event["id"]] = func
   
                node_original[event["id"]] = args
                node_result[event["id"]] = None
                node_status[event["id"]] = "normal"

                if event["parent"] is not None:
                    G.add_edge(event["parent"], event["id"])

                message = f"Calling {func}"

            # ---------- RETURN ----------
            elif event["type"] == "return":

                call_id = event["id"]
                result = event["value"]

                if stack:
                    stack.pop()

                if call_id_stack:
                    call_id_stack.pop()
                active_call_id = call_id_stack[-1] if call_id_stack else None

                node_status[call_id] = "done"
                node_result[call_id] = result

                message = f"Return → {result}"
            # ---------- ACTION ----------
            elif event["type"] == "phase":

                details = event.get("details", {})

                if "table" in details:
                    dp_table = details["table"]
                elif "dp" in details:
                    dp_table = details["dp"]

                phase = event["phase"]

                if active_call_id is None:
                    continue

                if phase == "divide":
                    node_status[active_call_id] = "split"
                    message = "Divide"

                elif phase == "combine":
                    node_status[active_call_id] = "done"
                    # node_result[active_call_id] = event["details"]["result"]
                    message = f"Combine → {event['details']['result']}"

                elif phase == "choose":
                    node_status[active_call_id] = "split"
                    message = "Choosing pivot"

                elif phase == "memo_hit":
                    node_status[active_call_id] = "cache"
                    message = "DP reuse"

                elif phase == "memo_store":
                    node_status[active_call_id] = "done"
                    message = "DP store"  

                elif phase == "dp_update":
                    details = event["details"]
                    dp_table = details.get("table", dp_table)

                    if isinstance(dp_table, dict) and "n" in details:
                        dp_cell = (0, details["n"])
                        message = f"Computed fib({details['n']}) = {dp_table[details['n']]}"  
                
                # elif phase == "array_update":
                #     array_state = event["details"]["array"]
                #     message = f"Array updated: {array_state}"

                elif phase == "explore":
                    board_state = event["details"]["board"]
                    current_cell = (event["details"]["row"], event["details"]["col"])
                    invalid_cell = None
                    # node_status[active_call_id] = "explore"
                    message = f"Trying column {event['details']['col']}"

                elif phase == "valid":
                    node_status[active_call_id] = "split"
                    message = "Valid placement"

                elif phase == "invalid":
                    board_state = event["details"]["board"]
                    invalid_cell = (event["details"]["row"], event["details"]["col"])
                    current_cell = None
                    message = "Conflict detected"

                elif phase == "backtrack":
                    node_status[active_call_id] = "backtrack"
                    message = "Backtracking"

                elif phase == "solution":
                    node_status[active_call_id] = "solution"
                    message = "Solution found"

                elif phase == "place":
                    board_state = event["details"]["board"]
                    current_cell = None
                    invalid_cell = None
                    message = "Placed Queen"
                    
                elif phase == "remove":
                    board_state = event["details"]["board"]
                    current_cell = None
                    invalid_cell = None
                    message = "Backtracking remove queen"
                
                elif phase == "consider_root":
                    message = f"Testing root {event['details']['k']} for range [{event['details']['i']}, {event['details']['j']}]\nCost = {event['details']['cost']} (Optimal: {event['details']['best_so_far']})"

                elif phase == "build_tree":
                    node_id = event["details"]["id"]
                    label = event["details"]["label"]
                    parent = event["details"]["parent"]
                    
                    G.add_node(node_id)
                    labels[node_id] = label
                    node_status[node_id] = "solution"
                    
                    if parent is not None:
                        G.add_edge(parent, node_id)
                        
                    message = f"Building Optimal Tree: Added Node {label}"

                elif phase == "mid":
                    message = f"Mid index = {event['details']['mid']} (value={event['details']['value']})"

                elif phase == "found":
                    message = f"Found at index {event['details']['index']}"

                elif phase == "left":
                    message = f"Move LEFT → high = {event['details']['new_high']}"

                elif phase == "right":
                    message = f"Move RIGHT → low = {event['details']['new_low']}"

                elif phase == "consider":
                    message = f"Checking item {event['details']['i']} at capacity {event['details']['w']}"

                elif phase == "update":
                    details = event["details"]

                    # ---------- LCS ----------
                    if "value" in details and "j" in details:
                        dp_table = details["table"]
                        dp_cell = (details["i"], details["j"])
                        dp_dependencies = [
                            (details["i"] - 1, details["j"]),
                            (details["i"], details["j"] - 1),
                            (details["i"]-1, details["j"]-1)
                        ]
                        message = f"dp[{details['i']}][{details['j']}] = {details['value']}"

                    # ---------- KNAPSACK ----------
                    elif "table" in details:
                        dp_table = details["table"]
                        i = details["i"]
                        w = details["w"]

                        dp_cell = (i,w)
                        dp_dependencies = [
                            (i - 1, w),
                        ]
                        
                        if w - details["i"] >= 0:
                            dp_dependencies.append((i-1, w - details["i"]))

                        message = (
                            f"Item {details['i']} at capacity {details['w']}\n"
                            f"Include = {details['include']}\n"
                            f"Exclude = {details['exclude']}\n"
                            f"Chosen = {details['chosen']}"
                        )
                        # message = f"dp[{details['i']}][{details['w']}] = {details['chosen']}"

                    # ---------- LIS ----------
                    elif "dp" in details:
                        dp_table = details["dp"]
                        dp_cell = (0, details["i"])
                        dp_dependencies = [(0, j) for j in range(details["i"])]
                        message = (
                            f"Updating dp[{details['i']}]\n"
                            f"Longest increasing subsequence ending here = {dp_table[details['i']]}"
                        )
                        # message = f"dp[{details['i']}] = {dp_table[details['i']]}"
                        
                    # ---------- OBST ----------
                    elif algo_name == "obst":
                        dp_table = details["table"]
                        dp_cell = (details["i"], details["j"])
                        dp_dependencies = []
                        message = f"cost[{details['i']}][{details['j']}] = {details['value']}"

                    # ---------- FALLBACK ----------
                    else:
                        message = "DP update"

                elif phase == "skip":
                    message = f"Item too heavy → skip"
                    dp_table = event["details"].get("table", dp_table)
                    dp_cell = (event["details"]["i"], event["details"]["w"])

                elif phase == "compare":
                    details = event["details"]

                    # ---------- LIS ----------
                    if "a_i" in details:
                        message = (
                            f"Compare arr[{details['j']}] = {details['a_j']} "
                            f"with arr[{details['i']}] = {details['a_i']}"
                        )

                    # ---------- LCS ----------
                    elif "c1" in details:
                        message = f"Compare '{details['c1']}' with '{details['c2']}'"

                    # ---------- FALLBACK ----------
                    else:
                        message = "Comparing..."
                
                # ---------- DRAW STACK ----------
        if ax_stack:
            for i, frame in enumerate(reversed(stack)):
                color = "orange" if i == 0 else "lightblue"
                ax_stack.text(
                    0.5, i, frame,
                    ha='center', va='center',
                    bbox=dict(boxstyle="round", facecolor=color),
                    fontsize=11
                )

            ax_stack.set_title("Call Stack (Space Complexity)")
            ax_stack.set_xlim(0,1)
            ax_stack.set_ylim(-1, max(4,len(stack)+1))
            ax_stack.axis('off')

        # ---------- NODE COLORS ----------
        colors = []
        for node in G.nodes:
            status = node_status.get(node, "normal")

            if status == "split":
                colors.append("#fff176")   # yellow
            elif status == "merging":
                colors.append("#ff8a65")   # orange
            elif status == "done":
                colors.append("#81c784")   # green
            elif status == "cache":
                colors.append("#ba68c8")   # purple
            elif status == "explore":
                colors.append("#64b5f6")  # blue
            elif status == "invalid":
                colors.append("#ef5350")  # red
            elif status == "backtrack":
                colors.append("#ffb74d")  # orange
            elif status == "solution":
                colors.append("#66bb6a")  # green
            else:
                colors.append("#90caf9")   # blue

        if ax_tree:
            # ---------- DRAW TREE ----------
            # ---------- UPDATE LABELS WITH RESULTS ----------
            display_labels = {}

            for node in G.nodes:

                original = labels[node]
                result = node_result.get(node)

                if result is not None:
                    display_labels[node] = f"{original}\n↓\n{result}"
                else:
                    display_labels[node] = original

            if len(G.nodes) > 0:

                # find correct root dynamically
                roots = [n for n in G.nodes if G.in_degree(n) == 0]
                root = roots[0] if roots else list(G.nodes)[0]

                pos = hierarchy_layout(G, root)

                # ensure only valid nodes are drawn
                valid_nodes = [n for n in G.nodes if n in pos]

                subG = G.subgraph(valid_nodes)

                sub_labels = {k: display_labels[k] for k in valid_nodes}
                sub_colors = [colors[list(G.nodes).index(k)] for k in valid_nodes]

                nx.draw(
                    subG,
                    pos,
                    labels=sub_labels,
                    node_color=sub_colors,
                    node_size=3200,
                    arrows=False,
                    ax=ax_tree
                )

            ax_tree.set_title("Recursion Tree (Algorithm Logic)")
            if algo_name == "knapsack":
                ax_tree.set_title("DP does not use recursion tree")

        # fig.suptitle(message, fontsize=14, color="darkgreen")
        fig.suptitle(f"[Step {step_index}] {message}", fontsize=14, color="darkgreen")
        fig.canvas.draw_idle()

        
        # # ---------- DRAW ARRAY (MERGE SORT) ----------

        # if is_mergesort:

        #     ax_array.clear()
        #     ax_array.set_title("Array Visualization")

        #     if array_state:

        #         values = array_state
        #         x = list(range(len(values)))

        #         ax_array.bar(x, values)

        #         ax_array.set_xticks(x)
        #         ax_array.set_xticklabels(values)

        #         ax_array.set_ylim(0, max(values) + 2)

        #     ax_array.axis("on")

        # ---------- DRAW CHESSBOARD ----------

        if is_nqueens:

            ax_board.clear()
            ax_board.set_title("Chessboard")

            if board_state is not None:

                n = len(board_state)

                for r in range(n):
                    for c in range(n):

                        base_color = "#f0d9b5" if (r+c)%2==0 else "#b58863"

                        # highlight invalid cell
                        if invalid_cell == (r, c):
                            color = "#ef5350"  # red
                        else:
                            color = base_color

                        ax_board.add_patch(
                            plt.Rectangle((c, r), 1, 1, color=color)
                        )

                        # highlight current cell (blue border)
                        if current_cell == (r, c):
                            ax_board.add_patch(
                                plt.Rectangle(
                                    (c, r), 1, 1,
                                    fill=False,
                                    edgecolor="blue",
                                    linewidth=3
                                )
                            )

                        # draw queen
                        if board_state[r] == c:
                            ax_board.text(
                                c+0.5, r+0.5, "Q",
                                ha="center",
                                va="center",
                                fontsize=18,
                                color="black"
                            )

                ax_board.set_xlim(0, n)
                ax_board.set_ylim(n, 0)

            ax_board.axis("off")


        # ---------- DRAW DP TABLE ----------
        # ---------- DRAW DP TABLE ----------
        if has_dp and ax_dp is not None:

            ax_dp.clear()
            ax_dp.set_title("Dynamic Programming Table")
            ax_dp.axis("off")

            if dp_table is not None:

                # 🔥 CASE 1 → Knapsack / 2D DP (LIST)
                if isinstance(dp_table, list):
                    # 🔥 CASE A → 1D DP (LIS)
                    if all(not isinstance(x, list) for x in dp_table):

                        table_data = [dp_table]

                        col_labels = [f"i={i}" for i in range(len(dp_table))]

                        table = ax_dp.table(
                            cellText=[dp_table],
                            colLabels=col_labels,
                            loc="center",
                            cellLoc="center",
                            bbox=[0, 0.3, 1, 0.4]
                        )

                        table.auto_set_font_size(False)
                        table.set_fontsize(12)

                        # highlight current index
                        if dp_cell:
                            _, i = dp_cell
                            if i < len(dp_table):
                                table[(1, i)].set_facecolor("#ffeb3b")
                        
                        for _, j in dp_dependencies:
                            if j < len(dp_table):
                                table[(1, j)].set_facecolor("#90caf9")

                    # 🔥 CASE B → 2D DP (Knapsack)
                    else:

                        rows = len(dp_table)
                        cols = len(dp_table[0]) if rows > 0 else 0

                        row_labels = [f"i={i}" for i in range(len(dp_table))]
                        col_labels = [f"w={j}" for j in range(len(dp_table[0]))]

                        table = ax_dp.table(
                            cellText=dp_table,
                            rowLabels=row_labels,
                            colLabels=col_labels,
                            loc="center",
                            cellLoc="center",
                            bbox=[0.1, 0.1, 0.9, 0.8]
                        )

                        table.auto_set_font_size(False)
                        table.set_fontsize(10)

                        # highlight current cell
                        if dp_cell:
                            i, w = dp_cell
                            if i < rows and w < cols:
                                table[(i + 1, w)].set_facecolor("#ffeb3b")
                        
                        for di, dj in dp_dependencies:
                            if 0 <= di < rows and 0 <= dj < cols:
                                table[(di+1, dj)].set_facecolor("#90caf9")
                
                # 🔥 CASE → Fibonacci DP (DICT)
                elif isinstance(dp_table, dict):

                    keys = sorted(dp_table.keys())
                    values = [dp_table[k] for k in keys]

                    ax_dp.clear()
                    ax_dp.set_title("Fibonacci DP Progression", fontsize=14)
                    #  draw boxes
                    for i, k in enumerate(keys):
                        x = i

                        # highlight current computation
                        if dp_cell and k == dp_cell[1]:
                            color = "#ffeb3b"  # yellow highlight
                        else:
                            color = "#90caf9"  # blue

                        # draw box
                        ax_dp.add_patch(
                            plt.Rectangle((x, 0), 1, 1, color=color, ec="black")
                        )

                        # value
                        ax_dp.text(
                            x + 0.5, 0.5,
                            str(dp_table[k]),
                            ha="center",
                            va="center",
                            fontsize=14
                        )

                        # label (n index)
                        ax_dp.text(
                            x + 0.5, -0.3,
                            f"n={k}",
                            ha="center",
                            fontsize=10
                        )

                    ax_dp.set_xlim(0, len(keys))
                    ax_dp.set_ylim(-1, 1.5)
                    ax_dp.axis("off")
            else:
                ax_dp.axis("off") 

        elif ax_dp is not None:
            ax_dp.axis("off")
        if ax_info:
            ax_info.clear()
            ax_info.set_title("Explanation")

            extra = ""

            if dp_dependencies:
                extra = "\nUsing previous states: \n"
                for d in dp_dependencies:
                    extra += f"{d}\n"
                    
            ax_info.text(
                0.05, 0.95,
                message + "\n" + extra,
                fontsize = 12,
                wrap=True,
                va='top'
            )

            ax_info.axis("off")


    def on_key(event):
        nonlocal step_index

        if event.key == " ":
            step_index = min(step_index + 1, len(events)-1)
            draw_step()

        elif event.key == "b":
            step_index = max(step_index - 1, 0)
            draw_step()

        elif event.key == "q":
            plt.close()

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
            pos.update(
                hierarchy_layout(
                    G, neighbor,
                    width=dx,
                    vert_gap=vert_gap,
                    vert_loc=vert_loc-vert_gap,
                    xcenter=nextx
                )
            )
    return pos