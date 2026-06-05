# algorithms/fcfs.py
# First Come First Served (FCFS) Scheduling Algorithm.

# Rules:
# Processes are sorted by arrival time.
# Non-preemptive: once a process starts, it runs to completion.
# If the CPU is idle (no process has arrived yet), time advances to the next arrival.

from utils.metrics import (
    calculate_turnaround_time,
    calculate_waiting_time,
    calculate_averages,
)


def run_fcfs(processes: list[dict]) -> dict:
    """
    simulate FCFS scheduling.
    args:
        processes: List of process dicts with keys:
            pid, arrival, burst, priority.
             
    returns:
        A dict with keys: timeline, results, avg_waiting_time, avg_turnaround_time.
    """

    # works on sorted copy - never mutate the original list
    queue = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))

    timeline = []
    results = []
    current_time = 0

    for process in queue:
        # if cpu is idle, jump forward to when this process arrives

        if current_time < process["arrival"]:
            current_time = process["arrival"]

        start_time = current_time
        end_time = start_time + process["burst"]

        timeline.append({
            "pid": process["pid"],
            "start": start_time,
            "end": end_time,
        })

        turnaround = calculate_turnaround_time(end_time, process["arrival"])
        waiting = calculate_waiting_time(turnaround, process["burst"])

        results.append({
            "pid": process["pid"],
            "arrival": process["arrival"],
            "burst": process["burst"],
            "completion": end_time,
            "turnaround_time": turnaround,
            "waiting_time": waiting,
        })

        current_time = end_time

    averages = calculate_averages(results)

    return {
        "timeline": timeline,
        "results": results,
        "avg_waiting_time": averages["avg_waiting_time"],
        "avg_turnaround_time": averages["avg_turnaround_time"],
    }
