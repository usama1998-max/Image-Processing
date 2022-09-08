import numpy as np
import cv2
import argparse
import os


# Numpy for arrays
# cv2 for image processing
# argparse for taking commands from command line
# os for checking if the file exist

# Task One
# This function replaces green screen images with desired background
def task_two(filename, greenScreenFile):
    # For checking if the file exists
    check = [os.path.exists(filename), os.path.exists(greenScreenFile)]

    # Condition if the file does not exist
    if check[0] is False and check[1] is False:
        print("error: No such files")
        return

    # Condition if the green screen file does not exist
    if check[0] is True and check[1] is False:
        print("error: greenScreenFile does not exists!")
        return

    # Condition if the scenic/background file does not exist
    if check[0] is False and check[1] is True:
        print("error: main file does not exists!")
        return

    # Condition if the file is same
    if filename == greenScreenFile:
        print("error: same file!")
        return

    # reading Both files
    bg_img = cv2.imread(filename)
    gs_img = cv2.imread(greenScreenFile)

    # Setting the width and height
    # Note: setting the width and height is important because some images may be small or too large !
    width = 400
    height = 250
    dimensions = (width, height)

    # Resizing the images
    resized_bg = cv2.resize(bg_img, dimensions, interpolation=cv2.INTER_AREA)
    resized_gs = cv2.resize(gs_img, dimensions, interpolation=cv2.INTER_AREA)

    # Converting the resized image from BGR to HSV
    hsv = cv2.cvtColor(resized_gs, cv2.COLOR_BGR2HSV)

    # This function is for checking if the desired color exists in range
    mask = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    # This function removes the desired color
    res = cv2.bitwise_and(resized_gs, resized_gs, mask=mask)

    # Converting the output into grayscale
    to_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # subtracting the masked image from the original one
    fr = resized_gs - res
    f = np.where(fr == 0, resized_bg, fr)

    # For checking if the desired color is in range
    mask2 = cv2.inRange(hsv, (36, 25, 25), (70, 255, 255))

    # this function subtract green background and adds subject to white background
    nres = cv2.bitwise_and(resized_gs, resized_gs, mask=mask2)
    bw = resized_gs - nres
    b = np.where(bw == 0, to_bgr, bw)

    # For Stacking all images
    stack1 = np.concatenate((resized_gs, b), axis=1)
    stack2 = np.concatenate((resized_bg, f), axis=1)

    stack3 = np.concatenate((stack1, stack2), axis=0)

    cv2.imshow("Result", stack3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Task One
# This functions takes image as an input and displays the output in different channels
def task_one(filename, option):
    # for checking if the file exist
    check = os.path.exists(filename)

    if check is False:
        print("No such file")
        return

    # Reading file if check is True
    color_img = cv2.imread(filename)

    # Setting the width and height
    # Note: it is necessary to set the width and height because some image may be too large or too small
    width = 400
    height = 250
    dimensions = (width, height)

    # Resizing
    resized_img = cv2.resize(color_img, dimensions, interpolation=cv2.INTER_AREA)

    # Converting the file into different Color Spaces
    img_xyz = cv2.cvtColor(resized_img, cv2.COLOR_BGR2XYZ)
    img_ycrcb = cv2.cvtColor(resized_img, cv2.COLOR_BGR2YCR_CB)
    img_Lab = cv2.cvtColor(resized_img, cv2.COLOR_BGR2LAB)
    img_hsv = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)

    # Separating the color spaces into separate channels
    Z, Y, X = cv2.split(img_xyz)
    y, Cr, Cb = cv2.split(img_ycrcb)
    L, a, b = cv2.split(img_Lab)
    h, s, v = cv2.split(img_hsv)

    # Storing those channels in a dictionary for accessing
    color_spaces = {
        "XYZ": [X, Y, Z],
        "Lab": [L, a, b],
        "YCrCb": [y, Cr, Cb],
        "HSV": [h, s, v]
    }

    # Accessing the channels
    cs = color_spaces[option]

    # if there is no such color space in the dictionary
    if cs is None:
        print("No such option!")
        return

    # Converting those images in grayscale
    c1_rgb = cv2.cvtColor(cs[0], cv2.COLOR_GRAY2BGR)
    c2_rgb = cv2.cvtColor(cs[1], cv2.COLOR_GRAY2BGR)
    c3_rgb = cv2.cvtColor(cs[2], cv2.COLOR_GRAY2BGR)

    # Stacking images togather
    stack1 = np.hstack([resized_img, c1_rgb])
    stack2 = np.hstack([c2_rgb, c3_rgb])
    stack3 = np.vstack([stack1, stack2])

    cv2.imshow("Output", stack3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main() -> None:
    # Argument parser for accepting filename or options from terminal
    chroma_key_parser = argparse.ArgumentParser(
        description="__OPENCV___\nNote: provide background image first then green screen image in second!")

    # all options that you can apply
    chroma_key_parser.add_argument('-XYZ', action="store_true", help="Converts image to XYZ color space")
    chroma_key_parser.add_argument('-HSV', action="store_true", help="Converts image to HSV color space")
    chroma_key_parser.add_argument('-YCrCb', action="store_true", help="Converts image to YCrCb color space")
    chroma_key_parser.add_argument('-Lab', action="store_true", help="Converts image to Lab color space")
    chroma_key_parser.add_argument('filename', action="store", nargs="*",
                                   help="Enter background file first and green screen second")

    # Stores the arguments
    args = chroma_key_parser.parse_args()

    # for checking if the option is called
    option_called = False

    # Converting arguments into dict
    arguments = vars(args)

    # for checking which option is true
    for k, v in arguments.items():
        if v is True:
            task_one(arguments['filename'][0], k)
            option_called = True
            break

    # if option is not there then it will run this function but green screen file will be required
    if option_called is False:
        # this condition helps to check if the green screen file is present
        # Both files are stored in a list and the length becomes 2
        if len(arguments['filename']) < 2:
            print("error: Green Screen file Missing!")
            return
        task_two(arguments['filename'][0], arguments['filename'][1])
        return


if __name__ == "__main__":
    main()
