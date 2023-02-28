import rightcam as rc

import cv2
import main

def process_video():
    # extract frames from video
    is_webcam = False
    if not is_webcam:
        vidcap = cv2.VideoCapture(r"D:\\railway_proj\\video.mp4")
        success, image = vidcap.read()
    else:
        vidcap = cv2.VideoCapture(0)
        success, image = vidcap.read()
    while success:
        success, image = vidcap.read()
        right_linelist = rc.right_rail_edge(image)
        a1,_,_ = right_linelist.shape
        for i in range(a1):
            cv2.line(image, (right_linelist[i][0][0], right_linelist[i][0][1]), 
            (right_linelist[i][0][2], right_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
            # cv2.line(image, (right_linelist[i][0][0], 0), (right_linelist[i][0][0], image.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
            print((right_linelist[i][0][0]-rc.ref_x)*0.219)
        cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
        cv2.imshow("Rail Edge",image)
        cv2.waitKey(1)


if __name__ == "__main__":
    process_video()
    