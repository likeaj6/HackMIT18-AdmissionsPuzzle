""" Extract the QR code from the bottom left corner of each frame
"""
import imageio
import cv2
import numpy as np
import matplotlib.pyplot as plt

# read in the video - there are 149 frames
reader = imageio.get_reader('vid.mp4')

# extract the first frame - format is numpy array
# picture is 1280 pixels wide and 720 pixels tall
first_frame = reader.get_data(0)

# take only the rows 596:695
# take only the columns 25:124
# take all 3 rgb values :
qr_code_1 = first_frame[596:695,25:124,:]
print(qr_code_1.shape)
qr_code_gray = cv2.cvtColor(qr_code_1, cv2.COLOR_BGR2GRAY)
# ret,thresh1 = cv2.threshold(qr_code_gray,0,255,cv2.THRESH_BINARY)


# qr_codes = []
#
# # iterates over each frame, i for index, im for image
# for i, im in enumerate(reader):
#     # get the frame
#     frame = reader.get_data(i)
#     # append just the qr code to be processed
#     qr_codes.append(frame[596:695,25:124,:])
#
# print(len(qr_codes))

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.imshow(qr_code_gray)
plt.show()
