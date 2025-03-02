# opencv bad apple convert to small bitmaps for AugmentOS Smart Glasses
import os

import cv2
import numpy as np
from pathlib import Path

bmp_folder = Path("bmps")
final_folder = Path("final")
final_folder.mkdir(exist_ok=True)
bmp_folder.mkdir(exist_ok=True)

cap = cv2.VideoCapture('badapple.mp4')
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))


ret, frame = cap.read()

# height is the limiting factor, scale according to the height
goal_aspect_ratio = 576/136

# add padding to the sides until it matches the aspect ratio
adjusted_width = int(height * goal_aspect_ratio)
index = 0
while ret:
    # invert frame first
    frame = cv2.bitwise_not(frame)
    new_image = np.ones((height, adjusted_width, 3), dtype=np.uint8) * 255
    new_image[:, (adjusted_width-width)//2:(adjusted_width-width)//2+width] = frame
    # add them in on the sides too
    # new_image[:, 0:width] = frame
    # new_image[:, -width:] = frame
    # resize
    new_image = cv2.resize(new_image, (576, 136))
    # invert, save as bitmap
    inverted = cv2.bitwise_not(new_image)
    bmp_path = 'bmps/' + f"{index}" + '.bmp'
    cv2.imwrite(bmp_path, inverted)


    # run imagemagick to convert to 1bpp
    convert_str = f"magick {bmp_path} -monochrome -type bilevel {final_folder / f'{index}.bmp'}"
    os.system(convert_str)
    
    print(index)
    ret, frame = cap.read()
    index += 1