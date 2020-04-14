import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from collections import deque

def get_links(link):
    u_Client = urlopen(link)
    ps = soup(u_Client.read(), 'html.parser')
    links_with_text = []
    final_links = []

    t = ps.find('table', class_ = 'infobox vcard')
    if t is not None:
        for a in t.find_all('a', href = True):
            if a.text:
                links_with_text.append(a['href'])
    for a in ps.find_all('a', href=True):
        if a.text:
            links_with_text.append(a['href'])
    for link in links_with_text:
        if '/wiki/' in link and 'https' not in link and '//' not in link and ':' not in link \
                and '(' not in link and 'Main' not in link:
            final_links.append('https://en.wikipedia.org' + link)
    return final_links

def get_name(link):
    u_Client = urlopen(link)
    ps = soup(u_Client.read(), 'html.parser')
    try:
        name = ps.find('div', class_='nickname').text
    except AttributeError:
        return None
    return name

def bfs(links):
    while len(links) != 0:
       link = links[0]
       print(link)
       links.remove(link)
       name = get_name(link)
       if name is not None and 'Trump' in name:
           return True
       else:
           tmp = get_links(link)
           for j in range(len(tmp)):
               if tmp[j] not in links:
                   links.append(tmp[j])
    return False

start_url = 'https://en.wikipedia.org/wiki/Donald_Trump'
path = [start_url]
links_list = list(set(get_links(start_url)))
# q = deque()
# for i in range(len(links_list)):
#     q.append(links_list[i])

bfs(links_list)
