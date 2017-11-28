import os
from shutil import copyfile
import math
from colorthief import ColorThief
import download

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
    'brown': (173, 115, 0),
    'white': (255, 255, 255),
    'black': (0, 0, 0)
}

def main(queries):
    print("Getting images")
    images = {}
    #download.start(queries)
    print("Sorting images")
    for dir in queries:
        files = os.listdir(dir)
        for file in files:
            path = dir + "/" + file
            print("Crunching " + path)
            if os.stat(path).st_size > 7E6:
                print("Skipping big file")
                continue
            elif os.stat(path).st_size < 6.6E4:
                print("Skipping small file")
                continue
            color_t = ColorThief(path)
            img_color = color_t.get_color(quality=5)
            color_match = ""
            dist = 1E3
            for color, value in COLORS.items():
                r_del = math.pow((img_color[0] - value[0]), 2)
                g_del = math.pow((img_color[1] - value[1]), 2)
                b_del = math.pow((img_color[2] - value[2]), 2)
                t_del = math.sqrt(r_del + g_del + b_del)
                if t_del < dist:
                    dist = t_del
                    color_match = color
            print("Got " + color_match)
            if color_match in images:
                images[color_match].append(path)
            else:
                images[color_match] = [path]
    print("Done sorting \n Copying...")
    for cat, paths in images:
        os.makedirs(cat, exist_ok=True)
        i = 0
        for img in paths:
            copyfile(img, cat + "/" + i + ".jpg")
    print("Done!")

if __name__ == "__main__":
    print("Queries: \n")
    #QUE = input().split(",")
    QUE = ['beach']
    main(QUE)
