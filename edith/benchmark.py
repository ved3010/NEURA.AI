"""
E.D.I.T.H. System Benchmark Utility
"""

import time
import psutil
import logging

logger = logging.getLogger("edith.benchmark")


def run_benchmark() -> dict:
    """Run CPU and Memory speed benchmark test."""
    start_time = time.time()
    
    # Compute intensive calculation
    acc = 0
    for i in range(2_000_000):
        acc += i * 0.001
        
    duration = time.time() - start_time
    cpu_percent = psutil.cpu_percent()
    mem = psutil.virtual_memory()

    results = {
        "status": "COMPLETED",
        "compute_time_seconds": round(duration, 4),
        "score": round(1000 / max(0.01, duration), 2),
        "cpu_load_percent": cpu_percent,
        "memory_available_gb": round(mem.available / (1024**3), 2),
    }

    return results


if __name__ == "__main__":
    print(run_benchmark())
