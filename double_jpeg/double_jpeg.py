import sys

import cv2
import numpy as np
from matplotlib import pyplot as plt

path = sys.argv[1]
image = cv2.imread(path)

write_coordinates = False

if len(sys.argv) == 4:
    x = int(sys.argv[2])
    y = int(sys.argv[3])
    write_coordinates = True

if image.shape[0] % 8 != 0:
    rows = image.shape[0] + 8 - image.shape[0] % 8;
else:
    rows = image.shape[0];
if image.shape[1] % 8 != 0:
    cols = image.shape[1] + 8 - image.shape[1] % 8;
else:
    cols = image.shape[1];

im2 = np.zeros((rows, cols, 3), np.uint8)
im2[0:image.shape[0], 0:image.shape[1]] = image

n = im2.shape[0]*im2.shape[1]/64

luminance = cv2.cvtColor(im2, cv2.COLOR_BGR2YCR_CB)[:,:,0]

luminance = luminance.reshape(int(n), 8, -1, 8).swapaxes(1, 2).reshape(-1, 8, 8)

dct_values = np.zeros((int(n), 8,8), dtype=np.float32)
for i in range(0, int(n)):
    dct_values[i] = cv2.dct(np.float32(luminance[i]))

if write_coordinates:
    plt.hist(
        dct_values[:, x, y],
        bins=np.arange(dct_values[:, x, y].min(), dct_values[:, x, y].max()))
else:
    f,a1 = plt.subplots(8,8)
    a1 = a1.ravel()
    for idx,ax in enumerate(a1):
        data = dct_values[:,int(idx / 8), int(idx % 8)]
        ax.hist(data, bins=np.arange(data.min(), data.max()))

plt.show()
