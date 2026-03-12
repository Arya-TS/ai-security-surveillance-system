import supervision as sv

tracker = sv.ByteTrack()


def track_detections(detections):

    tracks = tracker.update_with_detections(detections)

    return tracks