# Frisco-ISD-GPA-Calc---Real-Time
Frisco ISD calculates high school student GPAs at the end of each semester (December and June).

Many student would like the option to be able to see their GPA in real time without having to manually do calculation by hand

Unfortunately for some students the mobile apps on both Android and iOS do not show accurate real time GPAs.

This project is designed to perform the correct calculations on student data from the Home Access Center.

![](https://github.com/SumitNalavade/Frisco-ISD-GPA-Calc---Real-Time/blob/main/HAC.png)
![](https://github.com/SumitNalavade/Frisco-ISD-GPA-Calc---Real-Time/blob/cbdf16549215c9a311e133cc19e56c3d02747640/Login%20page.PNG)
![](https://github.com/SumitNalavade/Frisco-ISD-GPA-Calc---Real-Time/blob/cbdf16549215c9a311e133cc19e56c3d02747640/Calc.PNG)

*Two apps in repository:*

*.exe file (For windows)*

*.app file (Coming soon for Mac)*

The calculation works in two stages:
1. Retreive the existing student GPA as noted on their transcript from HAC
2. Retreieve all current student grades and use calculate the real time GPA
3. Merge existing GPA with real time GPA to find the average 

To retreieve student data from Home Access Center, the python Selenium web scraping library was used in a headless browser.

**Objectives: Demonstrate knowledge of object oriented programming, integrate external libraries for a specific goal,
touch base with the Tkinter library for python guis, Demonstrate problem solving skills that come with a larger project**

