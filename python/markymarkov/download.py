import os
import hashlib
import scrapelib
import lxml.html


def scrape_story(url, cache_dir):
    story_doc = lxml.html.fromstring(scrapelib.urlopen(url))
    text = story_doc.xpath('//div[@class="storytext xcontrast_txt"]')[0].text_content()

    with open(cache_dir + '/' + hashlib.sha1(url).hexdigest(), 'w') as file:
        file.write(text.encode('utf8', 'ignore'))

    print url

    # check for next page
    base_url = 'http://www.fanfiction.net'
    next = story_doc.xpath('//input[contains(@value, "Next")]/@onclick')
    if next:
        url = base_url + next[0].replace("self.location='", '').strip("'")
        scrape_story(url, cache_dir)

def scrape_stories(url, cache_dir):
    os.path.exists(cache_dir) or os.makedirs(cache_dir)
    doc = lxml.html.fromstring(scrapelib.urlopen(url))
    doc.make_links_absolute(url)
    for link in doc.xpath('//a[@class="stitle"]/@href'):
        scrape_story(link, cache_dir)

