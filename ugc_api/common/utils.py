def inc_avg_mean(avg: float, count: int, value: int) -> float:
    """
    update arithmetic mean
    :param avg: current avg value
    :param count: member count
    :param value: value of new member
    """
    return (avg + value) / (count + 1)
