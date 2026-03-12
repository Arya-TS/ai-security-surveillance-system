import time


class TrackManager:

    def __init__(self, expire_time=5):

        self.tracks = {}

        self.expire_time = expire_time


    def update_track(self, track_id):

        self.tracks[track_id] = time.time()


    def cleanup(self):

        current = time.time()

        expired = []

        for track_id, last_seen in list(self.tracks.items()):

            if current - last_seen > self.expire_time:

                expired.append(track_id)

                del self.tracks[track_id]

        return expired