# The following assumptions are made for the question:
# 1. The Image Bounding Box starts from (0,0) at the top left..
# 2. Y-Threshold is a parameter based on which row selection happens, this can make
#    significant changes to results.. based on observation and testing the threshold is set to 10.
# 3. The logic is implemented as given..
#   - csv is loaded as dataframes..
#   - sorting is to be done for each rows..
#   - an OCR class with minx, maxx, miny, maxy is created for simplicity in implementation
#   - a row threshold limit of 10 by default is given, this can be changed to finetune based on innputs..
#   - more clear definition of threshold limit is given later..
#   - The main sorting algorithm is given in function sortOCRList(list<OCR>, threshold_limit)
#   - Left-right and top-bottom sorting is done by:
#   - sampling and checking the closest neighbours in the ocrlist for
#   - if neighbour1's max y is greater than neighbour2's min y this means they are above and below
import pandas as pd

THRESHOLD_LIMIT = 10


class OCR:
    def __init__(self, entity, coordinates, maxx, minx, maxy, miny):
        self.entity = entity
        self.coordinates = coordinates
        self.maxy = maxy
        self.miny = miny
        self.maxx = maxx
        self.minx = minx

    def toStringOCR(self):
        rt = "[" + str(self.coordinates) + ", " + self.entity + "]"
        return rt


# for now have a sample string::
# samplestr = "[[[[683.0, 658.0], [1191.0, 523.0], [1210.0, 594.0], [702.0, 730.0]], ('ty X6 54i z3B', 0.70269555)], [[[984.0, 661.0], [1136.0, 638.0], [1142.0, 676.0], [989.0, 700.0]], ('SNERL', 0.5955701)], [[[835.0, 691.0], [1056.0, 631.0], [1063.0, 656.0], [842.0, 717.0]], ('323399-003', 0.9963886)], [[[700.0, 734.0], [808.0, 703.0], [814.0, 722.0], [705.0, 753.0]], ('15/13', 0.9040577)], [[[815.0, 726.0], [882.0, 714.0], [886.0, 735.0], [819.0, 747.0]], ('PF', 0.51700246)]]"
# samplestr2 = "[[[[917.0, 374.0], [980.0, 374.0], [980.0, 406.0], [917.0, 406.0]], ('SZ', 0.9893714)], [[[578.0, 442.0], [759.0, 451.0], [752.0, 578.0], [572.0, 569.0]], ('23', 0.5911504)], [[[214.0, 474.0], [290.0, 474.0], [290.0, 513.0], [214.0, 513.0]], ('J S', 0.85718375)], [[[442.0, 483.0], [529.0, 483.0], [529.0, 518.0], [442.0, 518.0]], ('U K', 0.947205)], [[[835.0, 486.0], [935.0, 484.0], [936.0, 517.0], [836.0, 520.0]], ('cm', 0.9032759)], [[[218.0, 518.0], [296.0, 509.0], [302.0, 563.0], [224.0, 572.0]], ('13', 0.9987333)], [[[441.0, 524.0], [528.0, 512.0], [534.0, 556.0], [447.0, 568.0]], ('72', 0.924562)], [[[827.0, 517.0], [911.0, 517.0], [911.0, 573.0], [827.0, 573.0]], ('31', 0.78640205)], [[[129.0, 585.0], [316.0, 580.0], [317.0, 616.0], [130.0, 620.0]], ('211/13', 0.959378)], [[[752.0, 591.0], [935.0, 582.0], [937.0, 615.0], [754.0, 624.0]], ('012014', 0.90237254)], [[[244.0, 660.0], [363.0, 660.0], [363.0, 690.0], [244.0, 690.0]], ('FAS', 0.8477187)]]"
# samplestr3 = "[[[[121.0, 252.0], [889.0, 184.0], [899.0, 299.0], [131.0, 366.0]], ('MADE IN VIETNAM', 0.9879587)], [[[135.0, 472.0], [291.0, 483.0], [286.0, 545.0], [131.0, 533.0]], ('9', 0.99808526)], [[[262.0, 477.0], [884.0, 402.0], [896.0, 498.0], [274.0, 574.0]], ('741260255', 0.99289894)], [[[124.0, 534.0], [285.0, 534.0], [285.0, 598.0], [124.0, 598.0]], ('SPG', 0.9985122)], [[[642.0, 528.0], [863.0, 490.0], [873.0, 548.0], [652.0, 587.0]], ('0118', 0.83320355)], [[[305.0, 539.0], [665.0, 525.0], [667.0, 593.0], [307.0, 607.0]], ('753001', 0.9976473)], [[[406.0, 689.0], [728.0, 662.0], [733.0, 721.0], [410.0, 747.0]], ('ARTCG5907', 0.9976264)], [[[403.0, 755.0], [795.0, 715.0], [801.0, 770.0], [409.0, 809.0]], ('7L119468897', 0.89648336)], [[[111.0, 779.0], [342.0, 804.0], [339.0, 837.0], [107.0, 812.0]], ('adlidas', 0.91498554)], [[[389.0, 803.0], [807.0, 764.0], [812.0, 825.0], [395.0, 864.0]], ('F5PW29Xw08122', 0.9369447)]]"
#

