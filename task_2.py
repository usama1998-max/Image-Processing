import numpy as np
import cv2


def main() -> None:
    bg_img = cv2.imread("brick.jpg")
    gs_img = cv2.imread("greenScreen03.jpg")

    width = 400
    height = 250
    dimensions = (width, height)

    resized_bg = cv2.resize(bg_img, dimensions, interpolation=cv2.INTER_AREA)
    resized_gs = cv2.resize(gs_img, dimensions, interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(resized_gs, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    res = cv2.bitwise_and(resized_gs, resized_gs, mask=mask)

    to_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    fr = resized_gs - res
    f = np.where(fr == 0, resized_bg, fr)

    mask2 = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    nres = cv2.bitwise_and(resized_gs, resized_gs, mask=mask2)
    bw = resized_gs - nres
    b = np.where(bw == 0, to_bgr, bw)

    stack1 = np.concatenate((resized_gs, b), axis=1)
    stack2 = np.concatenate((resized_bg, f), axis=1)

    stack3 = np.concatenate((stack1, stack2), axis=0)

    cv2.imshow("Result", stack3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

