"""Download images from tumblr"""
import os
import json
import urllib.request
import urllib.error
from key import tumblr_key as key

def _download(url):
    try:
        req = urllib.request.Request(url)
        resp = urllib.request.urlopen(req)
        resp_data = resp.read().decode('utf-8')
        return resp_data

    except urllib.error.HTTPError as error:
        print("HTTPError " + str(error.code))

    except urllib.error.URLError as error:
        print("URLError " + str(error))

def _get_images(url):
    data = json.loads(_download(url))
    print(data.keys())
    post_data = data['response']
    items = []
    i = 1
    for post in post_data:
        if post['type'] == "photo":
            photos = post['photos']
            for photo in photos:
                items.append(photo['original_size']['url'])
                i += 1
    print("Got " + str(i) + " images \n")
    return items

def start(queries):
    for tag in queries:
        print("Searching for " + tag + " on tumblr \n")
        search = tag.replace(' ', '%20')
        #make the keyword url sanitized
        os.makedirs("images/" + tag, exist_ok=True)
        url = "https://api.tumblr.com/v2/tagged?tag=" + search + "&api_key=" + key
        links = _get_images(url)
        print("Total Image Links: \n" + str(len(links)))
        print("Starting Download... \n")
        i = 0
        for link in links:
            print('Getting image ' + str(i + 1), end='    ', flush=True)
            try:
                req = urllib.request.Request(link)
                res = urllib.request.urlopen(req, None, 15)
                #Create a jpg dile and write the image binary data to it
                f_t = "." + res.info()['Content-Type'][6:]
                f_t = f_t.split(' ')[0]
                if f_t == ".jpeg":
                    f_t = ".jpg"
                print("Size: " + str(res.info()['Content-Length']) + "B    File type: " + f_t)
                with open("images/" + tag + "/tumblr_" + str(i) + f_t, 'wb') as file:
                    data = res.read()
                    file.write(data)
                res.close()

            except urllib.error.HTTPError as error:  #If there is any HTTPError
                print("HTTPError " + str(error.code))

            except urllib.error.URLError as error:
                print("URLError " + str(error))

            except IOError as error:   #If there is any IOError
                print("IOError " + str(error))

            i += 1
        print("Done with " + tag + "\n")
    print("Done getting tumblr images")
    return

start(['neon'])
