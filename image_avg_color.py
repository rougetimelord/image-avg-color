"""Searches google for images then sorts them by color"""
import os
from shutil import copyfile
import math
from multiprocessing import Process
from colorthief import ColorThief
import google_download
import tumblr_download

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
    'pink': (255, 0, 128),
    'black': (0, 0, 0),
    'white': (255, 255, 255)
}

def _check_images(queries):
    down_queries = []
    images_done = os.listdir("images")
    for term in queries:
        if not term in images_done:
            down_queries.append(term)
    #First we download the images, if we need any
    if down_queries:
        print("Getting images")
        google_que = down_queries[:]
        tumblr_que =down_queries[:]
        google_p = Process(target=google_download.start, args=(google_que,))
        tumblr_p = Process(target=tumblr_download.start, args=(tumblr_que,))
        tumblr_p.start()
        google_p.start()
        tumblr_p.join()
        google_p.join()
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
    if dist <= 500:
        return color_match
    elif dist <= 1E3:
        return color_match + 'ish'
    else:
        return 'unsorted'

def main(queries):
    """Do the thing"""
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
    os.makedirs("colors", exist_ok=True)
    #Go through all the colors we did find and copy the images
    for cat, paths in images.items():
        os.makedirs("colors/" + cat, exist_ok=True)
        i = 0
        for img in paths:
            f_t = img[-4:]
            print(img + " is file type " + f_t)
            copyfile(img, "colors/" + cat + "/" + str(i) + f_t)
            i += 1
    print("Done!")

if __name__ == "__main__":
    #If this is the main instance run, otherwise you have to call main
    print("Queries:")
    QUE = input().replace(", ", ",").split(",")
    print(str(QUE))
    main(QUE)
