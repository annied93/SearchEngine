from bs4 import BeautifulSoup
import gc
import urllib.parse
import os.path
import time
import requests

# Global variables - constants for use and storage data structures
base = 'https://en.wikipedia.org/'
wiki_page = 'https://en.wikipedia.org/wiki/'
main_page = 'https://en.wikipedia.org/wiki/Main_Page'
depth_reached = 0
storage = {}
parent = None
visited = []
max_pages = 1000
header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


class Page:
    def __init__(self, url, depth, url_parent):
        self._url = url
        self._depth = depth
        self._content = None
        self._parent = url_parent
        self._anchor = None

    @property
    def url(self):
        return self._url

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def depth(self):
        return self._depth

    @property
    def parent(self):
        return self._parent

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, url_anchor):
        self._anchor = url_anchor


def change_parent(value):
    global parent
    parent = value


def check_list(string, list_str):
    for s in list_str:
        if str(s.lower()) == str(string.lower()):
            return False
    return True


def seen_url(url):
    url_lower = url.lower()
    return (url in visited) or (url_lower in visited)


def check_link(url):
    wiki = (url.find(wiki_page) != -1)
    not_main = (url.lower() != main_page.lower()) and (url.lower() != wiki_page.lower())
    not_fragment = (url.find("#") == -1)
    not_admin = (url.find(":", 6) == -1)
    return wiki and not_main and not_fragment and not_admin


def crawl(url, current_dept, max_depth, key_word):
    if key_word is None:
        unfocused_crawl(url, current_dept, max_depth)
    else:
        focused_crawl(url, current_dept,max_depth, key_word)


def write_file(url, content, type_flag):
    if type_flag is False:
        file_path = 'unfocused_crawl_html/'
        name = os.path.join(file_path, url[len(wiki_page):] + '.html')
    else:
        file_path = 'focused_crawl_html/'
        name = os.path.join(file_path, url[len(wiki_page):] + '.html')
    f = open(name, 'w+')
    f.write(content)
    f.close()


def web_crawl(url, depth, key_word, type_flag):
    global parent
    global visited

    change_parent(storage[url].parent)
    frontier = list()

    try:
        page = requests.get(url, headers=header, timeout=5)

        visited.append(url.lower())

        content = page.text
        write_file(url, content, type_flag)

        storage[url].content = content
        soup = BeautifulSoup(content, 'html.parser')

        body_links = soup.find_all('a')

        for link in body_links:
            link_href = urllib.parse.urljoin(wiki_page, link.get('href'))
            url_link = str(link_href)
            url_anchor = link.text
            if check_link(url_link) and (url_link not in frontier) and seen_url(url) \
                    and contain_key(url_link, url_anchor, key_word):
                frontier.append(url_link)
                if url_link not in storage.keys():
                    storage.update({url_link: Page(url_link, depth + 1, url)})
                    storage[url_link].anchor = url_anchor
        return frontier

    except Exception:
        return


