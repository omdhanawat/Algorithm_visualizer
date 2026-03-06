import matplotlib.pyplot as plt

def draw_state_panel(ax, state_data):
    ax.clear()
    ax.set_title("State Evolution / DP Table")

    if not state_data:
        ax.axis("off")
        return

    text_lines = []

    for key, value in state_data.items():
        text_lines.append(f"{key}: {value}")

    for i, line in enumerate(text_lines):
        ax.text(0.1, 0.9 - i*0.1, line, fontsize=11)

    ax.axis("off")