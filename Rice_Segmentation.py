import cv2
import numpy as np
import glob
import os
from os import listdir



#================Blur-GrayScale-HSV=============================
def Blur_Gray_HSV(img, min_hue, max_hue, min_sat, max_sat, min_val, max_val):
    #=================Some Important Opertions on Image======
    imgAvgBlur = cv2.blur(img,(2,2))
    imgBlur = cv2.GaussianBlur(imgAvgBlur, (7, 7), 2)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgBlank = np.ones_like(img)*255
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    imgContour = img.copy()
    #========================================================

    #=====Making a mask using Hue-Saturation-Value of image==
    # Hue and Saturation have almost zero effect in creating the mask
    # However the mask solely depends on the Value
    # Value = 246 gives the best mask for these type of images
    lower_limit = np.array([min_hue, min_sat, min_val])
    upper_limit = np.array([max_hue, max_sat, max_val])
    final_mask = cv2.inRange(imgHSV, lower_limit, upper_limit)
    #========================================================
    # Corners are detected using algorithm called Canny Edge Detector
    # Lower and Upper thresholds, aperutre size and gradient values are carefully chosen
    # that best suit the given scenario
    imgCorner = cv2.Canny(final_mask, 50, 80, apertureSize=5, L2gradient = True)
    # cv2.imshow('', imgCorner)
    # cv2.waitKey(0)
    return imgGray, imgBlank, imgContour, final_mask, imgCorner
#===============================================================


