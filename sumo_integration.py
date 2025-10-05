import os
import sys
import traci

# Define the path to the SUMO GUI executable. This is specific to my machine,
# so you'll need to update this to your own path!
SUMO_GUI_PATH = r"C:\Users\Krish Setiya\Downloads\sumo-win64-1.24.0\sumo-1.24.0\bin\sumo-gui.exe"
# Making sure the SUMO environment variable is set so TraCI can find its tools.
if 'SUMO_HOME' in os.environ:
    tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools_path)
else:
    sys.exit("Oops! Looks like the 'SUMO_HOME' environment variable isn't set. I need that to find the tools.")


def launch_sumo_simulation(sumo_config_file):
    """
    Starts the SUMO GUI and sets up the connection with our script using TraCI.
    Think of it as opening the simulation world so we can start interacting with it.
    """
    # Using the hardcoded path directly to avoid any environment issues.
    sumo_command = [SUMO_GUI_PATH, "-c", sumo_config_file]

    print("Okay, launching the SUMO simulation now...")
    traci.start(sumo_command)


def get_current_vehicle_counts(lane_identifiers):
    """
    Asks the SUMO simulation for the real-time vehicle count for a given
    list of lanes. It's like asking a traffic controller for a status update.

    Args:
        lane_identifiers (list): A list of strings, where each string is a lane ID.

    Returns:
        dict: A dictionary with each lane ID and the number of vehicles on it.
    """
    current_counts = {}
    for lane_id in lane_identifiers:
        # We're getting the number of vehicles that passed over this lane in the last time step.
        current_counts[lane_id] = traci.lane.getLastStepVehicleNumber(lane_id)
    return current_counts


def update_traffic_light_timings(traffic_light_id, phase_duration, phase_state):
    """
    Adjusts the traffic light's phase duration and state in the simulation.

    Args:
        traffic_light_id (str): The ID of the traffic light we want to control.
        phase_duration (int): How long the new green light phase should last, in seconds.
        phase_state (str): The new state of the traffic light phase (e.g., "GGrr", "rGGr").
    """
    # The TraCI 'setPhaseDuration' function is what makes our dynamic logic work!
    traci.trafficlight.setPhaseDuration(traffic_light_id, phase_duration)
    traci.trafficlight.setPhase(traffic_light_id, phase_state)


def end_sumo_simulation():
    """
    Gracefully shuts down the TraCI connection and the SUMO simulation.
    This is important for a clean exit!
    """
    print("All done. Closing the SUMO simulation.")
    traci.close()