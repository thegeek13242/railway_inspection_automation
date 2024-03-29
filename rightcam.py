import cv2
import numpy as np
from otsu import otsu

ref_x = 901


def right_rail_edge(image):
    rail_mask_left = 1105
    
    # image = cv2.imread(path)

    # kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # image = cv2.filter2D(src=image, ddepth=-1, kernel=kernel)

    image = cv2.blur(image, (5,5))

    mask = np.ones(image.shape[:2], dtype="uint8")*255
    cv2.rectangle(mask, (0, 0), (rail_mask_left, 1080), 0, -1)
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

    minR = 99999999
    temp = []
    for x in strlist:
        if (x[0][0] > rail_mask_left+10):
            if (x[0][0] < minR):
                minR = x[0][0]
                temp = x
    strlist = []
    # strlist.append([[minR, 0, minR, image.shape[0]]])
    strlist.append(temp)

    strlist = np.array(strlist)
    return strlist
