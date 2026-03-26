import cv2
import time
from datetime import datetime

from recognition.face_recog import load_faces, recognize
from detection.person_detector import detect_person
from alerts.alert_manager import save_unknown
from alerts.video_recorder import start_event, update_event, stop_event
from database.db_manager import init_db, insert_alert
from tracking.tracker import track_detections
from tracking.track_manager import TrackManager


load_faces("known_faces")

track_manager = TrackManager(expire_time=5)

init_db()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not accessible")
    exit()

face_cache = {}
CACHE_TIME = 2

intrusion_active = False
intrusion_image = None
intrusion_name = None


while True:

    success, frame = cap.read()

    if not success:
        break

    detections = detect_person(frame)
    tracks = track_detections(detections)

    for xyxy, track_id in zip(tracks.xyxy, tracks.tracker_id):

        x1, y1, x2, y2 = map(int, xyxy)

        h, w = frame.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        person_crop = frame[y1:y2, x1:x2]

        if person_crop.size == 0:
            continue

        track_manager.update_track(track_id)

        if (
            track_id not in face_cache
            or time.time() - face_cache[track_id][1] > CACHE_TIME
        ):

            names = recognize(person_crop)
            name = names[0] if len(names) > 0 else "Unknown"

            if name == "Unknown":

                if not intrusion_active:

                    intrusion_active = True
                    intrusion_name = name

                    intrusion_image = save_unknown(person_crop)

                    start_event(frame)

                    # print("[INTRUSION] Unknown person detected")

            face_cache[track_id] = (name, time.time())

        name = face_cache[track_id][0]

        color = (0, 255, 0)
        if name == "Unknown":
            color = (0, 0, 255)

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        cv2.putText(
            frame,
            f"{name} (ID {track_id})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    finished_video = update_event(frame)

    if finished_video and intrusion_active:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_alert(
            intrusion_name,
            timestamp,
            intrusion_image,
            finished_video
        )

        # print("[ALERT] Saved after 10 sec recording")

        intrusion_active = False
        intrusion_image = None
        intrusion_name = None

    expired_tracks = track_manager.cleanup()

    for tid in expired_tracks:
        if tid in face_cache:
            del face_cache[tid]

    cv2.imshow("AI Surveillance Camera", frame)

    key = cv2.waitKey(1) & 0xFF

    # MANUAL STOP
    if key == ord('q'):

        finished_video = stop_event()

        if finished_video and intrusion_active:

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            insert_alert(
                intrusion_name,
                timestamp,
                intrusion_image,
                finished_video
            )

            # print("[ALERT] Saved on manual exit")

        break


cap.release()
cv2.destroyAllWindows()