# algorithms/round_robin.py
# Round Robin (RR) Scheduling Algorithm.

# Rules:
#   - Each process gets a fixed time slice called the quantum.
#   - After the quantum expires, the running process is preempted and moved to the back of the ready queue.
#   - New arrivals join the queue before the preempted process when they arrive at the exact moment of preemption.
#   - If a process finishes before its quantum expires, the next scheduling decision happens immediately.

from collections import deque
from utils.metrics import (
    calculate_turnaround_time,
    calculate_waiting_time,
    calculate_averages,
)


def run_round_robin(processes: list[dict], quantum: int) -> dict:
    """
    Simulates Round Robin scheduling.

    Args:
        processes: List of process dicts with keys:
                   pid, arrival, burst, priority.
        quantum:   Time slice each process gets per turn (must be > 0).

    Returns:
        A dict with keys: timeline, results,
        avg_waiting_time, avg_turnaround_time.
    """

    # Work on a copy and track remaining burst time per process
    process_map = {
        p["pid"]: {
            "pid": p["pid"],
            "arrival": p["arrival"],
            "burst": p["burst"],
            "priority": p["priority"],
            "remaining": p["burst"],
            "completion": 0,
        }
        for p in processes
    }

    # Sort initial list by arrival time to feed the queue correctly
    sorted_pids = [p["pid"] for p in sorted(processes, key=lambda p: p["arrival"])]

    timeline = []
    current_time = 0
    ready_queue = deque()
    enqueued = set()

    # Enqueue processes that arrive at time 0
    for pid in sorted_pids:
        if process_map[pid]["arrival"] <= current_time:
            ready_queue.append(pid)
            enqueued.add(pid)

    while ready_queue:
        pid = ready_queue.popleft()
        proc = process_map[pid]

        # Run for at most one quantum
        run_for = min(quantum, proc["remaining"])
        start_time = current_time
        end_time = current_time + run_for

        timeline.append({
            "pid": pid,
            "start": start_time,
            "end": end_time,
        })

        proc["remaining"] -= run_for
        current_time = end_time

        # Enqueue newly arrived processes before re-queueing preempted one
        for pid2 in sorted_pids:
            if pid2 not in enqueued and process_map[pid2]["arrival"] <= current_time:
                ready_queue.append(pid2)
                enqueued.add(pid2)

        if proc["remaining"] > 0:
            # Process not finished — goes back to the end of the queue
            ready_queue.append(pid)
        else:
            # Process finished
            proc["completion"] = current_time

        # If the queue is empty but processes haven't all arrived, advance time
        if not ready_queue:
            unarrived = [
                p for p in process_map.values()
                if p["pid"] not in enqueued
            ]
            if unarrived:
                next_arrival = min(p["arrival"] for p in unarrived)
                current_time = next_arrival
                for pid2 in sorted_pids:
                    if (
                        pid2 not in enqueued
                        and process_map[pid2]["arrival"] <= current_time
                    ):
                        ready_queue.append(pid2)
                        enqueued.add(pid2)

    # Build results from the completed process map
    results = []
    for pid in sorted_pids:
        proc = process_map[pid]
        turnaround = calculate_turnaround_time(proc["completion"], proc["arrival"])
        waiting = calculate_waiting_time(turnaround, proc["burst"])
        results.append({
            "pid": pid,
            "arrival": proc["arrival"],
            "burst": proc["burst"],
            "completion": proc["completion"],
            "turnaround_time": turnaround,
            "waiting_time": waiting,
        })

    averages = calculate_averages(results)

    return {
        "timeline": timeline,
        "results": results,
        "avg_waiting_time": averages["avg_waiting_time"],
        "avg_turnaround_time": averages["avg_turnaround_time"],
    }