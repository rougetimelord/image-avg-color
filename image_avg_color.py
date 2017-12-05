"""Searches google for images then sorts them by color"""
import os
from shutil import copyfile, rmtree
from time import sleep
import math
from colorthief import ColorThief
import download

#Set up the colors we want to check
COLORS = {
    'red': (255, 0, 0),
    'orange': (255, 128, 0),
    'yellow': (255, 255, 0),
    'lime': (128, 255, 0),
    'green': (0, 255, 0),
    'mint': (0, 255, 128),
    'teal': (0, 128, 255),
    'blue': (0, 0, 255),
    'purple': (128, 0, 255),
    'pink': (255, 0, 128)
}

def _check_images(queries):
    down_queries = []
    images_done = os.listdir("images")
    for term in queries:
        if not term in images_done:
            down_queries.append(term)
    #First we download the images, if we need any
    if down_queries:
        download.start(down_queries)
    return

def get_difference(img_color):
    """Try to match the color with a color we know"""
    if img_color == (255, 255, 255):
        return "white"
    elif img_color == (0, 0, 0):
        return "black"
    #Because we use rgb we can use pythagoran theorem to find the distance and minimize it
    #However it has to be weighted for humans
    color_match = ""
    dist = 3E3
    for color, value in COLORS.items():
        r_co = (img_color[0] + value[0]) / 2
        r_del = math.pow(img_color[0] - value[0], 2)
        g_del = math.pow(img_color[1] - value[1], 2)
        b_co = 2 + ((255 - r_co) / 256)
        b_del = math.pow(img_color[2] - value[2], 2)
        t_del = math.sqrt(r_co * r_del + 4 * g_del + b_co * b_del)
        if t_del < dist:
            dist = t_del
            color_match = color
    return color_match

def main(queries):
    """Do the thing"""
    print("Getting images")
    #Check that images aren't already downloaded
    _check_images(queries)
    images = {}
    print("Sorting images")
    #Go through the folders of everything we searched for
    for dire in queries:
        #Find all the images in the folder
        files = os.listdir("images/" + dire)
        for file in files:
            path = "images/" + dire + "/" + file
            print("Crunching " + path, end='    ', flush=True)
            #Skip images that are too large or small
            if os.stat(path).st_size > 7E6:
                print("Skipping big file")
                continue
            elif os.stat(path).st_size < 6.6E4:
                print("Skipping small file")
                continue
            #Get color
            color_t = ColorThief(path)
            img_color = color_t.get_color(quality=5)
            color_match = get_difference(img_color)
            print("Got " + color_match)
            #Add the image to the stack of images in the matched color
            if color_match in images:
                images[color_match].append(path)
            else:
                images[color_match] = [path]

    print("Done sorting \nCopying...")
    rmtree("./colors/*")
    sleep(100)
    os.makedirs("colors", exist_ok=True)
    #Go through all the colors we did find and copy the images
    for cat, paths in images.items():
        os.makedirs("colors/" + cat, exist_ok=True)
        i = 0
        for img in paths:
            copyfile(img, "colors/" + cat + "/" + str(i) + ".jpg")
            i += 1
    print("Done!")

if __name__ == "__main__":
    #If this is the main instance run, otherwise you have to call main
    print("Queries:")
    QUE = input().replace(", ", ",").split(",")
    print(str(QUE))
    main(QUE)
