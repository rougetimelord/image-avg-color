import os
import urllib.request
import urllib.error

def download(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        resp_data = str(resp.read())
        return resp_data
    except Exception as e:
        print(str(e))

def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:
        #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        #Search through the html for images and take the links
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line+1)
        end_content = s.find(',"ow"', start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return (content_raw, end_content)

def _images_get_all_items(page):
    items = []
    while True:
        next_img = _images_get_next_item(page)
        if next_img[0] == "no_links":
            break
        else:
            items.append(next_img[0])
            #Add the link we just found and chop the html so the same link doesn't come up twice
            page = page[next_img[1]:]
    return items

def start(queries):
    """Do the thing"""
    for keyword in queries:
        print("Searching for " + keyword)
        items = []
        search = keyword.replace(' ', '%20')
        #make the keyword url sanitized
        try:
            os.makedirs(keyword, exist_ok=True)
        except OSError as e:
            raise
        url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        #Get the html of the google images page then search it for links
        raw_html = download(url)
        items = _images_get_all_items(raw_html)
        print("Total Image Links: " + str(len(items)))
        print("Starting Download...")
        #Save imgaes to their directories
        #Also skip the image if anythin is wrong 
        i = 0
        for link in items:
            try:
                req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
                res = urllib.request.urlopen(req, None, 15)
                #Create a jpg dile and write the image binary data to it
                with open(keyword + "/" + str(i) + ".jpg", 'wb') as f:
                    data = res.read()
                    f.write(data)
                res.close()

            except urllib.error.HTTPError as e:  #If there is any HTTPError
                print("HTTPError " + str(e.code))

            except urllib.error.URLError as e:
                print("URLError " + str(e))

            except IOError as e:   #If there is any IOError
                print("IOError " + str(e))

            except Exception as e:
                print("Other error " + str(e))

            i += 1
        print("Done with " + keyword + "\n")
    print("Done getting images")
    return
