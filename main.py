# This is a sample Python script.
import os
import cv2
import numpy as np
import gc
import sys
import curses
import time


cap = cv2.VideoCapture('Bad Apple_144p.mp4')
frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(frameHeight)
os.system(f'mode con cols={frameWidth + 1} lines={frameHeight + 1}')

buf = np.empty((frameCount, frameHeight, frameWidth, 3), np.dtype('uint8'))


fc = 0
ret = True
out = ''
fps = 30
ms = 1 / fps
status = 0

if not os.path.isdir("./out"):
    os.makedirs("./out")
while cap.isOpened() and status:
    ret, buf = cap.read()
    if not ret:
        break
    cv2.imshow('image', buf)
    k = cv2.waitKey(5)
    fc += 1
    os.system('cls')
    temp = open('./out/RES(' + str(fc) + ').txt', 'w')
    # buf = cv2.resize(buf, (0, 0), fx=frameWidth, fy=frameHeight)

    for i in range(int(frameHeight / 2)):
        for j in range(int(frameWidth)):
            if buf[i * 2][j][0] > 200:
                out += "#"
            else:
                out += "."
        out += "\n"
    temp.write(out)
    temp.close()
    out = ''
    if k & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

stdscr = curses.initscr()
stdscr.scrollok(True)
stdscr.timeout(1)
curses.curs_set(0)
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
t0 = time.time()
i = 1

while True:
    t1 = time.time()
    i = int((t1 - t0) * fps) + 1
    filename = './out/RES('+str(i)+').txt'
    try:
        with open(filename, 'r') as f:
            data = f.read()
            stdscr.addstr(0, 0, data)
            # stdscr.addstr("Frame: %d" % i)
            stdscr.clrtoeol()
            stdscr.clearok(1)
            stdscr.refresh()
    except IOError:
        break

curses.curs_set(1)
curses.echo()
curses.nocbreak()
stdscr.keypad(False)

curses.endwin()
gc.collect()
sys.exit()
# clear_screen()
# for i in range(10):
#     # clear_screen()
#     print('################')  # Press Ctrl+F8 to toggle the breakpoint.
