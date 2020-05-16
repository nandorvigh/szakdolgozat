import cv2
import matplotlib.pyplot as plt
import sys
import numpy as np
from scipy.spatial import distance
from itertools import groupby


def match(descriptors, source_img):
    res_img = source_img
    convex_hull1 = []
    convex_hull2 = []
    arr = []
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.knnMatch(descriptors, descriptors, 2)

    for m, n in matches:
        key_point1 = key_points[m.trainIdx]
        key_point2 = key_points[m.queryIdx]
        if key_point1 == key_point2:
            continue

        key_point1, key_point2 = orderPoints(key_point1, key_point2)
        euclidean_distance = distance.euclidean(key_point1.pt, key_point2.pt)
        arr.append([key_point1, key_point2, euclidean_distance])

        convex_hull1.append(key_point1.pt)
        convex_hull2.append(key_point2.pt)
        cv2.line(res_img,
                 (int(key_point1.pt[0]), int(key_point1.pt[1])),
                 (int(key_point2.pt[0]), int(key_point2.pt[1])),
                 (255, 0, 0),
                 2)
    return res_img, convex_hull1, convex_hull2, arr


def orderPoints(key_point1, key_point2):
    points1 = key_point1.pt
    points2 = key_point2.pt

    if points1[0] > points2[0]:
        return key_point2, key_point1
    return key_point1, key_point2


def split(u, v, points):
    return [p for p in points if np.cross(p - u, v - u) < 0]


def extend(u, v, points):
    if not points:
        return []

    w = min(points, key=lambda p: np.cross(p - u, v - u))
    p1, p2 = split(w, v, points), split(u, w, points)
    return extend(w, v, p1) + [w] + extend(u, w, p2)


def convex_hull(points):
    u = min(points, key=lambda p: p[0])
    v = max(points, key=lambda p: p[0])
    left, right = split(u, v, points), split(v, u, points)

    return [v] + extend(u, v, left) + [u] + extend(v, u, right) + [v]


path = sys.argv[1]
img = cv2.imread(path)

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

nFeaturePoints = 2000
patchSize = 4
scoreType = cv2.ORB_FAST_SCORE
orb = cv2.ORB_create(nfeatures=nFeaturePoints, scoreType=scoreType, patchSize=patchSize)
key_points = orb.detect(gray_img)

key_points, descriptors = orb.compute(gray_img, key_points)

result, conv_hull1, conv_hull2, euclidean_distances = match(descriptors, img)

for key, group in groupby(euclidean_distances, lambda x: x[2]):
    convex_shape1 = []
    convex_shape2 = []
    for element in group:
        convex_shape1.append(element[0].pt)
        convex_shape2.append(element[1].pt)

    pts1 = np.array(convex_shape1, np.int32)
    hull1 = np.array(convex_hull(pts1))

    pts2 = np.array(convex_shape2, np.int32)
    hull2 = np.array(convex_hull(pts2))

    cv2.fillPoly(result, [hull1], (0,0,255))
    cv2.fillPoly(result, [hull2], (0,0,255))


plt.figure(1)

res = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
plt.imshow(res)
plt.show()
cv2.waitKey(0)
