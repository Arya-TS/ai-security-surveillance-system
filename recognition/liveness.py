import mediapipe as mp
import numpy as np
import cv2

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# Eye landmark indices
LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]


def eye_aspect_ratio(eye):

    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])

    ear = (A + B) / (2.0 * C)

    return ear


def detect_blink(frame):

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if not results.multi_face_landmarks:
        return False

    landmarks = results.multi_face_landmarks[0].landmark

    h, w, _ = frame.shape

    left_eye = []
    right_eye = []

    for idx in LEFT_EYE:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        left_eye.append([x,y])

    for idx in RIGHT_EYE:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        right_eye.append([x,y])

    left_eye = np.array(left_eye)
    right_eye = np.array(right_eye)

    left_ear = eye_aspect_ratio(left_eye)
    right_ear = eye_aspect_ratio(right_eye)

    ear = (left_ear + right_ear) / 2

    BLINK_THRESHOLD = 0.20

    if ear < BLINK_THRESHOLD:
        return True

    return False