import networkx as nx
import matplotlib.pyplot as plt

def build_tree(events):
    G = nx.DiGraph()
    labels = {}

    for event in events:
        if event["type"] == "call":
            node_id = event["id"]
            label = f"{event['func']}({event['args']['n']})"

            G.add_node(node_id)
            labels[node_id] = label

            if event["parent"] is not None:
                G.add_edge(event["parent"], node_id)

    return G, labels

def draw_tree(events):
    G, labels = build_tree(events)

    pos = hierarchy_layout(G, 0)

    plt.figure(figsize=(10,6))
    nx.draw(G, pos,
            labels=labels,
            node_size=2000,
            node_color="#90caf9",
            font_size=10,
            arrows=False)

    plt.title("Recursion Tree (Time Complexity Structure)")
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