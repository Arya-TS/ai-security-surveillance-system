import face_recognition
import os
import cv2

known_encodings = []
known_names = []


def load_faces(folder):
    global known_encodings, known_names

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        image = face_recognition.load_image_file(path)

        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file)[0])

    print("Loaded faces:", known_names)


def recognize(frame):

    if frame is None or frame.size == 0:
        return []

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)

    if len(locations) == 0:
        return []

    encodings = face_recognition.face_encodings(rgb, locations)

    names = []

    for encoding in encodings:

        matches = face_recognition.compare_faces(known_encodings, encoding)

        name = "Unknown"

        if True in matches:
            name = known_names[matches.index(True)]

        names.append(name)

    return names