import cv2
import os
import time

VIDEO_FOLDER = "alerts/videos"
os.makedirs(VIDEO_FOLDER, exist_ok=True)

recording = False
video_writer = None
start_time = 0
current_video_path = None

EVENT_DURATION = 10


def start_event(frame):

    global recording, video_writer, start_time, current_video_path

    if recording:
        return

    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")

    current_video_path = os.path.join(
        VIDEO_FOLDER,
        f"intrusion_{timestamp}.mp4"
    )

    h, w = frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    video_writer = cv2.VideoWriter(
        current_video_path,
        fourcc,
        20,
        (w, h)
    )

    recording = True
    start_time = time.time()

    print(f"[EVENT] Recording started: {current_video_path}")


def update_event(frame):

    global recording, video_writer, start_time, current_video_path

    if not recording:
        return None

    video_writer.write(frame)

    if time.time() - start_time > EVENT_DURATION:

        video_writer.release()

        finished_path = current_video_path

        recording = False
        current_video_path = None

        print(f"[EVENT] Recording finished: {finished_path}")

        return finished_path

    return None