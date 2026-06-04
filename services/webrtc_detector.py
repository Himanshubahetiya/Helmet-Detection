from ultralytics import YOLO
from streamlit_webrtc import VideoProcessorBase
import av
import cv2
import os
from services.model_loader import model

os.makedirs("outputs/videos", exist_ok=True)

LIVE_CACHE_FILE = "outputs/videos/live_helmet_detection_log.mp4"


class HelmetVideoProcessor(VideoProcessorBase):

    def __init__(self):
        self.out = None

        try:
            if os.path.exists(LIVE_CACHE_FILE):
                os.remove(LIVE_CACHE_FILE)
        except:
            pass

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        results = model(img, verbose=False)

        annotated_frame = results[0].plot()

        if self.out is None:

            h, w, _ = annotated_frame.shape

            fourcc = cv2.VideoWriter_fourcc(*"mp4v")

            self.out = cv2.VideoWriter(
                LIVE_CACHE_FILE,
                fourcc,
                20.0,
                (w, h)
            )

        self.out.write(annotated_frame)

        return av.VideoFrame.from_ndarray(
            annotated_frame,
            format="bgr24"
        )

    def __del__(self):

        try:
            if self.out is not None:
                self.out.release()
        except:
            pass