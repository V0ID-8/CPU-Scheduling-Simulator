# utils/metrics.py
# Shared metric calculations used by all scheduling algorithms.
# Keeps math logic out of the algorithm and UI files.

def calculate_waiting_time(turnaround_time: float, burst_time: float) -> float:
    """
    waiting time = turnaround_time - burst_time
    the total time a process spends in the ready queue, not running\
    """

    return turnaround_time - burst_time


def calculate_turnaround_time(completion_time: float, arrival_time: float) -> float:
    """
    turnaround time = completion_time - arrival_time
    total time taken from arrival to completion of a process
    """
    return completion_time - arrival_time

def calculate_average(processes: list[dict]) -> dict:
    """
    given a list of process result dicts (each with 'waiting_time' and 'turnaround_time' keys),return the average.
    """
    count = len(processes)
    if count == 0:
        return {"average_waiting_time": 0.0, "average_turnaround_time": 0.0}
    
    avg_wt = sum(p["waiting_time"] for p in processes) / count
    avg_tat = sum(p["turnaround_time"] for p in processes) / count

    return {"average_waiting_time": round(avg_wt, 2), "average_turnaround_time": round(avg_tat, 2)}

