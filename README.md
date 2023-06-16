# Rice-Disease-Detection-OpenCV
## Clone this Repo
```
git clone https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV
cd Rice-Disease-Detection-OpenCV
```

## Problem Statement
There is only a single image of rice grains.

![Image1](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/f7f0eaa8-49d0-49ce-8db5-b2fd45bff552)

There are four types of rice grains. Only one of these is healthy.

  1) Healthy
  
  ![image](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/5d4b1ea0-3e93-4548-bcbf-1a934ede924b)

  2) Discolored

  ![Screenshot 2023-04-08 214025](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/dbd6e53d-da8f-484a-ac68-52949ff1e36c)

  3) Chalky

  ![Screenshot 2023-04-08 213832](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/baa8e494-20fc-424b-a432-faaa676575df)

  4) Broken
  
  ![Screenshot 2023-04-08 213643](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/7d1a684b-e54e-46cb-9977-4334a0772309)

Rice grain from each type should be segmented with a speific color. Count of each type should also be displayed.

## Solution
Since there is only one image so ML/DL can't be used. It can be solved with image processing techniques mainly Hue-Saturation-Value (HSV).

![download](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/3c571dff-65fc-4eff-af9f-7697cfa45862)

The file

    Hue_Sat_Val_Settings.py
    
allows to use trackbars to adjust HSV values for an image. HSV values for four rice grain types are

  1) Chalky

![Capture3](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/61cd2736-0449-4fae-955b-22fdbb4539ca)

  2) Discolored

![Capture4](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/f1eefc9f-252c-4dd1-acf0-938c25fead12)

  3) Healthy and Broken (Since both have same color, just different in size)
  
  ![Capture5](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/dd5902d9-621d-48b1-aaff-0683fb26f170)

To differentiate between Healthy and broken, area of both is calculated. A threshold is set, if the area is greater than this threshold, 
grain would be healthy otherwise broken.

## Results
Run the following

    Rice_Segmentation.py
    
It uses some image processing techniques including HSV, erosion, dilation, area calculation under contours. The result is

![Image1](https://github.com/HassanBinAli/Rice-Disease-Detection-OpenCV/assets/87352841/d1cfa749-ee5c-4297-80a1-e203513b082e)

## Advantages
  1) Needs no training.
  2) Can be used to solve other similar problems.

## Disadvantages
  1) Not a generalized method.
  2) Using area to differentiate between healthy and broken grains is not a robust method.
  3) If two grains are so close that they touch each other, calculated area would be larger resulting in wrong segmentation.

## Acknowledgements

 - [Murtaza's Workshop - OpenCV Course](https://www.youtube.com/watch?v=WQeoO7MI0Bs)
