# algorithms/priority.py
# Priority Scheduling Algorithm — Non-Preemptive.

# Rules:
#   - At each scheduling decision point, pick the available process with the lowest priority number (highest urgency).
#   - Non-preemptive: once a process starts, it runs to completion.
#   - Ties in priority are broken by arrival time, then PID.
#   - Warning: low-priority processes may starve if high-priority ones keep arriving. This simulator does not implement aging.

from utils.metrics import (
    calculate_turnaround_time,
    calculate_waiting_time,
    calculate_averages,
)


def run_priority(processes: list[dict]) -> dict:
    """
    Simulates non-preemptive Priority scheduling.

    Args:
        processes: List of process dicts with keys:
                   pid, arrival, burst, priority.

    Returns:
        A dict with keys: timeline, results,
        avg_waiting_time, avg_turnaround_time.
    """

    # Work on a copy — never mutate the original list
    remaining = [p.copy() for p in processes]

    timeline = []
    results = []
    current_time = 0
    completed = 0
    total = len(remaining)

    while completed < total:
        # Collect all processes that have arrived and are not yet done
        available = [
            p for p in remaining
            if p["arrival"] <= current_time and not p.get("done", False)
        ]

        if not available:
            # CPU is idle — jump to the next arrival
            next_arrival = min(
                p["arrival"] for p in remaining if not p.get("done", False)
            )
            current_time = next_arrival
            continue

        # Pick the highest-priority process (lowest priority number)
        # Ties broken by arrival time, then PID
        chosen = min(
            available,
            key=lambda p: (p["priority"], p["arrival"], p["pid"])
        )

        start_time = current_time
        end_time = current_time + chosen["burst"]

        timeline.append({
            "pid": chosen["pid"],
            "start": start_time,
            "end": end_time,
        })

        turnaround = calculate_turnaround_time(end_time, chosen["arrival"])
        waiting = calculate_waiting_time(turnaround, chosen["burst"])

        results.append({
            "pid": chosen["pid"],
            "arrival": chosen["arrival"],
            "burst": chosen["burst"],
            "completion": end_time,
            "turnaround_time": turnaround,
            "waiting_time": waiting,
        })

        # Mark as done in the working copy
        for p in remaining:
            if p["pid"] == chosen["pid"]:
                p["done"] = True
                break

        current_time = end_time
        completed += 1

    averages = calculate_averages(results)

    return {
        "timeline": timeline,
        "results": results,
        "avg_waiting_time": averages["avg_waiting_time"],
        "avg_turnaround_time": averages["avg_turnaround_time"],
    }