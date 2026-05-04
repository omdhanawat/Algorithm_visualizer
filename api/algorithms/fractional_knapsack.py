from tracker.call_tracker import CallTracker

def get_fractional_knapsack_tracker():
    if not hasattr(get_fractional_knapsack_tracker, "tracker"):
        get_fractional_knapsack_tracker.tracker = CallTracker()
    return get_fractional_knapsack_tracker.tracker

def tracked_fractional_knapsack(weights, values, capacity):
    n = len(weights)
    tracker = get_fractional_knapsack_tracker()
    tracker.reset()
    call_id = tracker.record_call("fractional_knapsack", {"weights": weights, "values": values, "capacity": capacity})
    
    items = []
    for i in range(n):
        items.append({
            "id": i,
            "w": weights[i],
            "v": values[i],
            "ratio": round(values[i] / weights[i], 2)
        })
    
    tracker.record_phase(
        "calculate_ratios",
        message=f"Initialized {n} items. Calculated Value/Weight ratio for each to identify the most 'valuable' items per unit.",
        state={"items": items, "capacity": capacity}
    )
    
    sorted_items = sorted(items, key=lambda x: x["ratio"], reverse=True)
    tracker.record_phase(
        "greedy_sorting",
        message="Sorted items by ratio in descending order. We will greedily pick the highest ratio items first.",
        state={"items": sorted_items}
    )
    
    total_value = 0.0
    rem_capacity = float(capacity)
    selected = []
    
    for item in sorted_items:
        if rem_capacity <= 0: break
            
        if item["w"] <= rem_capacity:
            total_value += item["v"]
            rem_capacity -= item["w"]
            selected.append({"id": item["id"], "fraction": 1.0, "v": item["v"]})
            tracker.record_phase(
                "pick_full_item",
                message=f"Item {item['id']} fits! Taking the whole item. Value +{item['v']}, Capacity remaining: {rem_capacity}.",
                i=item["id"],
                visual={"nodes": [item["id"]]},
                state={"total_value": round(total_value, 2), "rem_capacity": rem_capacity, "selected": list(selected)}
            )
        else:
            fraction = round(rem_capacity / item["w"], 2)
            val_added = round(item["v"] * fraction, 2)
            total_value += val_added
            selected.append({"id": item["id"], "fraction": fraction, "v": val_added})
            
            tracker.record_phase(
                "pick_fractional_item",
                message=f"Item {item['id']} is too large. Taking a {int(fraction*100)}% fraction to fill the remaining {rem_capacity} capacity.",
                i=item["id"],
                visual={"nodes": [item["id"]]},
                state={"total_value": round(total_value, 2), "rem_capacity": 0, "selected": list(selected)}
            )
            rem_capacity = 0

    tracker.record_phase("complete", message=f"Greedy selection complete. Maximum total value obtained: {round(total_value, 2)}.", state={"selected": selected})
    tracker.record_return(call_id, total_value)
    return total_value
