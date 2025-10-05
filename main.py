import time
import traci
from vehicle_detection import detect_vehicles
from ai_decision_engine import calculate_green_timings
from sumo_integration import launch_sumo_simulation, get_current_vehicle_counts, update_traffic_light_timings, \
    end_sumo_simulation

# The path to your SUMO configuration file. You'll need to make sure this is correct.
SUMO_CONFIG_FILE = "sumo_config/basic_sumo.sumocfg"

# IDs for the traffic light and lanes we'll be monitoring. These need to match
# the IDs defined in your SUMO XML files.
TRAFFIC_LIGHT_ID = "0"
LANE_IDS = ["lane_id_1", "lane_id_2"]  # Placeholder lane IDs


def main():
    try:
        launch_sumo_simulation(SUMO_CONFIG_FILE)

        # This is our main simulation loop. It's designed to mimic a real-world
        # traffic control system, stepping through time and making decisions.

        step_counter = 0
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()
            step_counter += 1

            # Here's where the magic happens! In a real-world project, you'd
            # connect to a live camera feed and use a model like YOLO to count
            # the vehicles. For this simulation, we're using TraCI's built-in
            # function to get the vehicle counts.
            # (e.g., using a video feed placeholder:
            # ret, frame = cap.read()
            # if ret:
            #     vehicle_count_lane1, _ = detect_vehicles(frame) )

            current_vehicle_counts = get_current_vehicle_counts(LANE_IDS)

            # Pass the live data to our smart decision-making function.
            new_timings = calculate_green_timings(current_vehicle_counts)

            # Now, we apply the new timings to the traffic lights in the simulation.
            # This is a simplified two-phase example. For a more complex intersection,
            # you'd need a more robust phase management system (e.g., handling yellow lights).
            update_traffic_light_timings(TRAFFIC_LIGHT_ID, new_timings[LANE_IDS[0]], "GGrr")
            update_traffic_light_timings(TRAFFIC_LIGHT_ID, new_timings[LANE_IDS[1]], "rGGr")

            # A friendly log message to keep track of what's happening.
            print(
                f"Time Step: {step_counter} | Traffic Update: Lane counts are {current_vehicle_counts}. New green light durations are {new_timings}.")

            # Pausing for a moment to make the simulation visible and easier to follow.
            time.sleep(1)


    except traci.exceptions.TraCIException as e:
        print(
            f"An error occurred with TraCI. Did you make sure SUMO is installed and the path is correct? Error details: {e}")
    finally:
        # Always remember to close the simulation gracefully!
        end_sumo_simulation()


if __name__ == "__main__":
    main()