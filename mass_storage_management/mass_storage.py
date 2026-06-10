
def fcfs_scheduling(requests, initial_head):
    """
    Simulates First-Come, First-Served disk scheduling.
    Returns the sequence of head movements and the total seek count.
    """
    total_head_movement = 0
    current_head = initial_head
    sequence = [initial_head] # Start tracking the path here