import cv2
import numpy as np

#===================To read the Image===========================
img = cv2.imread("Test_Images/Image1.png")
# text_in_image = loaded_img[:25, :, :]
# img = loaded_img[25:, :, :]
#===============================================================


#=================Some Important Opertions on Image=============
# imgBlur = cv2.GaussianBlur(img, (1, 1), 0)
resized_image = cv2.resize(img, (400, 400)) 
imgAvgBlur = cv2.blur(resized_image,(2,2))
imgBlur = cv2.GaussianBlur(imgAvgBlur, (7, 7), 1)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#===============================================================


#=============Setting the Hue-Saturation-Value of Image=========

def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)  # in opencv, hue has a maximum value of 179
cv2.createTrackbar("Hue Max", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 0, 255, empty)

while True:
    # img = cv2.imread('3.png')
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    # first argument --> name of slide
    # second argument --> name of trackbar window
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    # We got the minimum and maximum values, now we have to apply them to our image
    # let's create a mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)
    # we get some values of lower and upper that are perfectly applied to our image
    # then we added those values to the createTrackbar

    # now let's use a function to get colored image
    imgResult = cv2.bitwise_and(resized_image, resized_image, mask=mask)

    cv2.imshow("Resulted image", imgResult)
    cv2.imshow("HSV image", imgHSV)
    cv2.imshow("masked image", mask)

    cv2.waitKey(1)
#===============================================================
