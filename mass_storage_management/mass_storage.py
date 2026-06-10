
def fcfs_scheduling(requests, initial_head):
    """
    Simulates First-Come, First-Served disk scheduling.
    Returns the sequence of head movements and the total seek count.
    """
    total_head_movement = 0
    current_head = initial_head
    sequence = [initial_head] # Start tracking the path here

    for track in requests:
        # Calculate the distance from current head to the requested track
        distance = abs(current_head - track)
        total_head_movement += distance

        # Move the head to the new track
        current_head = track
        sequence.append(current_head)

    return sequence, total_head_movement