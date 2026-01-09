def weighted_progress(tasks):
    total_points = 0
    total = 0
    for t in tasks:
        p = max(1, int(t.points or 1))
        total_points += p
        total += p * int(t.progress or 0)
    if total_points == 0:
        return 0
    return round(total / total_points, 1)
