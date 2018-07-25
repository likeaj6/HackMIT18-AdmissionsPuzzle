import numpy as np
import cv2
from os import listdir
from os.path import isfile, join
import imageio

mask = cv2.imread('mask.jpg', 0)


reader = imageio.get_reader('vid.mp4')

def get_frames():
   for i, im in enumerate(reader):
       imageio.imwrite(join('frames', ('%03d' % i)+'.png'), im)

def inpaint():
   files = [f for f in listdir('frames') if isfile(join('frames', f))]
   mask = cv2.imread('mask.png', 0)

   for f in files:
       img = cv2.imread(join('frames', f))
       dst = cv2.inpaint(img,mask,3,cv2.INPAINT_TELEA)
       cv2.imwrite(join('cleaned_frames', f), dst)

def stitch():
   fps = reader.get_meta_data()['fps']
   writer = imageio.get_writer('output.mp4', 'ffmpeg', fps=fps, quality=8)
   files = [f for f in listdir('cleaned_frames') if isfile(join('cleaned_frames', f))]
   files.sort()
   for f in files:
       img = imageio.imread(join('cleaned_frames', f))
       writer.append_data(img)
   writer.close()

if __name__ == '__main__':
   print('Splitting video in frames...')
   # get_frames()
   print('Removing watermark from frames...')
   inpaint()
   print('Putting it all back together...')
stitch()
