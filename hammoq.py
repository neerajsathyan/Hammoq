# You should start by separating out the different lines. When you have done that, you can simply process the
# contours left to right (sorted from x = 0 to x = width ) Start by drawing the found contours on a black background.
# Next, sum the rows. The sum of rows without words/contours will be 0. There is usually some space between lines of
# text, which will have sum = 0. You can use this to find the min and max height values for each line of text. To
# find the order of the words, first look for the contours in the y range of the first line, then for the lowest x.
# https://stackoverflow.com/questions/58903071/i-want-to-sort-the-words-extracted-from-image-in-order-of-their-occurence-using

import pandas as pd
import numpy as np

# load the csv file
#df = pd.read_csv("rec_text.csv")
#print(df.head(5))

# for now have a sample string::
str = "[[[[683.0, 658.0], [1191.0, 523.0], [1210.0, 594.0], [702.0, 730.0]], ('ty X6 54i z3B', 0.70269555)], [[[984.0, 661.0], [1136.0, 638.0], [1142.0, 676.0], [989.0, 700.0]], ('SNERL', 0.5955701)], [[[835.0, 691.0], [1056.0, 631.0], [1063.0, 656.0], [842.0, 717.0]], ('323399-003', 0.9963886)], [[[700.0, 734.0], [808.0, 703.0], [814.0, 722.0], [705.0, 753.0]], ('15/13', 0.9040577)], [[[815.0, 726.0], [882.0, 714.0], [886.0, 735.0], [819.0, 747.0]], ('PF', 0.51700246)]]"

# load image and get dimensions
# img = cv2.imread('xmple2.png',0)
# h,w = img.shape[:2]
# # sum all rows
# sumOfRows = np.sum(img, axis=1)
#
# # loop the summed values
# startindex = 0
# lines = []
# compVal = True
# for i, val in enumerate(sumOfRows):
#     # logical test to detect change between 0 and > 0
#     testVal = (val > 0)
#     if testVal == compVal:
#             # when the value changed to a 0, the previous rows
#             # contained contours, so add start/end index to list
#             if val == 0:
#                 lines.append((startindex,i))
#             # update startindex, invert logical test
#                 startindex = i+1
#             compVal = not compVal



# # create empty list
# lineContours = []
# # find contours (you already have this)
# x, contours, hier = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# # loop contours, find the boundingrect,
# # compare to line-values
# # store line number,  x value and contour index in list
# for j,cnt in enumerate(contours):
#     (x,y,w,h) = cv2.boundingRect(cnt)
#     for i,line in enumerate(lines):
#         if y >= line[0] and y <= line[1]:
#             lineContours.append([line[0],x,j])
#             break
#
# # sort list on line number,  x value and contour index
# contours_sorted = sorted(lineContours)
#
# # write list index on image
# for i, cnt in enumerate(contours_sorted):
#     line, xpos, cnt_index = cnt
#     cv2.putText(img,str(i),(xpos,line+50),cv2.FONT_HERSHEY_SIMPLEX,1,(127),2,cv2.LINE_AA)
#
# # show image
# cv2.imshow('Img',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()