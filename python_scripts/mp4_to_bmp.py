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
    new_image = np.ones((height, adjusted_width, 3), dtype=np.uint8) * 255
    new_image[:, (adjusted_width-width)//2:(adjusted_width-width)//2+width] = frame
    # add them in on the sides too
    # new_image[:, 0:width] = frame
    # new_image[:, -width:] = frame
    # resize


    # add text on left side:
    # AugmentOS Hackathon
    # @ Mentra HQ
    # March 1st 2025

    # add text to right side
    # Frame: index

    new_image = cv2.resize(new_image, (576, 136))
    new_image = cv2.putText(new_image, f"Frame: {index}", (450, 136//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0,), 1, cv2.LINE_AA)
    new_image = cv2.putText(new_image, "AugmentOS Hackathon", (10, 136//2-20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    new_image = cv2.putText(new_image, "@ Mentra HQ", (10, 136//2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    new_image = cv2.putText(new_image, "March 1st 2025", (10, 136//2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.imshow('frame', new_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
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