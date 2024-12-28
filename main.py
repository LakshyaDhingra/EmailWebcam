# Module for opening webcam
import cv2
import time

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
    check, frame = video.read()
    # converted image to gray-frame
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    cv2.imshow("My image", gray_frame_gau)

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
        if cv2.contourArea(contour) < 30000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    cv2.imshow("My image", frame)

    # converted to keyboard key
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
