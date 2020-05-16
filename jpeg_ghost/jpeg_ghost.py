import cv2
import numpy as np
import math
import sys
import matplotlib.pyplot as plt

block_size = 16
rangeOfQuality = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

path = sys.argv[1]
img1 = cv2.imread(path)
ydim, xdim, zdim = img1.shape

nQ = len(rangeOfQuality)
map = np.zeros([ydim, xdim, len(rangeOfQuality)])
c = 0
for quality in rangeOfQuality:
    cv2.imwrite('tmp1.jpg', img1, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    img2 = cv2.imread('tmp1.jpg')
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    for z in range(0, zdim):
        map[:, :, c] = map[:, :, c] + np.power(img1[:, :, z].astype(float) - img2[:, :, z].astype(float), 2)
    map[:, :, c] = map[:, :, c] / zdim
    c = c + 1

blocks = np.zeros([
    np.floor(ydim / block_size).astype(int),
    np.floor(xdim / block_size).astype(int),
    nQ])
for c in range(0, nQ):
    cy = 0
    for y in range(0, ydim - block_size, block_size):
        cx = 0
        for x in range(0, xdim - block_size, block_size):
            block_values = map[y: y + block_size, x: x + block_size, c]
            blocks[cy, cx, c] = np.mean(block_values)
            cx = cx + 1
        cy = cy + 1

minval = np.amin(blocks, 2)
maxval = np.amax(blocks, 2)

for c in range(0, nQ):
    blocks[:, :, c] = blocks[:, :, c] - minval
    blocks[:, :, c] = blocks[:, :, c] / (maxval - minval)

sp = math.ceil(math.sqrt(nQ))

fig, axs = plt.subplots(sp, sp)
axs = axs.reshape(sp * sp)
for c, ax in zip(range(0, nQ), axs):
    ax.set_title(rangeOfQuality[c])
    ax.imshow(blocks[:, :, c], extent=[0, 1, 0, 1])


plt.show()
cv2.waitKey(0)
