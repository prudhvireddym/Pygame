# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:46:14 2020

@author: prudh
"""

import cv2

index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        if index ==100:
            break
    else:
        arr.append(index)
    cap.release()
    index += 1
    print(arr)