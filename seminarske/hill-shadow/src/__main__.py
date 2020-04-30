import numpy as np
from math import atan, sqrt, atan2, pi, cos, sin
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

zenith = int(input("Vnesi zenith: "))
azimuth = int(input("Vnesi azimuth: "))

def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

img = mpimg.imread('../data/mb-center_vhod.tif')
gray = rgb2gray(img)

shading = []

for y in range(1, len(gray) - 1):
    shading.append([])
    for x in range(1, len(gray[0]) - 1):
        A = gray[y - 1][x - 1]
        D = gray[y - 1][x]
        G = gray[y - 1][x + 1]

        B = gray[y][x - 1]
        E = gray[y][x]
        H = gray[y][x + 1]

        C = gray[y + 1][x - 1]
        F = gray[y + 1][x]
        I = gray[y + 1][x + 1]

        dzdx = ((C + 2 * F + I) - (A + 2 * D + G)) / 8
        dzdy = ((G + 2 * H + I) - (A + 2 * B + C)) / 8

        slope = max([atan(sqrt(dzdx ** 2 + dzdy ** 2)), 0])
        aspect = 0

        if slope > 0:
            aspect = (atan2(dzdy, -dzdx) + 2*pi) % 2*pi
        else:
            if dzdy > 0:
                aspect = pi/2
            elif dzdy < 0:
                aspect = 3*pi/2

        shadow = (cos(-zenith) * cos(slope)) + (cos(azimuth - aspect) * sin(-zenith) * sin(slope))
        shadow *= 255

        shading[-1].append(shadow)

plt.imshow(shading, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
plt.show()
