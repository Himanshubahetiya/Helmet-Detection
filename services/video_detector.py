from ultralytics import YOLO
import cv2
from services.model_loader import model

def detect_video(video_path):

    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(5))

    output_path = "outputs/videos/output.mp4"

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        results = model(frame)

        annotated = results[0].plot()

        writer.write(annotated)

    cap.release()
    writer.release()

    return output_path