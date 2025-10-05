from ultralytics import YOLO
import cv2

# We're loading a pre-trained YOLOv8 model from Ultralytics.
# 'yolov8n.pt' is a great choice because it's fast and lightweight,
# perfect for real-time applications like this!
# The model file will download automatically the first time you run the code.
yolo_model = YOLO("yolov8n.pt")


def find_vehicles_in_frame(video_frame):
    """
    Uses the YOLOv8 model to scan a single video frame and identify
    and count all the vehicles.

    Args:
        video_frame (np.array): The raw image data of a single video frame.

    Returns:
        tuple: A tuple containing:
               - The total number of vehicles detected (int).
               - A list of bounding box coordinates for each detected vehicle (list).
    """
    # The `stream=True` argument makes the detection process more memory-efficient,
    # which is crucial for processing video streams.
    detection_results = yolo_model(video_frame, stream=True)

    vehicle_count = 0
    vehicle_bounding_boxes = []

    # The COCO dataset, which YOLOv8 was trained on, uses specific IDs for different
    # types of vehicles. We're only interested in these ones.
    # car: 2, motorcycle: 3, bus: 5, truck: 7
    vehicle_class_ids = [2, 3, 5, 7]

    for result in detection_results:
        # Grabbing the coordinates of the detected objects and their class IDs.
        boxes = result.boxes.xyxy.cpu().numpy().astype(int)
        class_ids = result.boxes.cls.cpu().numpy().astype(int)

        for box, class_id in zip(boxes, class_ids):
            # Checking if the detected object is one of our target vehicle types.
            if class_id in vehicle_class_ids:
                vehicle_count += 1
                vehicle_bounding_boxes.append(box)

    return vehicle_count, vehicle_bounding_boxes