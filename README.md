# nail-detection-2.0

## Nail Detection 2.0
## _Detection & Analysis._

Developed using _OpenCV_([OpenCV](https://opencv.org/)) and _Matplotlib_([Matplotlib](https://matplotlib.org/)) with Python programming language([Python](https://www.python.org/)). 
**Project @ SUT.**

- Have camera detection and graph analysis.
- ~~Use ttkbootstrap([ttkbootstrap](bootstrap.readthedocs.io/)) for build GUI.~~
- Use Tkinter () for build GUI

## Features

##### _:: 3 Zone ::_
1. Camera
    - Use OpenCV for Capture video.
    - Have controller ex. Time interval, Zoom, Box size, controller box axis.
2. Video process
    - Process a video when recorded video from camera using OpenCV
    - Find finger (IF NEEDED)
    - Change image to gray scale
    - Use cv2 gaussian blur (IF NEED?)
    - Calculating a color in a area of nail 
3. Graph
    - Analysis.
    - Have controller ex. Time interval, Data limit, ToolBar
4. Main Controller (Display desktop)
    - Output everything in display using touch screen display (Full Screen) 
    - realtime show graph and camera (Testing)
    - should read a graph and video in realtime
    - record a video and will process when a video is record done (True running)
    - To Do (Task in now)

## Installation (to installing use a install dependencies [1] Section)

requires [Python](https://www.python.org/) v3.7.3 to run.
requires [Opencv](https://opencv.org/) v4.5.3.56.
requires [Pillow](https://pillow.readthedocs.io/en/stable/index.html) v8.3.2 (I have a spilcal to install by use a install dependencies in a down)
requires [Matplotlib](https://matplotlib.org/) v3.4.3
requires [Numpy](https://numpy.org/) v1.21.5


#### git clone
```sh
git clone https://github.com/HanawuZ/nail-detection-2.0
cd nail-detection-2.0
```

### install dependencies [1]
>**Raspberry Pi** pre-install dependencies
> Installing dependencies for Pillow use in ttkbootstrap.
```sh
sudo apt-get update
sudo apt-get install libjpeg-dev -y
sudo apt-get install zlib1g-dev -y
sudo apt-get install libfreetype6-dev -y
sudo apt-get install liblcms1-dev -y
sudo apt-get install libopenjp2-7 -y
sudo apt-get install libtiff5 -y
```
**Python v3.9.12+**
> [How To Install the Latest Python Version on Raspberry Pi?](https://raspberrytips.com/install-latest-python-raspberry-pi/)
> and then install python dependencies
```sh
python3 -m pip install -r requirements.txt
```

<!-- ### run
```sh
python3 gui.py
``` -->

## ref in project
https://pyshine.com/Video-processing-in-Python-with-OpenCV-and-PyQt5-GUI/

https://towardsdatascience.com/faster-video-processing-in-python-using-parallel-computing-25da1ad4a01

https://stackoverflow.com/questions/70318766/tkinter-and-multiprocessing-cannot-pickle-tkinter-tkapp-object
## ref for everyone to use in your project and working
https://blog.devgenius.io/learn-ci-cd-with-github-actions-to-deploy-a-nestjs-app-to-heroku-8feb715d3ce7
