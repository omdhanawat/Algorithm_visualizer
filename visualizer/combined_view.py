import matplotlib.pyplot as plt
import networkx as nx

def animate_execution(events):
    plt.ion()
    fig = plt.figure(figsize=(12,6))

    ax_stack = fig.add_subplot(121)
    ax_tree = fig.add_subplot(122)

    stack = []
    G = nx.DiGraph()
    labels = {}

    for step, event in enumerate(events):

        # ----- UPDATE MODEL -----
        if event["type"] == "call":
            func = f"{event['func']}({event['args']['n']})"
            stack.append(func)

            G.add_node(event["id"])
            labels[event["id"]] = func

            if event["parent"] is not None:
                G.add_edge(event["parent"], event["id"])

        elif event["type"] == "return":
            if stack:
                stack.pop()

        # ----- DRAW STACK -----
        ax_stack.clear()
        for i, frame in enumerate(reversed(stack)):
            color = "orange" if i == 0 else "lightblue"
            ax_stack.text(0.5, i, frame,
                          ha='center', va='center',
                          bbox=dict(boxstyle="round", facecolor=color))

        ax_stack.set_title("Call Stack (Space Complexity)")
        ax_stack.set_xlim(0,1)
        ax_stack.set_ylim(-1, max(6,len(stack)+1))
        ax_stack.axis('off')

        # ----- DRAW TREE -----
        ax_tree.clear()
        if len(G.nodes) > 0:
            pos = hierarchy_layout(G, 0)
            nx.draw(G, pos,
                    labels=labels,
                    node_size=2000,
                    node_color="#90caf9",
                    font_size=9,
                    arrows=False,
                    ax=ax_tree)

        ax_tree.set_title("Recursion Tree (Time Complexity)")

        plt.pause(1.2)

    plt.ioff()
    plt.show()


def hierarchy_layout(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {root:(xcenter,vert_loc)}
    neighbors = list(G.neighbors(root))

    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos.update(hierarchy_layout(G, neighbor, width=dx,
                                        vert_gap=vert_gap,
                                        vert_loc=vert_loc-vert_gap,
                                        xcenter=nextx))
    return pos