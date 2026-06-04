from ultralytics import YOLO
from streamlit_webrtc import VideoProcessorBase
import av

# Load model only once
model = YOLO("model/best.pt")


class HelmetVideoProcessor(VideoProcessorBase):

    def recv(self, frame):

        # Convert frame to numpy array
        img = frame.to_ndarray(format="bgr24")

        # YOLO prediction
        results = model(img, verbose=False)

        # Draw bounding boxes
        annotated_frame = results[0].plot()

        # Return processed frame
        return av.VideoFrame.from_ndarray(
            annotated_frame,
            format="bgr24"
        )