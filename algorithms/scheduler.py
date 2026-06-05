# algorithms/scheduler.py
# Central router for all scheduling algorithms.
# The UI calls run_scheduler() with a name and process list.
# This module dispatches to the correct algorithm and returns
# a unified result dict.

from algorithms.fcfs import run_fcfs
from algorithms.sjf import run_sjf
from algorithms.round_robin import run_round_robin
from algorithms.priority import run_priority


def run_scheduler(algorithm: str, processes: list[dict], quantum: int = 2) -> dict:
    """
    Dispatches to the correct scheduling algorithm.

    Args:
        algorithm:  One of "FCFS", "SJF", "RR", "Priority".
        processes:  List of process dicts (pid, arrival, burst, priority).
        quantum:    Time quantum for Round Robin (ignored for other algorithms).

    Returns:
        A result dict with keys: timeline, results,
        avg_waiting_time, avg_turnaround_time.

    Raises:
        ValueError: If fewer than 1 process is provided or algorithm is unknown.
    """

    if not processes:
        raise ValueError("No processes provided. Add at least one process.")

    algorithm = algorithm.strip().upper()

    if algorithm == "FCFS":
        return run_fcfs(processes)
    elif algorithm == "SJF":
        return run_sjf(processes)
    elif algorithm == "RR":
        if quantum <= 0:
            raise ValueError("Quantum must be greater than 0.")
        return run_round_robin(processes, quantum)
    elif algorithm == "PRIORITY":
        return run_priority(processes)
    else:
        raise ValueError(f"Unknown algorithm: '{algorithm}'.")