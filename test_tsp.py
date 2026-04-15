import sys
from algorithms.tsp import tracked_tsp
import json

try:
    events = tracked_tsp(3, [[0, 2, 9], [2, 0, 6], [9, 6, 0]])
    print(f"Success! {len(events)} events generated.")
    for e in events:
       if 'visual' in e:
          if 'edges' in e['visual']:
             print("Init edges sample: ", e['visual']['edges'][:2])
             break
except Exception as e:
    import traceback
    traceback.print_exc()
