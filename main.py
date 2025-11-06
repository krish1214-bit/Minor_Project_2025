import cv2
from vehicle_detection import find_vehicles_in_frame  # Assumes your YOLO wrapper is in vehicle_detection.py

IMAGE_PATH = r"C:\Users\Krish Setiya\Downloads\sample image.png"

# divide into ROIs 
LANE_ROIS = [
    (0, 0, 213, 480),     # Lane 1 (left)
    (213, 0, 427, 480),   # Lane 2 (center)
    (427, 0, 640, 480)    # Lane 3 (right)
]

MIN_GREEN_DURATION = 5
MAX_GREEN_DURATION = 15
MAX_VEHICLE_COUNT = 20

def calculate_green_duration(vehicle_count):
    duration = MIN_GREEN_DURATION + (MAX_GREEN_DURATION - MIN_GREEN_DURATION) * (vehicle_count / MAX_VEHICLE_COUNT)
    return max(MIN_GREEN_DURATION, min(duration, MAX_GREEN_DURATION))

def main():
    frame = cv2.imread(IMAGE_PATH)
    if frame is None:
        print("Error: Could not read the image.")
        return

    vehicle_counts = []
    vehicle_boxes_per_lane = []

    # Vehicle detection for each lane
    for (x1, y1, x2, y2) in LANE_ROIS:
        roi = frame[y1:y2, x1:x2]
        count, boxes = find_vehicles_in_frame(roi)
        boxes = [[b[0] + x1, b[1] + y1, b[2] + x1, b[3] + y1] for b in boxes]
        vehicle_counts.append(count)
        vehicle_boxes_per_lane.append(boxes)

    green_lane_index = vehicle_counts.index(max(vehicle_counts)) if vehicle_counts else -1
    green_durations = [calculate_green_duration(count) for count in vehicle_counts]

    for lane_index, boxes in enumerate(vehicle_boxes_per_lane):
        box_color = (0, 255, 0) if lane_index == green_lane_index else (0, 0, 255)

        for box in boxes:
            cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), box_color, 2)

        signal_text = "GREEN" if lane_index == green_lane_index else "RED"
        duration_text = f"{green_durations[lane_index]:.1f}s" if lane_index == green_lane_index else ""
        cv2.putText(frame, f"{signal_text} {duration_text} Vehicles: {vehicle_counts[lane_index]}",
                    (30, 50 + lane_index * 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, box_color, 2)

    cv2.imshow("Smart Traffic Light - Lane Density and Timings", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # After detection and visualization
    print("\n================= TRAFFIC DENSITY REPORT =================")
    for idx, duration in enumerate(green_durations):
        if idx == green_lane_index:
            print(f"Lane {idx + 1}: {vehicle_counts[idx]} vehicles → GREEN for {duration:.1f} seconds")
        else:
            print(f"Lane {idx + 1}: {vehicle_counts[idx]} vehicles → RED")
    print("==========================================================\n")


if __name__ == "__main__":
    main()
