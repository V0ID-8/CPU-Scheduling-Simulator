# utils/validators.py
# Input validation helpers used before dispatching to the scheduler.
# Keeping validation here means UI files stay clean and rules
# can be updated in one place.


def validate_processes(processes: list[dict]) -> tuple[bool, str]:
    """
    Validates the full list of processes before scheduling.

    Returns:
        (True, "") if valid.
        (False, error_message) if invalid.
    """
    if not processes:
        return False, "No processes added. Please add at least one process."

    if len(processes) > 10:
        return False, "Maximum 10 processes supported."

    seen_configs = []
    for p in processes:
        if p["burst"] <= 0:
            return False, f"{p['pid']} has an invalid burst time. Burst must be > 0."
        if p["arrival"] < 0:
            return False, f"{p['pid']} has a negative arrival time."
        if p["priority"] < 0:
            return False, f"{p['pid']} has a negative priority."

        config = (p["arrival"], p["burst"])
        seen_configs.append(config)

    return True, ""


def validate_quantum(quantum: int) -> tuple[bool, str]:
    """
    Validates the Round Robin quantum value.

    Returns:
        (True, "") if valid.
        (False, error_message) if invalid.
    """
    if quantum <= 0:
        return False, "Quantum must be a positive integer greater than 0."
    if quantum > 100:
        return False, "Quantum value is unrealistically large. Keep it under 100."
    return True, ""