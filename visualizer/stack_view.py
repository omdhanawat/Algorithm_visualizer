import matplotlib.pyplot as plt

def animate_stack(events):
    stack = []
    call_map = {}

    plt.ion()
    fig, ax = plt.subplots(figsize=(8,6))

    step = 1

    for event in events:
        ax.clear()

        explanation = ""
        return_info = ""

        # ---------- CALL ----------
        if event["type"] == "call":
            func = f"{event['func']}({event['args']['n']})"
            parent = call_map.get(event["parent"], None)

            call_map[event["id"]] = func
            stack.append(func)

            if parent:
                explanation = f"{parent} calls {func} and waits for result"
            else:
                explanation = f"Start execution: {func}"

        # ---------- RETURN ----------
        elif event["type"] == "return":
            func = call_map.get(event["id"], "")
            value = event["value"]

            if stack:
                stack.pop()

            parent = call_map.get(
                next((e["parent"] for e in events if e.get("id")==event["id"]), None),
                None
            )

            explanation = f"{func} finished execution"
            return_info = f"Returned value {value}"

        # ---------- DRAW STACK ----------
        for i, frame in enumerate(reversed(stack)):
            color = "#ffcc80" if i == 0 else "#90caf9"
            ax.text(
                0.2, i,
                frame,
                ha='center',
                va='center',
                fontsize=12,
                bbox=dict(boxstyle="round,pad=0.5", facecolor=color)
            )

        # ---------- TEXT AREA ----------
        ax.text(0.55, 0.85, f"Step {step}", transform=ax.transAxes, fontsize=14, weight="bold")
        ax.text(0.55, 0.70, explanation, transform=ax.transAxes, fontsize=12)
        ax.text(0.55, 0.55, return_info, transform=ax.transAxes, fontsize=12, color="green")

        ax.set_title("Understanding Recursion via Call Stack", fontsize=15)
        ax.set_xlim(0,1)
        ax.set_ylim(-1, max(6,len(stack)+1))
        ax.axis('off')

        plt.pause(1.4)
        step += 1

    plt.ioff()
    plt.show()