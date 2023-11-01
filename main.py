import rightcam as rc
import leftcam as lc
import numpy as np
import cv2
import streamlit as st
import sys
import os
import serial
import re
import time
from math import atan2, degrees
import board
import adafruit_mpu6050
# import altair as alt
# import pandas as pd

MASK_LEFT_INNER = 940  # 970
MASK_RIGHT_INNER = 1000  # 1000 #980

MASK_LEFT_OUTER = 750  # 400
MASK_RIGHT_OUTER = 1150  # 1500

LEFT_REF_X = 691  # 874
RIGHT_REF_X = 326  # 901

MM_PER_PX_RIGHT = 0.4674  # 0.2505 #2601
MM_PER_PX_LEFT = 0.4902  # 0.2601 #2505

RIGHT_OUTER_BUFFER = 10
RIGHT_INNER_BUFFER = 10

LEFT_OUTER_BUFFER = 10
LEFT_INNER_BUFFER = 10

GRAPH_LOWER = 1550
GRAPH_UPPER = 2000
REF_GRAPH_LINE = 1676

DISPLAY_MASK = True

i2c = board.I2C()  # uses board.SCL and board.SDA
sensor = adafruit_mpu6050.MPU6050(i2c)

def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle

def get_inclination(_sensor):
    mean_angle_xz = 0
    for n in range(500):
        x, y, z = _sensor.acceleration
        angle_xz = vector_2_degrees(x, z)
        angle_yz = vector_2_degrees(y, z)

        mean_angle_xz = mean_angle_xz + angle_xz
    
    mean_angle_xz = mean_angle_xz/500

    time.sleep(0.5)
    return mean_angle_xz


def process_video():
    LR_REF_DIST = 1215  # 1425 #1315 #1345 #1425 # distance in the plane of rail between reference objects in mm
    LEFT_DIST = 0
    RIGHT_DIST = 0
    avg_listR = []
    avg_listL = []
    # extract frames from video
    # data_log = pd.DataFrame(columns=["x", "Distance"])
    ci = 0

    is_webcam = False
    placeholder = st.empty()
    pl_stop_button = st.empty()

    if not is_webcam:
        vidcapR = cv2.VideoCapture(r"right.mp4")
        vidcapL = cv2.VideoCapture(r"left.mp4")
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    else:
        vidcapR = cv2.VideoCapture(0)  # Right Cam
        vidcapL = cv2.VideoCapture(2)  # Left Cam
        vidcapR.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        vidcapR.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        vidcapL.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        vidcapL.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=10) as ser:
        while success:
            success, imageR = vidcapR.read()
            success, imageL = vidcapL.read()
            right_linelist = rc.right_rail_edge(
                imageR,
                rail_mask_right_inner=MASK_RIGHT_INNER,
                rail_mask_right_outer=MASK_RIGHT_OUTER,
                right_inner_buffer=RIGHT_INNER_BUFFER,
                right_outer_buffer=RIGHT_OUTER_BUFFER,
                disp_mask=DISPLAY_MASK,
            )
            left_linelist = lc.left_rail_edge(
                imageL,
                rail_mask_left_inner=MASK_LEFT_INNER,
                rail_mask_left_outer=MASK_LEFT_OUTER,
                left_inner_buffer=LEFT_INNER_BUFFER,
                left_outer_buffer=LEFT_OUTER_BUFFER,
                disp_mask=DISPLAY_MASK,
            )
            try:
                a1_R, _, _ = right_linelist.shape
                a1_L, _, _ = left_linelist.shape

            except:
                continue

            for i in range(a1_R):
                cv2.line(
                    imageR,
                    (right_linelist[i][0][0], right_linelist[i][0][1]),
                    (right_linelist[i][0][2], right_linelist[i][0][3]),
                    (0, 0, 255),
                    1,
                    cv2.LINE_AA,
                )
                # cv2.line(imageR, (right_linelist[i][0][0], 0), (right_linelist[i][0][0], imageR.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
                avg_listR.append((right_linelist[i][0][0] - RIGHT_REF_X) * MM_PER_PX_RIGHT)
                # print(len(avg_listR))
                if len(avg_listR) > 10:
                    RIGHT_DIST = abs(sum(avg_listR) / len(avg_listR))
                    avg_listR = []
            cv2.namedWindow("Rail Edge Right", cv2.WINDOW_NORMAL)
            cv2.imshow("Rail Edge Right", imageR)
            cv2.waitKey(1)

            for i in range(a1_L):
                cv2.line(
                    imageL,
                    (left_linelist[i][0][0], left_linelist[i][0][1]),
                    (left_linelist[i][0][2], left_linelist[i][0][3]),
                    (0, 0, 255),
                    1,
                    cv2.LINE_AA,
                )
                # cv2.line(imageL, (left_linelist[i][0][0], 0), (left_linelist[i][0][0], imageL.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
                avg_listL.append((left_linelist[i][0][0] - LEFT_REF_X) * MM_PER_PX_LEFT)
                # print(len(avg_listL))
                if len(avg_listL) > 10:
                    LEFT_DIST = abs(sum(avg_listL) / len(avg_listL))
                    avg_listL = []
            cv2.namedWindow("Rail Edge Left", cv2.WINDOW_NORMAL)
            cv2.imshow("Rail Edge Left", imageL)
            cv2.waitKey(1)

            if not len(avg_listR):
                print(LEFT_DIST + RIGHT_DIST + LR_REF_DIST)
                res = LEFT_DIST + RIGHT_DIST + LR_REF_DIST
                # data_log = pd.concat(
                #     [data_log, pd.DataFrame({"x": ci, "Distance": res}, index=["x"])]
                # ).reset_index(drop=True)
                # print(data_log)
                # chart = (
                #     alt.Chart(data_log)
                #     .mark_line()
                #     .encode(
                #         y=alt.Y(
                #             "Distance:Q", scale=alt.Scale(domain=(GRAPH_LOWER, GRAPH_UPPER))
                #         ),
                #         x="x:Q",
                #     )
                # )
                # line = pd.DataFrame(
                #     {
                #         "x": [0, ci],
                #         "Distance": [
                #             REF_GRAPH_LINE,
                #             REF_GRAPH_LINE,
                #         ],  # Referece line plot on screen
                #     }
                # )

                # line_plot = (
                #     alt.Chart(line)
                #     .mark_line(color="red")
                #     .encode(
                #         x="x",
                #         y="Distance",
                #     )
                # )
                # ci = ci + 1
                dist_reading = ser.readline()
                distance = int(re.search(r'\d+', dist_reading).group()) * 0.0296
                print("here")
                inclination = get_inclination(sensor)
                print(distance)
                print(inclination)

                with placeholder.container():
                    st.markdown("Rail Separation: " + str(round(res, 2)))

                    # st.markdown("Chart")
                    # st.altair_chart(chart + line_plot, use_container_width=True)

                pl_stop_button.empty()
                with pl_stop_button.container():
                    if st.button("Stop", key=ci):
                        stop()


def start():
    process_video()


def stop():
    pid = os.getppid()
    os.kill(pid, 9)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Railway Inspection Automation",
    )
    st.title("Railway Inspection Automation")
    if st.button("Start"):
        print("start")
        process_video()
