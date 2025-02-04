# What is this App?

This is an object detection app written in Python. It detects objects that passes through the webcam.

This app is written with the idea of a webcam alert app, where the webcam is setup in a security location to record everyone who passes through the area.

3 Images will be generated when an object enter and exit the webcam:

1. Middle frame: For example, the object is viewed in frame for 5 sceonds, the 2.5 second's frame is captured.
2. Largest Detection: The image that had the largest detection box area while in frame is captured.
3. Nearest to Center: The image that had the detection box cloest to the center while in frame is captured.

The app will then send an email with these images attached everytime an object is detected. (Email address provided by the user)

# Library used

* Python
* Opencv
* smtplib
* email.message
* threading
* streamlit

### This app is homework App 9 - Build a Webcam Alert App from Udemy course [Python Mega Course: Learn Python in 60 Days, Build 20 Apps](https://www.udemy.com/course/the-python-mega-course/learn/lecture/34604706#overview)
# Live demo

Live demo: [https://youtu.be/UfdVSR1yFKU](https://youtu.be/UfdVSR1yFKU)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/UfdVSR1yFKU/0.jpg)](https://www.youtube.com/watch?v=UfdVSR1yFKU)

