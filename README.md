# Extract Wiki Content from Coursera Wiki

This is a bit of clunky bit of Python code - but it works with a little attention to extract
content from Coursera's mediaWiki instance.  In essense, you give this application a list
of categories and the `wiki_extract.py` will spider the URLs and extract the following:

* It reads the HTML version of the page and pulls out the main content `<div>`.  It then parses
that, looking for thumbnail images, and pull down the images down and stores them in the `images`
folder. It also looks for `File:` urls, visits the `File:` page, grabs the original large image
and also pulls that into `images`.  Then the `File:` hrefs are patched to point to the actual
image file.  Then the patched HTML is stored in a folder per category under the `html` folder

* Then it reads the "edit" page and pulls out the Markdown from the `<textarea>` tag.  It cleans 
this up a bit and stores it under the `markdown` folder with folders organized by category.

When this is done, the `images` and `html` folders are served up through `index.php` as long as 
this folder is checked out into the `/wiki` path in a web server.  If you go to `/wiki/index.php`
you see the list of the categories that are present.

# Using this Code

First you need to log into the wiki with an account that can edit on the wiki using Chrome.
Then go into View Developer Console -> Application -> Cookies and select all 
the cookies using click at the top and shift click at the bottom and past that 
into the `cookies` file as plain text.  An exmaple file is provided as `cookies-sample.txt`
and should look as follows:

    CAUTH    z0oWnRkXk...QOmPX .coursera.org   /   2017-01-06T18:04:37.776Z ...
    CSRF3-Token 148078....pIC .coursera.org   /   2016-12-03T17:37:35.380Z  ...
    ...
    maestro_login_flag  1   .coursera.org   /   2017-01-06T18:04:37.776Z ...

Then edit the file `wiki_extract.py` and update the list of categories.

Since I happen to also be storing the html, markdown, and images for my categories
in this github repo, you probably want to remove these folders before starting the spider.
I like using github as I run the spider over and over as it allows me to see 
what is new and changed.  I set things up and then just did a checkin after every
run or two to allow me to see how my corpus was evolving.

The spider will remake the image, html, and markdown directories if needed and spiders
the entire corpus every run.   But unless you are fixing something in the process
or spidering new content, even with a full re-spider, github will not see any changes.
