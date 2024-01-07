import time
import cv2
import glob
import os
from emailing import send_email
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1


def clean_folder():
    imgs = glob.glob('images/*.png')
    for img in imgs:
        os.remove(img)


while True:
    status = 0
    check, frame = video.read()

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = grey_frame_gau

    delta_frame = cv2.absdiff(first_frame, grey_frame_gau)

    thresh_frame = cv2.threshold(delta_frame, 35, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any:
            status = 1
            cv2.imwrite(f'images/{count}.png', frame)
            count = count + 1
            all_imgs = glob.glob('images/*.png')
            index = int(len(all_imgs) / 2)
            img_with_object = all_imgs[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        images_to_delete = glob.glob("images/*.png")
        images_to_delete.sort()
        for image in images_to_delete:
            if image != img_with_object:
                os.remove(image)

        email_thread = Thread(target=send_email, args=(img_with_object,))
        email_thread.daemon = True
        email_thread.start()
        email_thread.join()  # Wait for email_thread to finish before proceeding

        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        # clean image thread
        clean_thread.start()

        # send_email(img_with_object)
        # clean_folder()

    cv2.imshow('Video', frame)

    # exit from camera
    key = cv2.waitKey(1)
    if key == ord('q'):
        break


video.release()
