import rightcam as rc
import leftcam as lc
import cv2


def process_video():
    avg_listR = []
    avg_listL = []
    # extract frames from video
    is_webcam = True
    if not is_webcam:
        vidcapR = cv2.VideoCapture(r"D:\\railway_proj\\railway_inspection_automation\\right.mp4")
        vidcapL = cv2.VideoCapture(r"D:\\railway_proj\\railway_inspection_automation\\left.mp4")
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    else:
        vidcapR = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        vidcapL = cv2.VideoCapture(2,cv2.CAP_DSHOW)
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
    while success:
        success, imageR = vidcapR.read()
        success, imageL = vidcapL.read()
        right_linelist = rc.right_rail_edge(imageR)
        left_linelist = lc.left_rail_edge(imageL)
        try:
            a1_R, _, _ = right_linelist.shape
            a1_L, _, _ = left_linelist.shape

        except:
            continue
        for i in range(a1_R):
            cv2.line(imageR, (right_linelist[i][0][0], right_linelist[i][0][1]),
                     (right_linelist[i][0][2], right_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
            # cv2.line(imageR, (right_linelist[i][0][0], 0), (right_linelist[i][0][0], imageR.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
            avg_listR.append((right_linelist[i][0][0]-rc.ref_x)*0.219)
            print(len(avg_listR))
            if(len(avg_listR)>10):
                print(sum(avg_listR)/len(avg_listR))
                avg_listR = []
        for i in range(a1_L):
            cv2.line(imageL, (left_linelist[i][0][0], left_linelist[i][0][1]),
                     (left_linelist[i][0][2], left_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
            # cv2.line(imageL, (left_linelist[i][0][0], 0), (left_linelist[i][0][0], imageL.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
            avg_listL.append((left_linelist[i][0][0]-lc.ref_x)*0.219)
            print(len(avg_listL))
            if(len(avg_listL)>10):
                print(sum(avg_listL)/len(avg_listL))
                avg_listL = []
        # cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
            # print((right_linelist[i][0][0]-rc.ref_x)*0.219)
        # cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
        # cv2.imshow("Rail Edge", imageR)
        # cv2.waitKey(1)


if __name__ == "__main__":
    print("start")
    process_video()
