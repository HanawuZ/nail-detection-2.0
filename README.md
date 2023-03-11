# nail-detection-2.0

# NailDetection
## _Detection & Analysis._

Developed using _OpenCV_([OpenCV](https://opencv.org/)) and _Matplotlib_([Matplotlib](https://matplotlib.org/)) with Python programming language([Python](https://www.python.org/)). 
**Project @ SUT.**

- Have camera detection and graph analysis.
- Use ttkbootstrap([ttkbootstrap](bootstrap.readthedocs.io/)) for build GUI.

## Features

##### _:: 3 Zone ::_
1. Camera
    - Use OpenCV for Capture video.
    - Have controller ex. Time interval, Zoom, Box size, controller box axis.
2. Graph
    - Analysis.
    - Have controller ex. Time interval, Data limit, ToolBar
3. Main Controller
    - TODO

## Installation

requires [Python](https://www.python.org/) v3.9.12+ to run.

Install the dependencies and devDependencies and run the `gui.py`

#### git clone
```sh
git clone https://github.com/miracleexotic/nail-detection.git
cd nail-detection
```

### install dependencies
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

### run
```sh
python3 gui.py
```

## ref
https://pyshine.com/Video-processing-in-Python-with-OpenCV-and-PyQt5-GUI/
https://blog.devgenius.io/learn-ci-cd-with-github-actions-to-deploy-a-nestjs-app-to-heroku-8feb715d3ce7
