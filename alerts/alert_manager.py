import cv2
import os
import time
from datetime import datetime
from database.db_manager import insert_unknown

ALERT_FOLDER = "alerts/unknown"
os.makedirs(ALERT_FOLDER, exist_ok=True)

last_alert_time = 0
ALERT_COOLDOWN = 10


def save_unknown(frame):

    global last_alert_time

    current_time = time.time()

    if current_time - last_alert_time < ALERT_COOLDOWN:
        return None

    last_alert_time = current_time

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = os.path.join(
        ALERT_FOLDER,
        f"unknown_{timestamp}.jpg"
    )

    cv2.imwrite(filename, frame)

    insert_unknown(timestamp, filename)

    print(f"[ALERT] Unknown face saved: {filename}")

    return filename