import urllib.request
import re
import html
import os
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

wikibase = 'https://share.coursera.org'
baseurl = wikibase+'/wiki/index.php'

categories = [
'Sna',
'Pythonlearn',
'Fantasysf',
'Introfinance',
'Introthermodynamics',
'Modelthinking',
'Nlangp',
'Digitaldemocracy'
]

categories = []

# categories = ['Thinkagain', 'ThinkAgain']

start = 'Main'

# The file cookies should be the cut-pasted from Chrome
# View Developer Console -> Application -> Cookies

# Looks like:
# CAUTH    z0oWnRkXk...QOmPX .coursera.org   /   2017-01-06T18:04:37.776Z ...
# CSRF3-Token 148078....pIC .coursera.org   /   2016-12-03T17:37:35.380Z  ...
# ...
# maestro_login_flag  1   .coursera.org   /   2017-01-06T18:04:37.776Z ...

cookies = list()
hand = open('cookies')
for zap in hand:
    if zap.startswith('_') : continue
    pieces = zap.split()
    if len(pieces) < 6 : continue
    cookies.append(pieces)

# Concatenate the key-value pairs
hdr = ""
for x in cookies:
    if len(hdr) > 0 : hdr += '; '
    hdr += x[0]
    hdr += '='
    hdr += x[1]
    # print(x)
# print(hdr)

# If we have no categories, assume all the categories
# https://share.coursera.org/wiki/index.php/Courses
if len(categories) < 1 : 
    url = baseurl + '/Courses'
    print('Retrieving categories',url)
    opener = urllib.request.build_opener()
    opener.addheaders.append(('Cookie', hdr))
    # let this traceback if there is a problem
    f = opener.open(url)
    web = f.read().decode()
    # print(web)
    # <li><a href="/wiki/index.php/Scigast:Main" title="
    categories = re.findall('<li><a href="/wiki/index.php/([^:]+?)[:"]',web, re.MULTILINE | re.DOTALL)
    print('Found',len(categories),'categories')
    if len(categories) == 0 : quit()
    print(categories)


def save_image(url,fname,hdr) :
    print('Retrieving image',url)
    # Retrieve the Image
    opener = urllib.request.build_opener()
    opener.addheaders.append(('Cookie', hdr))
    try:
        f = opener.open(url)
    except:
        f = None

    if f is not None:
        folder = os.path.dirname(fname)
        if not os.path.exists(folder):
            os.makedirs(folder)
        image = f.read()
        if ( len(image) < 1 ) :
            print('Did not write empty file',fname);
        try:
            out = open(fname,'wb')
        except:
            print('Failed opening file',fname)
            return

        out.write(image)
        out.close()
        print('Wrote',len(data),' characters to '+fname)

