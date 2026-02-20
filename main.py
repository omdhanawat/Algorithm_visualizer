from algorithms.fibonacci import tracked_fib, tracker
from visualizer.combined_view import animate_execution

tracker.reset()
tracked_fib(4)

animate_execution(tracker.events)


# from algorithms.fibonacci import tracked_fib, tracker
# from visualizer.tree_view import draw_tree
# from algorithms.fibonacci import tracked_fib, tracker
# from visualizer.stack_view import animate_stack

# tracker.reset()
# tracked_fib(4)

# draw_tree(tracker.events)
# animate_stack(tracker.events)


# tracker.reset()
# tracked_fib(4)


# tracker.reset()
# result = tracked_fib(4)

# print("Result:", result)
# print("\nExecution Log:")

# for event in tracker.events:
#     print(event)