# Face Stabilizer

Python based open-cv multi-target face tracker and stabilizer. Identifies faces and categorizes them into entities, able to output multiple video files tracking the subject, keeping the face (or other selected target) at the center of the frame for the entirity of the lifespan of each entity within the input video.


# Prerequisites

This project was create using python `2.7.9`, with additional package installations such as `opencv-python`, `Pillow` and `numpy`. For easy installation, [PIP](https://packaging.python.org/en/latest/tutorials/installing-packages/) can be used. Additionally, a desired HAAR cascade must be downloaded from [OPENCV](https://github.com/opencv/opencv/tree/master/data/haarcascades) and placed in the root folder of this project. I most commonly use `haarcascade_frontalface_default.xml`, as that was not overly harsh on classification. You may place the video you desire (as an .mp4) to parse alongside this for easier access.

# Execution

This project can be executed by calling  
`py parse.py ./[input video here].mp4`

# Program Overview

This program utilizes python's open cv to split the given mp4 video into frames, and then identify the faces (or other target) in each frame. Then, each next frame identifies nearby targets and classifies targets that have not moved outside of a set threshold as the same entity. Each entity is tracked throughout the entirity of it's lifetime in the input video file, and then each entity is resized and repositioned such that the target is always at the center of the frame, stabilizing the subject at the center of the output video. 

# Results


## Single person stabilization:

|  Input 1: |  Output 1:  |
|-----------|-------------|
|<img src="./res/orig_1.gif" width="300" height="234"/>|<img src="./res/after_1.gif" width="234" height="234"/>|
<sub>[Source](https://www.youtube.com/watch?v=dQw4w9WgXcQ)</sub>