count = 100000
pages = 0
images = 0
while len(categories) > 0 :
    category = categories.pop()
    print()
    print('========== Starting Category',category,'with',len(categories),'left to process')

    retrieved = list()
    todo = list()
    todo.append(category+':'+start)

    while len(todo) > 0 : 
        print("----- Pages left to Spider ",len(todo))
        # print('--------',todo)
        # print('========',retrieved)
        count = count - 1
        if count == 0 : break
        page = todo.pop()

        if page in retrieved : 
            print('Already retrieved',url)
            continue
        retrieved.append(page)
        pages = pages + 1

        url = baseurl + '/' + urllib.parse.quote_plus(page)
        print('Retrieving HTML',url)
        # Retrieve the HTML
        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', hdr))
        try:
            f = opener.open(url)
        except:
            f = None

        if f is not None:
            data = f.read().decode()
            # print (data)

            soup = BeautifulSoup(data, 'html.parser')

            # Retrieve all of the img tags
            # <img alt="Snacourselogo.jpeg" src="/wiki/images/thumb/a/a1/Snacourselogo.jpeg/195px-Snacourselogo.jpeg" width="195" height="180" />
            tags = soup('img')
            for tag in tags:
                src = tag.get('src', 'None')
                if src == None : continue
                if not src.startswith('/wiki/images/') : continue
                fname = src[6:]
                url = wikibase + src;
                images = images + 1
                save_image(url,fname,hdr)

            # <a href="/wiki/index.php/File:Snacourselogo.jpeg" class="image">
            tags = soup('a')
            image_map = dict()
            for tag in tags:
                src = tag.get('href', 'None')
                if src == None : continue
                if not src.startswith('/wiki/index.php/File:') : continue

                url = wikibase + src;

                # Retrieve the File: page and pull in the href images
                opener = urllib.request.build_opener()
                opener.addheaders.append(('Cookie', hdr))
                print('Retrieving File page',url);
                try:
                    f = opener.open(url)
                except:
                    f = None

                if f is not None : 
                    fpage = f.read().decode()
                    soup2 = BeautifulSoup(fpage, 'html.parser')
                    tags2 = soup2('a')
                    for tag2 in tags2:
                        href = tag2.get('href', 'None')
                        if href == None : continue
                        if not href.startswith('/wiki/images') : continue
                        fname = href[6:]
                        url = wikibase + href;
                        images = images + 1
                        save_image(url,fname,hdr)
                        image_map[src] = href
                        break # only take the first one


            usesoup = False
            if usesoup : 
                thediv = soup.find("div", {"id": "content"})
                # print(thediv)
                data = str(thediv)
            else : 
                startpos = data.find('<div id="content">')
                endpos = data.find('</div><!-- end of MAINCONTENT div -->')
                data = data[startpos:endpos]+'</div>'

            # get rid of icky stuff
            data = data.replace('<div id="jump-to-nav">Jump to: <a href="#column-one">navigation</a>, <a href="#searchInput">search</a></div>','')
            # <!-- Saved in parser cache with key crowdwiki:pcache:idhash:265-0!*!*!!en!*!* and timestamp 20161127015124 -->
            data = re.sub(r'<!-- Saved in parser cache with key crowdwiki:pcache:.+ -->', '', data)
            
            # Change <a href="/wiki/index.php/File:... to <a href="/wiki/image...
            for k in image_map:
                v = image_map[k]
                data = data.replace(k,v)

            fname = 'html/'+page.replace(':','/')

            if len(data) < 1 :
                print('Did not write zero length file',fname);
                continue

            folder = os.path.dirname(fname)
            if not os.path.exists(folder):
                os.makedirs(folder)

            try:
                out = open(fname,'w')
            except:
                print('Failed opening file',fname)
                continue

            out.write(data)
            out.close()
            print('Wrote',len(data),' characters to '+fname)
    
        # Retrieve the markdown
        url = baseurl + '?title=' + urllib.parse.quote_plus(page) + '&action=edit'
        print('Retrieving markdown',url)

        opener = urllib.request.build_opener()
        opener.addheaders.append(('Cookie', hdr))

        # f = opener.open("https://share.coursera.org/wiki/index.php/Pythonlearn:Main")
        # f = opener.open("https://share.coursera.org/wiki/index.php?title=Pythonlearn:resources-week01&action=edit")

        try:
            f = opener.open(url)
        except: 
            f = None

        if f is not None:
            data = f.read().decode()
            # print (data)
            textarea = re.findall('<textarea.*?>(.*)</textarea>',data, re.MULTILINE | re.DOTALL)
            if len(textarea) < 1 :
                print("No <textarea> found")
                continue

            # Assume the first one
            textarea = html.unescape(textarea[0])
    
            fname = 'markdown/'+page.replace(':','/')
            if len(textarea) < 1 :
                print('Did not write zero length file',fname);
                continue

            folder = os.path.dirname(fname)
            if not os.path.exists(folder):
                os.makedirs(folder)

            try:
                out = open(fname,'w')
            except:
                print('Failed opening file',fname)
                continue

            out.write(textarea)
            out.close()
            print('Wrote',len(textarea),' characters to '+fname)

            # lines = textarea.split("\n")
            # for line in lines:
                # print(line)
    
            refs = re.findall('\[\[(.*?:.*?)\|.*?\]\]', textarea, re.MULTILINE | re.DOTALL)
            for ref in refs :
                pieces = ref.split(':')
                if len(pieces) != 2 : continue
                if pieces[0].lower() != category.lower() : continue
                ref = pieces[1]
                ref = ref.rstrip()
                ref = ref.replace(' ','_')
                if ref in retrieved : continue
                if ref in todo : continue
                todo.append(pieces[0]+':'+ref)

print('Pages retrieved:', pages);
print('Images retrieved:', images);
