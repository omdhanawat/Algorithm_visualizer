import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sys
import os
import traceback

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.middleware.cors import CORSMiddleware
        from pydantic import BaseModel
        from typing import List, Optional, Dict, Any

        # Initialize FastAPI dynamically
        fastapi_app = FastAPI(title="Algorithm Visualizer API")

        # Enable CORS for the React frontend
        fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        class AlgorithmRequest(BaseModel):
            params: Dict[str, Any]

        @fastapi_app.get("/health")
        async def health():
            return {"status": "ok"}

        @fastapi_app.get("/api/health")
        async def api_health():
            return {"status": "api ok"}

        @fastapi_app.post("/solve/{algo_id}")
        async def solve(algo_id: str, request: AlgorithmRequest):
            try:
                # Deferred Standardized Algorithm Imports
                from algorithms.fibonacci import tracked_fib, get_fib_tracker
                from algorithms.mergesort import tracked_mergesort, get_mergesort_tracker
                from algorithms.quicksort import tracked_quicksort, get_quicksort_tracker
                from algorithms.fibonacci_dp import tracked_fib_dp, get_fib_dp_tracker
                from algorithms.nqueens import tracked_nqueens, get_nqueens_tracker
                from algorithms.binary_search import tracked_binary_search, get_binary_search_tracker
                from algorithms.knapsack import tracked_knapsack, get_knapsack_tracker
                from algorithms.lis import tracked_lis, get_lis_tracker
                from algorithms.lcs import tracked_lcs, get_lcs_tracker
                from algorithms.obst import tracked_obst, get_obst_tracker
                from algorithms.floyd_warshall import tracked_floyd_warshall, get_fw_tracker
                from algorithms.dijkstra import tracked_dijkstra, get_dijkstra_tracker
                from algorithms.kruskal import tracked_kruskal, get_kruskal_tracker
                from algorithms.prim import tracked_prim, get_prim_tracker
                from algorithms.fractional_knapsack import tracked_fractional_knapsack, get_fractional_knapsack_tracker
                from algorithms.tsp import tracked_tsp, get_tsp_tracker

                params = request.params
                
                algos = {
                    "fib": (tracked_fib, get_fib_tracker),
                    "mergeSort": (tracked_mergesort, get_mergesort_tracker),
                    "quickSort": (tracked_quicksort, get_quicksort_tracker),
                    "fibDP": (tracked_fib_dp, get_fib_dp_tracker),
                    "nQueens": (tracked_nqueens, get_nqueens_tracker),
                    "binarySearch": (tracked_binary_search, get_binary_search_tracker),
                    "knapsack": (tracked_knapsack, get_knapsack_tracker),
                    "lis": (tracked_lis, get_lis_tracker),
                    "lcs": (tracked_lcs, get_lcs_tracker),
                    "obst": (tracked_obst, get_obst_tracker),
                    "floyd_warshall": (tracked_floyd_warshall, get_fw_tracker),
                    "dijkstra": (tracked_dijkstra, get_dijkstra_tracker),
                    "kruskal": (tracked_kruskal, get_kruskal_tracker),
                    "prim": (tracked_prim, get_prim_tracker),
                    "fractionalKnapsack": (tracked_fractional_knapsack, get_fractional_knapsack_tracker),
                    "tsp": (tracked_tsp, get_tsp_tracker),
                }

                if algo_id not in algos:
                    raise HTTPException(status_code=404, detail="Algorithm not found")

                fn, tracker_fn = algos[algo_id]
                tracker = tracker_fn()
                tracker.reset()

                if algo_id == "fib": fn(params.get("n", 5))
                elif algo_id == "mergeSort": fn(params.get("arr", [5, 2, 8, 1, 9]))
                elif algo_id == "quickSort": fn(params.get("arr", [5, 2, 8, 1, 9]))
                elif algo_id == "fibDP": fn(params.get("n", 8))
                elif algo_id == "nQueens": fn(params.get("n", 4))
                elif algo_id == "binarySearch": fn(params.get("arr", [1, 3, 5, 8, 12, 15, 18, 21, 25]), params.get("target", 18))
                elif algo_id == "knapsack": fn(params.get("weights", [2, 3, 4, 5]), params.get("values", [3, 4, 5, 8]), params.get("capacity", 8))
                elif algo_id == "lis": fn(params.get("arr", [10, 22, 9, 33, 21, 50, 41, 60]))
                elif algo_id == "lcs": fn(params.get("X", "AGGTAB"), params.get("Y", "GXTXAYB"))
                elif algo_id == "obst": fn(params.get("keys", [10, 12, 20]), params.get("freq", [34, 8, 50]))
                elif algo_id == "floyd_warshall": 
                    v = params.get("V", 4)
                    e = params.get("edges", [[0,1,5], [0,3,10], [1,2,3], [2,3,1]])
                    fn(v, e)
                elif algo_id == "dijkstra": 
                    v = params.get("V", 6)
                    e = params.get("edges", [[0,1,7], [0,2,9], [0,5,14], [1,2,10], [1,3,15], [2,3,11], [2,5,2], [3,4,6], [4,5,9]])
                    fn(v, e, params.get("source", 0))
                elif algo_id == "kruskal": 
                    v = params.get("V", 6)
                    e = params.get("edges", [[0,1,4], [0,2,3], [1,2,1], [1,3,2], [2,3,4], [3,4,2], [4,5,6]])
                    fn(v, e)
                elif algo_id == "prim": 
                    v = params.get("V", 6)
                    e = params.get("edges", [[0,1,4], [0,2,3], [1,2,1], [1,3,2], [2,3,4], [3,4,2], [4,5,6]])
                    fn(v, e, params.get("source", 0))
                elif algo_id == "fractionalKnapsack": fn(params.get("weights", [10, 20]), params.get("values", [60, 100]), params.get("capacity", 50))
                elif algo_id == "tsp": fn(params.get("n", 3), params.get("distMatrix", [[0, 2, 9], [2, 0, 6], [9, 6, 0]]))
                
                return {"events": tracker.events}
            except Exception as e:
                tb = traceback.format_exc()
                return {"error": str(e), "traceback": tb, "status": 500}

        # Route the ASGI request to the dynamically created FastAPI app
        await fastapi_app(scope, receive, send)

    except Exception as e:
        # If FastAPI fails to import, or anything else fails at the top level
        tb = traceback.format_exc()
        response_body = f"CRITICAL ASGI BOOT ERROR:\n{tb}".encode('utf-8')
        await send({
            'type': 'http.response.start',
            'status': 500,
            'headers': [[b'content-type', b'text/plain']]
        })
        await send({
            'type': 'http.response.body',
            'body': response_body
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000, reload=True)
