from ultralytics import YOLO
import cv2
import os
import uuid

# Load model once
model = YOLO("model/best.pt")

def detect_image(image_path):

    os.makedirs("outputs/images", exist_ok=True)

    results = model(image_path)

    annotated_image = results[0].plot()

    filename = f"{uuid.uuid4()}.jpg"

    output_path = os.path.join(
        "outputs/images",
        filename
    )

    cv2.imwrite(output_path, annotated_image)

    return output_path