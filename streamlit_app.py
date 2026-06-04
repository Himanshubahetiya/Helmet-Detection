import streamlit as st
import os
from services.image_detector import detect_image
from services.video_detector import detect_video
from streamlit_webrtc import webrtc_streamer
from services.webrtc_detector import HelmetVideoProcessor

os.makedirs("uploads/images", exist_ok=True)
os.makedirs("uploads/videos", exist_ok=True)

os.makedirs("outputs/images", exist_ok=True)
os.makedirs("outputs/videos", exist_ok=True)

st.set_page_config(
    page_title="Helmet Detection",
    page_icon="🪖",
    layout="wide"
)

st.title("🪖 Helmet Detection System")

option = st.sidebar.selectbox(
    "Select Detection Type",
    [
        "Image Detection",
        "Video Detection",
        "Live Webcam Detection"
    ]
)


# ---------------- IMAGE ---------------- #

if option == "Image Detection":

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        upload_path = os.path.join(
            "uploads/images",
            uploaded_file.name
        )

        with open(upload_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.image(upload_path, width=400)

        if st.button("Detect Helmet"):

            output_path = detect_image(upload_path)

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    upload_path,
                    caption="Original",
                    width=350
                )

            with col2:
                st.image(
                    output_path,
                    caption="Detected",
                    width=350
                )

# ---------------- VIDEO ---------------- #

elif option == "Video Detection":

    uploaded_video = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov"]
    )

    if uploaded_video:

        video_path = os.path.join(
            "uploads/videos",
            uploaded_video.name
        )

        with open(video_path, "wb") as f:
            f.write(uploaded_video.getbuffer())

        st.subheader("Original Video")

        st.video(video_path)

        if st.button("Detect Video"):

            with st.spinner(
                "Processing Video... Please Wait"
            ):

                output_path = detect_video(video_path)

            st.success(
                "Video Detection Completed"
            )

            st.subheader("Detected Video")

            st.video(output_path)

            with open(output_path, "rb") as file:

                st.download_button(
                    label="⬇ Download Result",
                    data=file,
                    file_name=os.path.basename(
                        output_path
                    ),
                    mime="video/mp4"
                )
                
elif option == "Live Webcam Detection":

    st.subheader("🎥 Live Helmet Detection")

    st.info(
        "Click START and allow camera permission."
    )

    webrtc_streamer(
        key="helmet-detection",
        video_processor_factory=HelmetVideoProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )