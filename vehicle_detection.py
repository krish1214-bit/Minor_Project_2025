from ultralytics import YOLO
import numpy as np

yolo_model = YOLO("yolov8n.pt")  # Make sure this path and weights are accessible

def find_vehicles_in_frame(image):
    # Run YOLO inference
    results = yolo_model(image, stream=True, verbose=False)
    vehicle_class_ids = [2, 3, 5, 7]  # car, motorcycle, bus, truck (COCO dataset classes)
    vehicle_count = 0
    vehicle_boxes = []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy().astype(int)
        class_ids = result.boxes.cls.cpu().numpy().astype(int)
        for box, cls_id in zip(boxes, class_ids):
            if cls_id in vehicle_class_ids:
                vehicle_count += 1
                vehicle_boxes.append(box)
    return vehicle_count, vehicle_boxes
