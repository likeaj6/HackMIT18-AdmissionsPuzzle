import pyautogui
import time

t_end = time.time() + 20
while time.time() < t_end:
    for i in range(640):
        for j in range(480):
            print(i, j)
            pyautogui.click(i, j)
    # do whatever you do
