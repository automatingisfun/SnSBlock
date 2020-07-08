import cv2
import math
from tkinter import *
import pyautogui
import time
import numpy as np
import matplotlib.pyplot as plt
import win32api, win32con
import keyboard

CHARACTER_POSITION = None
CAPTURE_AREA = [None, None]

QUIT = False # We loop in-game until this is set to True.

def terminate_program():
    global QUIT
    
    QUIT = True
    
    exit(0)

keyboard.add_hotkey('ctrl+c', terminate_program)

# TKinter callback.
def callback(event):
    global CHARACTER_POSITION
    global CAPTURE_AREA

    if CHARACTER_POSITION is None:
        CHARACTER_POSITION = [event.x, event.y]
        print("Click on the top left corner of the designated area.")
    elif CAPTURE_AREA[0] is None:
        CAPTURE_AREA[0] = (event.x, event.y)
        print("Click on the bottom right corner of the designated area.")
    elif CAPTURE_AREA[1] is None:
        CAPTURE_AREA[1] = (event.x, event.y)

        print("Configuration DONE.")

        # Shift the stored character position to match the coordinate system of the captured area.
        CHARACTER_POSITION = (CHARACTER_POSITION[0] - CAPTURE_AREA[0][0], CHARACTER_POSITION[1] - CAPTURE_AREA[0][1])

        # Close the overlayed window.
        root.quit()
        root.destroy()

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()

root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

root.bind("<Button-1>", callback)

# Make the window transparent to a degree.
root.attributes('-alpha', 0.3)

print("Click on character")

root.mainloop()

time.sleep(2)

while not QUIT:
    img = np.array(pyautogui.screenshot())[CAPTURE_AREA[0][1]:CAPTURE_AREA[1][1], CAPTURE_AREA[0][0]:CAPTURE_AREA[1][0], :]

    # Detect pixels representing an apple.
    RED_VERTICES = []

    red_vertex_indices = np.where((img[:, :, 0] > 150) & (img[:, :, 1] < 50) & (img[:, :, 2] < 50)) 

    y_coords, x_coords = red_vertex_indices

    # Calculate the distance of each red pixel relative to the character's position.
    for x_coord, y_coord in zip(x_coords, y_coords):
        RED_VERTICES.append({"location": (x_coord, y_coord), "distance": math.sqrt((CHARACTER_POSITION[0] - x_coord) ** 2 + (CHARACTER_POSITION[1] - y_coord) ** 2), "distance_x": CHARACTER_POSITION[0] - x_coord})

    if len(RED_VERTICES) > 0:
        closest_red_vertex = min(RED_VERTICES, key=lambda x: x["distance"])

        # Shift the positions by the coordinates of the capture area's top left corner.
        x, y = CAPTURE_AREA[0][0] + closest_red_vertex["location"][0], CAPTURE_AREA[0][1] + closest_red_vertex["location"][1]

        # Click at the given position to ensure that the mouse move event is executed.
        win32api.SetCursorPos((x, y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    else:
        print("empty...")
