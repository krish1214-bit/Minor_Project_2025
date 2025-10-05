def calculate_green_timings(lane_vehicle_counts: dict):
    """
    Calculates the new green light duration for each lane based on
    the current number of vehicles.

    The logic here is straightforward: lanes with more vehicles get
    a longer green light, but we ensure all lanes get at least a minimum
    amount of time to prevent starvation. The duration is capped at a
    maximum to keep things fair and avoid gridlock on other lanes.

    Args:
        lane_vehicle_counts (dict): A dictionary where keys are lane IDs
                                    and values are the number of vehicles.

    Returns:
        dict: A dictionary mapping lane IDs to their new green light
              durations in seconds.
    """
    min_green_seconds = 15
    max_green_seconds = 60

    total_vehicles_on_road = sum(lane_vehicle_counts.values())
    if total_vehicles_on_road == 0:
        # If no vehicles are detected, everyone gets the minimum green time.
        # This keeps the intersection from getting stuck.
        return {lane: min_green_seconds for lane in lane_vehicle_counts}

    # The core of the logic: calculate each lane's green time based on
    # its proportion of the total traffic.
    new_timings = {}
    for lane_id, vehicle_count in lane_vehicle_counts.items():
        # A little math to scale the green time between our min and max values.
        proportion = vehicle_count / total_vehicles_on_road
        green_time = min_green_seconds + (max_green_seconds - min_green_seconds) * proportion
        new_timings[lane_id] = int(green_time)

    return new_timings