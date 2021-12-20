import inline as inline
import matplotlib as matplotlib
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
matplotlib.rcParams['image.cmap'] = 'gray'

imageCopy = cv2.imread("./test.png")
imageGray = cv2.imread("./test.png", 0)
image = imageCopy.copy()

contours, hierarchy = cv2.findContours(imageGray, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
bboxes = [cv2.boundingRect(i) for i in contours]
bboxes = sorted(bboxes, key=lambda y: y[1])

df = pd.DataFrame(bboxes, columns=['x', 'y', 'w', 'h'], dtype=int)
df["y2"] = df["y"] + df["h"]  # adding column for y on the right side # ymax of the counter
df["x2"] = df["x"] + df["w"]
# df = df.sort_values(["y", "x", "y2", "x2"])  # sorting

for i in range(1000):  # change rows between each other by their coordinates several times
    # to sort them completely
    for ind in range(len(df) - 1):
        #     print(ind, df.iloc[ind][4] > df.iloc[ind+1][0])
        if df.iloc[ind][4] > df.iloc[ind + 1][1] and df.iloc[ind][0] > df.iloc[ind + 1][0] and (
                df.iloc[ind][4] - df.iloc[ind + 1][1]) >= 70:
            df.iloc[ind], df.iloc[ind + 1] = df.iloc[ind + 1].copy(), df.iloc[ind].copy()
num = 0
for box in df.values.tolist():
    x, y, w, h, hy, hx = box
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 255), 2)
    # Mark the contour number
    cv2.putText(image, "{}".format(num + 1), (x + 40, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2)
    num += 1
plt.imsave("sample.png", image[:, :, ::-1])
