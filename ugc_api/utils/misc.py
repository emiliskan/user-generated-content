
def inc_avg_mean(avg, cnt, val):
    """
    update arithmetic mean
    :param avg: old value
    :param cnt: member count
    :param val: new value
    """
    return (avg + val) / (cnt + 1)
