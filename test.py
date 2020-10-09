import xml.etree.ElementTree as ET
import sys

if __name__ == '__main__':

    tree = ET.parse('./xmlTest.xml')
    root = tree.getroot()
    layouts = root.findall("./layouts/layout")

    layoutList = [[], [], [], []]

    for lay in layouts:
        layoutDict = {}
        n = int(lay.find("./nbImages").text)
        path = str(lay.find("./template").text)
        isLandscape = bool(lay.find("./landscape").text)

        layoutDict["landscape"] = isLandscape
        layoutDict["nbImages"] = n
        layoutDict["template"] = path

        images = lay.findall("./images/image")
        print(len(images))
        if len(images) != int(lay.find("./nbImages").text):
            print("XML error too much images for this layout")
            sys.exit(1)

        imagesDict = {}
        for im in images:
            imageDict = {}
            imageDict["x"] = int(im.find("./x").text)
            imageDict["y"] = int(im.find("./y").text)
            imageDict["w"] = int(im.find("./w").text)
            imageDict["h"] = int(im.find("./h").text)
            imageDict["angle"] = int(im.find("./angle").text)
            imagesDict[int(im.find("./index").text)] = imageDict

        layoutDict["images"] = imagesDict
        layoutList[n - 1].append(layoutDict)
    print(layoutList)

    sys.exit(1)
