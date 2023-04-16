import cv2
import numpy as np
from otsu import otsu

ref_x = 874


def left_rail_edge(image):
    rail_mask_left = 730


    # image = cv2.imread(path)

    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

    image = cv2.blur(image, (5,5))

    mask = np.ones(image.shape[:2], dtype="uint8")*255
    cv2.rectangle(mask, (rail_mask_left, 0), (1920,1080), 0, -1)
    image = cv2.bitwise_and(image, image, mask=mask)
    # cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
    # cv2.imshow("Display", image)
    # cv2.waitKey(0)

    is_reduce_noise = 1
    is_normalized = 1

    threshold = otsu(image, is_reduce_noise, is_normalized)
    edges = cv2.Canny(image=image, threshold1=threshold /
                      2, threshold2=threshold)

    minLineLength = 100

    lines = cv2.HoughLinesP(image=edges, rho=1.4, theta=np.pi/180, threshold=int(
        threshold), lines=np.array([]), minLineLength=minLineLength, maxLineGap=15)
    a, b, c = lines.shape
    l = lines.tolist()

    # Only straight lines are considered
    strlist = []
    for x in l:
        angle = np.arctan2(x[0][3] - x[0][1], x[0][2] - x[0][0]) * 180. / np.pi
        # print(f"angle of {x} is {angle}")
        # if ((85 <= angle <= 95) or (-95 <= angle <= -85)):
        if ((89 <= angle <= 91) or (-91 <= angle <= -89)):
            # print(f"{x} is added to list")
            strlist.append(x)

    maxL = 0
    temp = []
    for x in strlist:
        if (x[0][0] < rail_mask_left-10):
            if (x[0][0] > maxL):
                maxL = x[0][0]
                temp = x
    strlist = []
    # strlist.append([[minR, 0, minR, image.shape[0]]])
    strlist.append(temp)

    strlist = np.array(strlist)
    # print(strlist)
    # print((minR-maxL)*calibFactor)
    try:
        a1, b1, c1 = strlist.shape
    except:
        return None
    # for i in range(a):
    #     cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
    for i in range(a1):
        cv2.line(image, (strlist[i][0][0], strlist[i][0][1]), (strlist[i]
                                                               [0][2], strlist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
    cv2.namedWindow("Rail Edge Left", cv2.WINDOW_NORMAL)
    cv2.imshow("Rail Edge Left", image)
    cv2.waitKey(1)
    # image = cv2.resize(image, (int(3840/2), int(2160/2)))
    # cv2.namedWindow("HoughLines", cv2.WINDOW_NORMAL)
    # cv2.imwrite('final.jpg', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return strlist

# def process_video():
#     avg_list = []
#     # extract frames from video
#     is_webcam = False
#     if not is_webcam:
#         vidcap = cv2.VideoCapture(r"D:\\railway_proj\\railway_inspection_automation\\left.mp4")
#         success, image = vidcap.read()
#     else:
#         vidcap = cv2.VideoCapture(1)
#         success, image = vidcap.read()
#     while success:
#         success, image = vidcap.read()
#         right_linelist = right_rail_edge(image)
#         try:
#             a1, _, _ = right_linelist.shape
#         except:
#             continue
#         for i in range(a1):
#             cv2.line(image, (right_linelist[i][0][0], right_linelist[i][0][1]),
#                      (right_linelist[i][0][2], right_linelist[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
#             # cv2.line(image, (right_linelist[i][0][0], 0), (right_linelist[i][0][0], image.shape[0]), (0, 0, 255), 1, cv2.LINE_AA)
#             avg_list.append(abs(right_linelist[i][0][0]-ref_x)*0.219)
#             print(len(avg_list))
#             if(len(avg_list)>10):
#                 print(sum(avg_list)/len(avg_list))
#                 avg_list = []
#             # print((right_linelist[i][0][0]-rc.ref_x)*0.219)
#         # cv2.namedWindow("Rail Edge", cv2.WINDOW_NORMAL)
#         # cv2.imshow("Rail Edge", image)
#         # cv2.waitKey(1)


# if __name__ == "__main__":
#     process_video()