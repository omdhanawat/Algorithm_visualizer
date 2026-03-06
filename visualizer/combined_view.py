import matplotlib.pyplot as plt
import networkx as nx
from algorithms.recurrence_info import RECURRENCES
from matplotlib.gridspec import GridSpec

def animate_execution(events):
    
    has_dp = any(
        e.get("type") == "phase" and e.get("phase") == "dp_update"
        for e in events
    )
    fig = plt.figure(figsize=(13,7))
    dp_table = None   # ← ALWAYS defined

    board_state = None
    is_nqueens = events[0]["func"] == "nQueens"

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

    elif has_dp:

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

    algo_name = events[0]["func"]
    recurrence_text = RECURRENCES.get(algo_name, "")

    fig.text(
        0.5, 0.02,
        f"Recurrence: {recurrence_text}",
        ha="center", fontsize=12, color="blue"
    )

    def draw_step():
        nonlocal stack, G, labels, node_status, dp_table, board_state

        ax_stack.clear()
        ax_tree.clear()

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
                    dp_table = event["details"]["table"]  

                elif phase == "explore":
                    node_status[active_call_id] = "explore"
                    message = f"Trying column {event['details']['col']}"

                elif phase == "valid":
                    node_status[active_call_id] = "split"
                    message = "Valid placement"

                elif phase == "invalid":
                    node_status[active_call_id] = "invalid"
                    message = "Conflict detected"

                elif phase == "backtrack":
                    node_status[active_call_id] = "backtrack"
                    message = "Backtracking"

                elif phase == "solution":
                    node_status[active_call_id] = "solution"
                    message = "Solution found"

                elif phase == "place":
                    board_state = event["details"]["board"]
                    message = f"Place Queen ({event['details']['row']},{event['details']['col']})"

                elif phase == "remove":
                    board_state = event["details"]["board"]
                    message = "Backtracking remove queen"

                # ---------- DRAW STACK ----------
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
            pos = hierarchy_layout(G, 0)
            nx.draw(
                G, pos,
                labels=display_labels,
                node_color=colors,
                node_size=3200,
                arrows=False,
                ax=ax_tree
            )
            # nx.draw(
            #     G, pos,
            #     labels=labels,
            #     node_color=colors,
            #     node_size=2000,
            #     arrows=False,
            #     ax=ax_tree
            # )

        ax_tree.set_title("Recursion Tree (Algorithm Logic)")

        fig.suptitle(message, fontsize=14, color="darkgreen")
        fig.canvas.draw_idle()


        # ---------- DRAW CHESSBOARD ----------

        if is_nqueens:

            ax_board.clear()
            ax_board.set_title("Chessboard")

            if board_state is not None:

                n = len(board_state)

                for r in range(n):
                    for c in range(n):

                        color = "#f0d9b5" if (r+c)%2==0 else "#b58863"

                        ax_board.add_patch(
                            plt.Rectangle((c,r),1,1,color=color)
                        )

                        if board_state[r] == c:
                            ax_board.text(
                                c+0.5,r+0.5,"Q",
                                ha="center",
                                va="center",
                                fontsize=18,
                                color="black"
                            )

                ax_board.set_xlim(0,n)
                ax_board.set_ylim(n,0)

            ax_board.axis("off")


        # ---------- DRAW DP TABLE ----------
        if has_dp and ax_dp is not None:

            ax_dp.clear()
            ax_dp.set_title("Dynamic Programming Table")

            if dp_table:

                keys = sorted(dp_table.keys())
                values = [dp_table[k] for k in keys]

                table_data = [
                    [f"n={k}" for k in keys],
                    values
                ]

                table = ax_dp.table(
                    cellText=table_data,
                    loc="center",
                    cellLoc="center"
                )

                table.scale(1.2, 2.5)
                table.auto_set_font_size(False)
                table.set_fontsize(12)

            ax_dp.axis("off")
    
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


def hierarchy_layout(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
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