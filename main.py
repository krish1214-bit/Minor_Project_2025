import cv2
from vehicle_detection import find_vehicles_in_frame
from ai_decision_engine import calculate_green_timings
import os

# To test with a video file, replace the path below. For webcam, use 0.
# For a single image, provide the image path.
#SOURCE = "path/to/your/test_video.mp4"


# SOURCE = 0  # Use this for a live webcam feed
SOURCE = r""C:\Users\Krish Setiya\Downloads\sample image.png""

def draw_detection_results(frame, vehicle_boxes, vehicle_count):
    """
    Draws bounding boxes and a vehicle count on the frame.
    This is a helper function for visualizing the results.
    """
    for box in vehicle_boxes:
        # Drawing a rectangle for each detected vehicle.
        # The coordinates are [x_min, y_min, x_max, y_max].
        x1, y1, x2, y2 = box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box

    # Displaying the vehicle count on the top-left corner.
    cv2.putText(frame, f"Vehicle Count: {vehicle_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                2)  # Red text


def main():
    if isinstance(SOURCE, str) and os.path.isfile(SOURCE) and SOURCE.endswith(('.jpg', '.jpeg', '.png')):
        # --- Handle single image input ---
        frame = cv2.imread(SOURCE)
        if frame is None:
            print("Error: Could not read image.")
            return

        vehicle_count, vehicle_boxes = find_vehicles_in_frame(frame)
        draw_detection_results(frame, vehicle_boxes, vehicle_count)

        cv2.imshow("Smart Traffic Light - Detection Test", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    else:
        # --- Handle video or webcam input ---
        cap = cv2.VideoCapture(SOURCE)
        if not cap.isOpened():
            print("Error: Could not open video source.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("End of video stream or error.")
                break

            vehicle_count, vehicle_boxes = find_vehicles_in_frame(frame)
            draw_detection_results(frame, vehicle_boxes, vehicle_count)

            cv2.imshow("Smart Traffic Light - Detection Test", frame)

            # Press 'q' to exit the video stream.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
