from ultralytics import YOLO
import supervision as sv

model = YOLO("yolov8n.pt")


def detect_person(frame):

    results = model(frame)[0]

    detections = sv.Detections.from_ultralytics(results)

    detections = detections[detections.class_id == 0]

    return detections