#================Dilation-Erosion-Addition======================
# A copy of the image is made containing the main drop. 
# This main drop is then dilated so that noise, and peculiar curves of the frop can be removed
# Now this drop is eroded so that it can attain its origina dimensions
# This processed image is then added to original one
def dilated_eroded_added(imgDEA, imgCornerDEA, final_maskDEA):
    ret = False
    contours, hierarchy = cv2.findContours(imgCornerDEA, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt1 in contours:
        imgBlankBlack = np.zeros_like(imgDEA)
        imgBlankBlack = cv2.cvtColor(imgBlankBlack, cv2.COLOR_BGR2GRAY)
        area = cv2.contourArea(cnt1)
        if area > 1000:
            cv2.drawContours(imgBlankBlack, cnt1, -1, (255, 255, 255), 3)
            cv2.fillPoly(imgBlankBlack, pts =[cnt1], color=(255,255,255))

            kernel = np.ones((2,2),np.uint8)
            final_mask_improved = cv2.dilate(imgBlankBlack,kernel,iterations = 5)
    
            kernel2 = np.ones((3,3),np.uint8)
            erosion = cv2.erode(final_mask_improved,kernel2,iterations = 7)
            
            final_mask2 = final_maskDEA + erosion
            
            imgCorner2 = cv2.Canny(final_mask2, 40, 40)
            ret = True
    if ret == True:  
        return imgCorner2, final_mask2
    else:
        return None, None
#===============================================================


#===================Contours-Colors-Text=========================
def get_contours (imgGC, imgContourGC, imgBlankGC, success_check, colorr, text1, text2):

    full = 0
    broken = 0
    maximum_area = 0
    contours, hierarchy = cv2.findContours(imgGC, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)   
    x_max, y_max = 0, 0
    for cnt_max in contours:
        area_max = cv2.contourArea(cnt_max)
        if area_max > maximum_area:
            maximum_area = area_max
    
    print("maximum area:", maximum_area)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)   
        approx = cv2.approxPolyDP(cnt, 0.01*peri, True)
        if area >= 0.65*maximum_area:
            full = full + 1
            success_check = True
               # 0.2 is the resolution
            x_max, y_max, w_max, h_max = cv2.boundingRect(approx)
            cv2.putText(imgContourGC, text1, (x_max+(w_max//2)-10, y_max+h_max+10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            colorr, 1)
            cv2.fillPoly(imgBlankGC, pts =[cnt], color=colorr)

        elif area > 0.2*maximum_area and area < 0.65*maximum_area:
            broken = broken + 1
            success_check = True
            x, y, w, h = cv2.boundingRect(approx)
            cv2.putText(imgContourGC, text2, (x+(w//2), y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        colorr, 1)
            cv2.fillPoly(imgBlankGC, pts =[cnt], color=colorr)

    return cv2.bitwise_and(imgBlankGC, imgContourGC), success_check, full, broken
#================================================================

if __name__ == '__main__':


    root_dir = 'Test_Images'
    destination_dir = 'Resulted_Images'
    #os.mkdir(destination_dir)
    i = 1
    for filename in os.listdir(root_dir):
        print(filename)
        Success_check = False
        if (filename.endswith(".PNG")):
        #===================To read the Image=============
            print("Inside Loop.")
            #img = cv2.imread(root_dir+"/"+filename)
            img = cv2.imread("Test_Images/Image1.png")
            # text_in_image = loaded_img[:25, :, :]
            # img = loaded_img[25:, :, :]
            #=================================================

            # for black chalky rice grains
            imgGray, imgBlank, imgContour, final_mask, imgCorner = Blur_Gray_HSV(img, 0, 179, 0, 255, 105, 255)
            cv2.imshow("Gray Image", imgGray)
            cv2.waitKey(0)
            cv2.imshow("Corner Image", imgCorner)
            cv2.waitKey(0)
            cv2.imshow("Mask", final_mask)
            cv2.waitKey(0)
            # imgCorner2, final_mask2 = dilated_eroded_added(img, imgCorner, final_mask)
            final_segmented_image1, Success_check1, full1, broken1 = get_contours(imgCorner, imgContour, imgBlank, Success_check, (0, 75, 150), "Chalky", "Broken")
            cv2.imshow("Segmented1", final_segmented_image1)
            cv2.waitKey(0)
            # for discolored yellow rice grains
            imgGray, imgBlank, imgContour, final_mask, imgCorner = Blur_Gray_HSV(img, 11, 52, 21, 115, 104, 255)
            cv2.imshow("Gray Image", imgGray)
            cv2.waitKey(0)
            cv2.imshow("Corner Image", imgCorner)
            cv2.waitKey(0)
            cv2.imshow("Mask", final_mask)
            cv2.waitKey(0)
            final_segmented_image2, Success_check2, full2, broken2 = get_contours(imgCorner, final_segmented_image1, imgBlank, 
                                                                        Success_check, (0, 128, 139), "Discolored", "Broken")
            cv2.imshow("Segmented2", final_segmented_image2)
            cv2.waitKey(0)
            # for healthy rice grains
            imgGray, imgBlank, imgContour, final_mask, imgCorner = Blur_Gray_HSV(img, 29, 179, 0, 30, 71, 165)
            cv2.imshow("Gray Image", imgGray)
            cv2.waitKey(0)
            cv2.imshow("Corner Image", imgCorner)
            cv2.waitKey(0)
            cv2.imshow("Mask", final_mask)
            cv2.waitKey(0)
            final_segmented_image3, Success_check3, full3, broken3 = get_contours(imgCorner, final_segmented_image2, imgBlank, 
                                                                        Success_check, (250, 10, 5), "Healthy", "Broken")
            # cv2.imshow("Segmented3", final_segmented_image3)
            # cv2.waitKey(0)
            #final_segmented_image_with_text = np.vstack([text_in_image, final_segmented_image])
            Chalky_count = full1
            Discolored_count = full2
            Healthy_count = full3
            Broken_count = broken1 + broken2 + broken3
            print(Chalky_count, Discolored_count, Healthy_count, Broken_count)
            cv2.putText(final_segmented_image3, "Healthy: "+str(Healthy_count), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (250, 10, 5), 1)
            cv2.putText(final_segmented_image3, "Chalky: "+str(Chalky_count), (10, 45), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 75, 150), 1)
            cv2.putText(final_segmented_image3, "Discolored: "+str(Discolored_count), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 128, 139), 1)
            cv2.putText(final_segmented_image3, 'Broken: '+str(Discolored_count) , (10, 95), cv2.FONT_HERSHEY_COMPLEX, 0.8,
                        (0, 0, 255), 1)
            annotated_image_name = filename
            if Success_check or Success_check2 or Success_check3:
                cv2.imwrite(destination_dir+'/'+annotated_image_name, final_segmented_image3)
            i+=1
            # cv2.imshow(final_segmented_image_with_text)
            # cv2.waitKey(0)
        #=====================================================