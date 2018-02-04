"""Download images from tumblr"""
import os
import json
import re
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
        print("Total Image Links: " + str(len(links)) + "\nStarting Download...")
        i = 0
        for link in links:
            print("Getting image " + str(i + 1) + " from tumblr", flush=True)
            try:
                head = urllib.request.Request(link, method="HEAD")
                headers = urllib.request.urlopen(head).info()
                f_t = "." + headers['Content-Type'][6:].split(' ')[0]
                if f_t[-1] == ";":
                    f_t = f_t[0:-1]
                if f_t == ".jpeg":
                    f_t = ".jpg"
                if not re.search(r'.(jpg|png|gif)$', f_t):
                    print("Skipping non image " + str(i + 1) + " from tumblr")
                    continue
                elif float(headers['Content-Length']) > 7E6:
                    print("Skipping big file " + str(i + 1) + " from tumblr")
                    continue
                elif float(headers['Content-Length']) < 6.6E4:
                    print("Skipping small file " + str(i + 1) + " from tumblr")
                    continue
                print("Stats for tumblr image " + str(i) + " Size: " + str(headers['Content-Length']) + "B    File type: " + f_t)
                req = urllib.request.Request(link)
                res = urllib.request.urlopen(req, None, 15)
                #Create a jpg file and write the image binary data to it
                with open("images/" + tag + "/tumblr_" + str(i) + f_t, 'wb') as file:
                    data = res.read()
                    file.write(data)
                res.close()

            except TypeError as e:
                print(str(e) + " on tumblr image " + str(i+1))
                continue
                
            except urllib.error.HTTPError as error:  #If there is any HTTPError
                print("Tumblr image " + str(i+1) + " hit HTTPError " + str(error.code))

            except urllib.error.URLError as error:
                print("Tumblr image " + str(i+1) + " hit URLError: " + str(error))

            except IOError as error:   #If there is any IOError
                print("Tumblr image " + str(i+1) + " hit IOError " + str(error))

            i += 1
        print("Done with " + tag + " from tumblr")
    print("Done getting tumblr images")
    return
