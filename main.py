import rightcam as rc
import leftcam as lc
import numpy as np
import cv2

import queue
import threading
import streamlit as st


MASK_LEFT_INNER = 940 #970
MASK_RIGHT_INNER = 1000 #980

MASK_LEFT_OUTER = 630
MASK_RIGHT_OUTER = 1224

LEFT_REF_X = 1379 #874
RIGHT_REF_X = 607 #901

MM_PER_PX_RIGHT = 0.2505 #2601
MM_PER_PX_LEFT = 0.2601 #2505

DISPLAY_MASK = False
DISPLAY_IMAGE = False


def process_video(q):
    LR_REF_DIST = 1425 # distance in the plane of rail between reference objects in mm
    LEFT_DIST = 0
    RIGHT_DIST = 0
    avg_listR = []
    avg_listL = []
    # extract frames from video
    
    is_webcam = False

    if not is_webcam:
        vidcapR = cv2.VideoCapture(r"right.mp4")
        vidcapL = cv2.VideoCapture(r"left.mp4")
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    else:
        vidcapR = cv2.VideoCapture(0) # Right Cam
        vidcapL = cv2.VideoCapture(2) # Left Cam
        vidcapR.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        vidcapR.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        vidcapL.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        vidcapL.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    while success:
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
        right_linelist = rc.right_rail_edge(imageR, rail_mask_right_inner=MASK_RIGHT_INNER, rail_mask_right_outer=MASK_RIGHT_OUTER, disp_mask=DISPLAY_MASK)
        left_linelist = lc.left_rail_edge(imageL, rail_mask_left_inner=MASK_LEFT_INNER, rail_mask_left_outer=MASK_LEFT_OUTER, disp_mask=DISPLAY_MASK)
        try:
            a1_R, _, _ = right_linelist.shape
            a1_L, _, _ = left_linelist.shape

        except:
            continue

        for i in range(a1_R):
            cv2.line(imageR, (right_linelist[i][0][0], right_linelist[i][0][1]),
                     (right_linelist[i][0][2], right_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
            # cv2.line(imageR, (right_linelist[i][0][0], 0), (right_linelist[i][0][0], imageR.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
            avg_listR.append((right_linelist[i][0][0]-RIGHT_REF_X)*MM_PER_PX_RIGHT)
            # print(len(avg_listR))
            if(len(avg_listR)>10):
                RIGHT_DIST = abs(sum(avg_listR)/len(avg_listR))
                avg_listR = []
        if DISPLAY_IMAGE:
            cv2.namedWindow("Rail Edge Right", cv2.WINDOW_NORMAL)
            cv2.imshow("Rail Edge Right", imageR)
            cv2.waitKey(1)

        for i in range(a1_L):
            cv2.line(imageL, (left_linelist[i][0][0], left_linelist[i][0][1]),
                     (left_linelist[i][0][2], left_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
            # cv2.line(imageL, (left_linelist[i][0][0], 0), (left_linelist[i][0][0], imageL.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
            avg_listL.append((left_linelist[i][0][0]-LEFT_REF_X)*MM_PER_PX_LEFT)
            # print(len(avg_listL))
            if(len(avg_listL)>10):
                LEFT_DIST = abs(sum(avg_listL)/len(avg_listL))
                avg_listL = []
        if DISPLAY_IMAGE:
            cv2.namedWindow("Rail Edge Left", cv2.WINDOW_NORMAL)
            cv2.imshow("Rail Edge Left", imageL)
            cv2.waitKey(1)
        print(LEFT_DIST+RIGHT_DIST+LR_REF_DIST)
        # cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
            # print((right_linelist[i][0][0]-rc.ref_x)*0.219)
        # cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
        # cv2.imshow("Rail Edge", imageR)
        # cv2.waitKey(1)
        q.put((cv2.hconcat(imageL,imageR),LEFT_DIST+RIGHT_DIST+LR_REF_DIST))


# if __name__ == "__main__":
#     print("start")
#     process_video()

def start_video():
    global started
    if started:
        return
    global q, t
    q = queue.Queue()
    t = threading.Thread(target=process_video, args=(q,))
    t.daemon = True
    t.start()
    started = True

def get_video():
    start_video()
    return q.get()

def stop_video():
    t.join()



if __name__ == "__main__":
    started = False
    q = queue.Queue()

    st.write("Distance: ")
    output = st.empty()

    while True:
        value = get_video()
        st.write(value[1])
        st.image(value[0], channels="RGB")
        st.empty()
