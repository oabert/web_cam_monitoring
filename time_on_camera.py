import cv2
import streamlit as st
from datetime import datetime

st.title('Motion Detector')
start_btn = st.button('Start Camera', key='start')
stop_btn = st.button('Stop Camera', key='stop')

if start_btn:
    streamlit_img = st.image([])

    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.putText(img=frame,
                    text=str(datetime.now().strftime('%A')),
                    org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(20, 100, 200), thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=frame,
                    text=str(datetime.now().strftime('%H:%M:%S')),
                    org=(30,140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2,
                    color=(20, 100, 200), thickness=2, lineType=cv2.LINE_AA)
        # key = cv2.waitKey(1)
        # if key == ord('q'):
        #     break

        streamlit_img.image(frame)
