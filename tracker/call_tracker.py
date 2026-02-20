class CallTracker:
    def __init__(self):
        self.events = []        # all events (call / return)
        self.call_id = 0        # unique id for each call
        self.stack = []         # current call stack

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

        return call_info["id"]

    def record_return(self, call_id, value):
        self.stack.pop()

        self.events.append({
            "type": "return",
            "id": call_id,
            "value": value
        })

    def reset(self):
        self.events.clear()
        self.stack.clear()
        self.call_id = 0