def getOCRFromString(samplestr):
    ocrList = []
    entity = samplestr.split(")],")
    ind = 1
    for ent in entity:
        entSplit = ent.split(", (")
        coordinates = entSplit[0]
        namedEnt = entSplit[1]
        coordinates = coordinates.replace("[", "")
        coordinates = coordinates.replace("]", "")
        if ind == len(entity):
            namedEnt = namedEnt.split(")]]")[0]
        namedEnt = "(" + namedEnt + ")"
        # convert coordinates to arrays..
        i = 0
        outerarr = []
        arr = []
        xLst = []
        yLst = []
        for cord in coordinates.split(","):
            # additionally, find minx, maxx, minny and maxy
            num = cord.strip()
            num = float(num)

            if i % 2 == 0:
                # x coordinates..
                xLst.append(num)
                arr = []
            arr.append(num)
            if i % 2 != 0:
                # y coordinates
                yLst.append(num)
                outerarr.append(arr.copy())
            i += 1
        ocr = OCR(namedEnt, outerarr, max(xLst), min(xLst), max(yLst), min(yLst))
        ocrList.append(ocr)
        ind += 1
    return ocrList


def sortOCRList(ocrList, rowThreshold):
    # sort them based on y-coordinates first, this will sort almost 50% results..
    ocrList.sort(key=lambda dat: dat.miny)
    # now sort them based on row segregation and x-coordinates.. row segregation is the third condition in if
    # statement by which it is decided if a particular entity will be allowed to be inside the givenn horizontal
    # field based on the threshold and then sorted based on x coordinates..
    # this is to be compared with all entities as possible.. and hence combination is given n
    # this can be simplified..
    # every loop will sort it from the end..
    for i in range(len(ocrList)):
        for j in range(len(ocrList) - 1):
            if ocrList[j].maxy > ocrList[j + 1].miny and ocrList[j].minx > ocrList[j + 1].minx and (
                    ocrList[j].maxy - ocrList[j + 1].miny) >= rowThreshold:
                ocrList[j], ocrList[j + 1] = ocrList[j + 1], ocrList[j]
    return ocrList


def prettyPrintOCRList(updatedOcrList):
    retStr = "["
    si = len(updatedOcrList)
    i = 1
    for ocr in updatedOcrList:
        if si == i:
            retStr = retStr + ocr.toStringOCR() + "]"
        else:
            retStr = retStr + ocr.toStringOCR() + ", "
        i += 1
    return retStr


df = pd.read_csv("rec_text.csv")


def sortedOCR(data):
    ocrList = getOCRFromString(data)
    updatedOcrList = sortOCRList(ocrList, THRESHOLD_LIMIT)
    retString = prettyPrintOCRList(updatedOcrList)
    return retString


df2 = df.applymap(lambda data: sortedOCR(data))

df2.to_csv("final_rec_text.csv", index=False)
