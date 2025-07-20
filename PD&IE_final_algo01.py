## Sample Testing Code - Recorded from real time car camera sensor
pip install ultralytics opencv-python deep_sort_realtime

from ultralytics import YOLO
import cv2
from deep_sort_realtime.deepsort_tracker import DeepSort
import numpy as np
import math

# Load YOLOv8 model
model = YOLO('yolov8n.pt')  # 'n' for fast, use 's/m' for more accuracy
# Initialize DeepSORT tracker
tracker = DeepSort(max_age=15)
# Store past trajectories for intent estimation
trajectory_dict = {}

# def estimate_intent(trajectory):
#     if len(trajectory) < 5:
#         return 0.0
#     dx = trajectory[-1][0] - trajectory[0][0]
#     dy = trajectory[-1][1] - trajectory[0][1]
#     angle = math.degrees(math.atan2(dy, dx))
#     # Simple rule: walking toward bottom of frame
#     if 70 <= angle <= 110:
#         return min(1.0, abs(dy)/100)  # normalized probability
#     return 0.0
def estimate_intent(trajectory, frame_height=540):
    if len(trajectory) < 5:
        return 0.0

    x_start, y_start = trajectory[0]
    x_end, y_end = trajectory[-1]

    dx = x_end - x_start
    dy = y_end - y_start
    distance = math.hypot(dx, dy)

    if distance < 10:  # not moving
        return 0.0

    angle = math.degrees(math.atan2(dy, dx))  # 0 = right, 90 = down

    # Broad cone for downward (towards vehicle/camera) movement
    if 45 <= angle <= 135 and dy > 0:
        # Normalize by frame height and clip
        prob = min(1.0, dy / (frame_height * 0.5))
        return round(prob, 2)
    return 0.0

cap = cv2.VideoCapture("ped2.mp4")  # or 0 for webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ✅ Resize the actual frame after it is read
    frame = cv2.resize(frame, (960, 540))  # or (640, 360) for smaller size

    # YOLOv8 detection
    results = model(frame, classes=[0], verbose=False)  # class 0 = person
    detections = []
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf)
            detections.append(([x1, y1, x2 - x1, y2 - y1], conf, 'person'))

    # Tracking
    tracks = tracker.update_tracks(detections, frame=frame)
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        l, t, w, h = track.to_ltrb()
        cx, cy = int((l + w) / 2), int((t + h) / 2)

        # Save trajectory
        trajectory_dict.setdefault(track_id, []).append((cx, cy))
        trajectory_dict[track_id] = trajectory_dict[track_id][-10:]  # limit history

        # Estimate intent
        # prob = estimate_intent(trajectory_dict[track_id])
        prob = estimate_intent(trajectory_dict[track_id], frame.shape[0])

        # Draw
        cv2.rectangle(frame, (int(l), int(t)), (int(w), int(h)), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{track_id} P:{prob:.2f}", (int(l), int(t) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255) if prob > 0.5 else (255, 255, 0), 2)

    cv2.imshow("Pedestrian Intent Estimation", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
