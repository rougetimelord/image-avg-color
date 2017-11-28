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
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
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
            items.append(next_img[0])      #Append all the links in the list named 'Links'
            page = page[next_img[1]:]
    return items

#Download Image Links
def start(queries):
    for keyword in queries:
        print("Searching for " + keyword + "\n")
        items = []
        search = keyword.replace(' ', '%20')
        #make a search keyword  directory
        try:
            os.makedirs(keyword)
        except OSError as e:
            if e.errno != 17:
                raise
        url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        raw_html = download(url)
        items = _images_get_all_items(raw_html)
        #print ("Image Links = "+str(items))
        print("Total Image Links \n" + str(len(items)) + "\n")

        print("Starting Download...")

        ## To save imges to the same directory
        # IN this saving process we are just skipping the URL if there is any error
        i = 0
        for link in items:
            try:
                req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
                res = urllib.request.urlopen(req, None, 15)
                with open(keyword + "/" + str(i) + ".jpg", 'wb') as f:
                    data = res.read()
                    f.write(data)
                res.close()

            except urllib.error.HTTPError as e:  #If there is any HTTPError
                print("HTTPError " + str(e.code))

            except urllib.error.URLError as e:
                print("URLError" + str(e.errno))

            except IOError as e:   #If there is any IOError
                print("IOError" + str(e.errno))

            i += 1
        print("done with " + keyword + "\n")
    print("Done getting images")
    return
