# Document Scanner (Computer Vision)
A lightweight document scanner built with OpenCV and NumPy, traditional image processing (no deep learning).
The program detects paper boundary, correct perspective distortion, and binarize image to get scanned document.

## Core CV algorithms
1. Gaussian blur + Canny edge detection
2. Contour detection & polygon approximation
3. 4-point perspective transformation (homography matrix)
4. Image binarization

## Environment
Python >= 3.9

## Install dependencies
```bash
pip3 install -r requirements.txt
