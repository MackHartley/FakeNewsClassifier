from bs4 import BeautifulSoup
import re
import urllib
import requests



# Not used anymore
def process_page(url):  #return the title (string), content (list) and all the out links (list)
    try:
        page = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print('URL not valid.')
        return '', ''
    soup = BeautifulSoup(page, "lxml")
    titles = soup.find_all('title')

    title = ''
    if len(titles) != 0:
        title_str = str(titles[0])
        title = clean_string(title_str)

    content = ''
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        para = str(p)
        content = content + ' ' +  clean_string(para)

    outlinks = []
    prefix = find_prefix(url)
    for link in soup.findAll('a', href=True):
        url = link.get('href')
        if len(url) == 0:
            continue
        elif url[0] == '/':
            url = prefix + url
        elif len(url) < 5:
            continue
        elif url[0:4] != 'http':
            continue
        outlinks.append(url)


    return title, content, outlinks


# Not used anymore
def get_title(url):   # Get the first title from a page
    try:
        page = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print('HTTPError')
        return ''
    soup = BeautifulSoup(page, "lxml")
    titles = soup.find_all('title')
    if len(titles) != 0:
        title_str = str(titles[0])
        clean_str = clean_string(title_str)
        return clean_str
    else:
        return ''


def clean_string(line):   # <p>Hello</p> -> Hello
    result = re.sub(r'<[^<>]*>', '', line)
    return result


def find_prefix(url):   # E.g : Find http://www.bbc.com from http://www.bbc.com/news/blogs-trending-43745629
    ind = url.index('.com')
    if ind == -1:
        print('No prefix found')
        return ''
    else:
        return url[0 : ind + 4]


def append_query(q):   # insert the query term (title) into the API url
    query = {'q' : q}
    q = urllib.parse.urlencode(query)
    return "https://newsapi.org/v2/everything?"+q+"&apiKey=2d5cb94ff25c4b1184dcd4986fb5fb1a"


def search_news(q):  # Search the title using Google API, return a json object
    news_url = append_query(q)
    try:
        r = requests.get(url=news_url)
        return r.json()
    except urllib.error.HTTPError:
        print('URL not valid.')
        return

def get_domain(title):
    search_result = search_news(title)
    if search_result['status'] != 'ok':
        print('Google API Error!')
        return None
    elif len(search_result['articles']) == 0:
        print('Can not find the article.')
        return None
    else:
        print('Find most related article: ' + search_result['articles'][0]['title'])
        print(search_result)
        url = search_result['articles'][0]['url']
        domain_name = url.split('/')[2].replace('www.', '')
        return domain_name


def API(url):  # Search the title using Google API, return a json object
    try:
        r = requests.get(url=url)
        return r.json()
    except urllib.error.HTTPError:
        print('URL not valid.')
        return