def unfocused_crawl(seed, current_depth, max_depth):
    global depth_reached
    global parent
    global visited
    global max_pages
    counter = 0

    file_name_1 = "result_crawl_"
    file_name_1 += seed[len(wiki_page):]
    file_name_1 += ".txt"
    f = open(file_name_1, "w+")

    url_list = []

    curr_depth = current_depth
    storage[seed] = Page(seed, curr_depth, parent)
    frontier = web_crawl(seed, curr_depth, None, False)

    url_list.append(seed)
    f.write(seed)
    f.write(', anchor: ')
    f.write(str(storage[seed].anchor))
    f.write(', depth: ')
    f.write(str(storage[seed].depth))
    f.write(', parent: ')
    f.write(str(storage[seed].parent))
    f.write('\n')
    counter += 1
    print(counter)

    curr_depth = 2
    length = len(frontier)
    child_at_depth = length
    temp = 0
    flag = 0

    while len(url_list) < max_pages and curr_depth <= max_depth and len(frontier) != 0:
        if flag == 0:
            flag = 1

        if child_at_depth == 0:
            curr_depth += 1
            flag = 0
            child_at_depth = temp
            temp = 0

        url = frontier.pop(0)
        if url.lower() not in url_list:
            gc.disable()
            #time.sleep(1)
            temp_frontier = web_crawl(url, curr_depth, None, False)
            gc.enable()
            if temp_frontier is not None:
                frontier = frontier + temp_frontier
                temp += len(temp_frontier)
        child_at_depth -= 1
        if check_list(url, url_list):
            url_list.append(url)
            f.write(url)
            f.write(', anchor: ')
            f.write(str(storage[url].anchor))
            f.write(', depth: ')
            f.write(str(storage[url].depth))
            f.write(', parent: ')
            f.write(str(storage[url].parent))
            f.write('\n')
            counter += 1
            print(counter)

    depth_reached += curr_depth

    depth = "Max depth reached:"
    depth += str(depth_reached)
    depth += '\n'
    f.write('\n')
    f.write(depth)
    f.close()


def contain_key(url, anchor, key_word):
    if key_word is None:
        return True
    url_contain = (key_word.lower() in url.lower())
    if anchor is None:
        return url_contain
    elif anchor is not None:
        anchor_contain = (key_word.lower() in anchor.lower())
        return url_contain or anchor_contain


def focused_crawl(seed, current_depth, max_depth, key_word):
    global depth_reached
    global parent
    global visited
    global max_pages
    counter = 0

    file_name_1 = "result_crawl_"
    file_name_1 += seed[len(wiki_page):]
    file_name_1 += '_focused.txt'
    f = open(file_name_1, "w+")

    url_list = []

    curr_depth = current_depth
    storage[seed] = Page(seed, curr_depth, parent)
    frontier = web_crawl(seed, curr_depth, key_word, True)
    if contain_key(seed, storage[seed].anchor, key_word):
        url_list.append(seed)
        f.write(seed)
        f.write(', anchor: ')
        f.write(str(storage[seed].anchor))
        f.write(', depth: ')
        f.write(str(storage[seed].depth))
        f.write(', parent: ')
        f.write(str(storage[seed].parent))
        f.write('\n')
        counter += 1
        print(counter)

    curr_depth = 2
    length = len(frontier)
    child_at_depth = length
    temp = 0
    flag = 0

    while len(url_list) < max_pages and curr_depth <= max_depth and len(frontier) != 0:
        if flag == 0:
            flag = 1

        if child_at_depth == 0:
            curr_depth += 1
            flag = 0
            child_at_depth = temp
            temp = 0

        url = frontier.pop(0)
        if url.lower() not in url_list:
            gc.disable()
            #time.sleep(1)
            temp_frontier = web_crawl(url, curr_depth, key_word, True)
            gc.enable()
            if temp_frontier is not None:
                frontier = frontier + temp_frontier
                temp += len(temp_frontier)
        child_at_depth -= 1
        if check_list(url, url_list) and (contain_key(url, storage[url].anchor, key_word)):
            url_list.append(url)
            f.write(url)
            f.write(', anchor: ')
            f.write(str(storage[url].anchor))
            f.write(', depth: ')
            f.write(str(storage[url].depth))
            f.write(', parent: ')
            f.write(str(storage[url].parent))
            f.write('\n')
            counter += 1
            print(counter)

    depth_reached += curr_depth

    depth = "Max depth reached:"
    depth += str(depth_reached)
    depth += '\n'
    f.write('\n')
    f.write(depth)
    f.close()


def main():
    current_depth = 1
    max_depth = 6
    seed_1 = 'https://en.wikipedia.org/wiki/Carbon_footprint'
    #crawl(seed_1, current_depth, max_depth, None)
    crawl(seed_1, current_depth, max_depth, "green")


main()




