# Don't stop program as soon as object leaves give it some time while it loads
# Module for opening webcam
import os
import cv2
import time
from emailing import send_email
import glob
# To prevent lagging of video and execution of only one function at a time
from threading import Thread

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1


def clean_folder():
    images = glob.glob("images/*.png")
    images.sort()
    for image in images:
        os.remove(image)


while True:
    status = 0
    check, frame = video.read()
    # converted image to gray-frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # This variable will hold on to the first frame and not change with next iterations
    if first_frame is None:
        first_frame = gray_frame_gau

    # Change between 2 frames
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # Creating a threshold which convert new frames to white frames
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # Classifying as a moving object, still face declared as a non-object
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Detecting contours around white areas
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 20000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # Producing images when object comes and goes
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            object_image_index = int(len(all_images)/2)
            object_image = all_images[object_image_index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # Instantiating the thread class for only sending email
        email_thread = Thread(target=send_email, args=(object_image, ))
        email_thread.daemon = True
        email_thread.start()
        email_thread.join(timeout=0.001)

    cv2.imshow("Customer image", frame)

    # converted to keyboard key
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
# Kept at end of the program so images aren't cleared while sending email
clean_folder()
