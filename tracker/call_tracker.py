class CallTracker:
    def __init__(self):
        self.events = []        # all events (call / return)
        self.call_id = 0        # unique id for each call
        self.stack = []         # current call stack
        self.total_calls = 0
        self.current_depth = 0
        self.max_depth = 0

    def record_call(self, func_name, args):
        parent_id = self.stack[-1] if self.stack else None
        
        call_info = {
            "type": "call",
            "id": self.call_id,
            "func": func_name,
            "args": args,
            "depth": len(self.stack),
            "parent": parent_id
        }

        self.events.append(call_info)
        self.stack.append(self.call_id)
        self.call_id += 1
        self.total_calls += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        return call_info["id"]

    def record_return(self, call_id, value):
        self.stack.pop()

        self.events.append({
            "type": "return",
            "id": call_id,
            "value": value
        })

        self.current_depth -= 1

    def reset(self):
        self.events.clear()
        self.stack.clear()
        self.call_id = 0
        # self.total_calls = 0
        # self.current_depth = 0
        # self.max_depth = 0

    def record_action(self, action_type, details):
        self.events.append({
            "type": "action",
            "action": action_type,
            "details": details
        })

    def record_phase(self, phase, details=None):
        self.events.append({
            "type": "phase",
            "phase": phase,
            "details": details or {}
        })