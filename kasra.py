#######################################
#       Written by Pooyan Zarif       #
#######################################
import os
import numpy as np
from PIL import Image, ImageOps
import argparse

#  Transparent an image
def transparent(image):
    data = image.getdata()
    # Transparency
    newImage = []
    for item in image.getdata():
        if item[:3] == (255, 255, 255):
            newImage.append((255, 255, 255, 0))
        else:
            newImage.append(item)

    image.putdata(newImage)
    return image


# Detect background of an image
def detect_background(image):
    colors = image.getcolors()
    m = 0
    color = 0
    for n, c in colors:
        if n > m:
            m = n
            color = c
    return color


# finde signiture in the image
def find_object(image):
    width = image.width
    height = image.height
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    npimage = np.array(image.getdata()).reshape((height, width)).astype(np.float32)

    background = detect_background(image)

    if background == 255:
        npimage = np.subtract(255, npimage)

    # Normalizring
    mmin = np.min(npimage)
    mmax = np.max(npimage)

    npimage = (npimage - mmin) / (mmax - mmin)

    # round pixels in for group (0-63 , 64-127 , 128-191 , 192-255)
    npimage = np.int8(npimage / 0.25) * 255

    sum_col = np.sum(npimage, axis=0)
    sum_row = np.sum(npimage, axis=1)
    
    # Finde border of the signiture
    vertical_color_tolerate = 0
    horizental_color_tolerate = 0
    left = 0
    while sum_col[left] <= horizental_color_tolerate:
        left += 1

    right = width - 1
    while sum_col[right] <= horizental_color_tolerate:
        right -= 1

    top = 0
    while sum_row[top] <= vertical_color_tolerate:
        top += 1

    bottom = height - 1
    while sum_row[bottom] <= vertical_color_tolerate:
        bottom -= 1

    return (left, top, right, bottom)


# stretch image in new size
def stretch(image, new_width, new_height):

    w, h = image.size
    if w > h:
        scale = new_width / w
    else:
        scale = new_height / h

    image = ImageOps.scale(image, scale)
    image = image.convert("RGBA")
    image = transparent(image)
    resized_w, resized_h = image.size
    off_x = (new_width - resized_w) // 2
    off_y = (new_height - resized_h) // 2
    newImage = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))
    newImage.paste(image, (off_x, off_y, off_x + resized_w, off_y + resized_h))
    return newImage


# crop an image and save in a destenition directory
def CropAndSave(filename, destenition):
    name = os.path.basename(filename).split(".")[0]
    W = 500
    H = 500

    image = Image.open(filename)
    (left, top, right, bottom) = find_object(image)
    croped = image.crop(box=(left, top, right, bottom))
    image = stretch(croped, W, H)
    fn = os.path.join(destenition, name + ".png")
    image.save(fn, "PNG")
    return name + ".png"


# set the arguments for command line
parser = argparse.ArgumentParser(
    description='Prepare signitures in Pargar standards. Written by "Pooyan Zarif"'
)
parser.add_argument(
    "-s", "--source", help='Enter Source directory. Default is "source"', default="source"
)
parser.add_argument(
    "-d",
    "--destination",
    help='Enter destination directory. Default is "destination"',
    default="destination",
)
parser.add_argument("-v", "--verbose", help='verbose', action="store_true")
args = vars(parser.parse_args())


source = args["source"]
dest = args["destination"]
verbose = args["verbose"]
signitures = os.listdir(source)

for signiture in signitures:
    filename = os.path.join(source, signiture)
    try:
        outputname = CropAndSave(filename, dest)
    except:
        print(f"Error happened during proccess of {signiture} .")
        continue
    if verbose:
        print(signiture, "-->", outputname)
print("Done!")