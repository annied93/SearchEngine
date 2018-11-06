import os
import urllib.parse
from bs4 import BeautifulSoup
import codecs


wiki_page = 'https://en.wikipedia.org/wiki/'
main_page = 'https://en.wikipedia.org/wiki/Main_Page'
graph_g1 = dict()
graph_g2 = dict()
outlink_1 = dict()
outlink1_count = dict()
outlink_2 = dict()
outlink2_count = dict()
counter = 0


# Task 1
def check_link(url):
    wiki = (url.find(wiki_page) != -1)
    not_main = (url.lower() != main_page.lower()) and (url.lower() != wiki_page.lower())
    not_fragment = (url.find("#") == -1)
    not_admin = (url.find(":", 6) == -1)
    return wiki and not_main and not_fragment and not_admin


def print_graph(d, name):
    graph_file = name
    f = open(graph_file, 'w+')
    for k, v in d.items():
        f.write(k)
        for item in v:
            f.write(' ')
            f.write(item)
        f.write('\n')

    f.close()


def print_g2(d):
    graph_file = 'g2.txt'
    f = open(graph_file, 'w+')
    for k, v in d.items():
        if 'green' in k.lower():
            f.write(k)
            for item in v:
                f.write(' ')
                f.write(item)
            f.write('\n')
    f.close()


def draw_base_g1(file_name):
    global graph_g1
    file_obj = open(file_name, "r")

    for line in file_obj:
        comma = line.find(", anchor")
        name = line[len(wiki_page):comma]
        graph_g1[name] = list()

    file_obj.close()
    return graph_g1


def draw_outlinks_g1(file_name):
    global outlink_1
    file_obj = open(file_name, "r")

    for line in file_obj:
        comma = line.find(", anchor")
        name = line[len(wiki_page):comma]
        outlink_1[name] = []
        outlink1_count[name] = 0

    file_obj.close()
    # print(outlink_1)


def get_outlinks_1(folder):
    global outlink_1
    global outlink1_count
    for file_name in os.listdir(folder):
        print(file_name)
        index = file_name.find('.html')
        name = file_name[:index]
        print(name)

        f = folder + '/' + file_name
        print(f)
        if '.DS' not in f:
            file_obj = codecs.open(f, 'r', encoding='utf-8')
            soup = BeautifulSoup(file_obj, 'html.parser')

            links = soup.find_all('a', href=True)
            print(links)
            for link in links:
                link_href = urllib.parse.urljoin(wiki_page, link.get('href'))
                link_str = str(link_href)
                if check_link(link_str):
                    token = link_str[len(wiki_page):]
                    print(token)
                    if (name in outlink_1.keys()) and (token in outlink_1.keys()) and (token not in outlink_1[name]) \
                            and (name.lower() != token.lower()):
                        outlink_1[name].append(token)
                        outlink1_count[name] += 1


# def print_outlink_1(d):
#     graph_file = 'outlink_1.txt'
#     f = open(graph_file, 'w+')
#     for k, v in d.items():
#         f.write(k)
#         f.write(' ')
#         f.write(str(v))
#         f.write('\n')
#
#     f.close()


def draw_base_g2(file_name):
    global graph_g2
    file_obj = open(file_name, "r")

    for line in file_obj:
        comma = line.find(", anchor")
        name = line[len(wiki_page):comma]
        graph_g2[name] = list()

    file_obj.close()
    return graph_g2


def get_links_g1(folder):
    global graph_g1
    for file_name in os.listdir(folder):
        print(file_name)
        index = file_name.find('.html')
        name = file_name[:index]
        print(name)

        f = folder + '/' + file_name
        print(f)
        if '.DS' not in f:
            file_obj = codecs.open(f, 'r', encoding='utf-8')
            soup = BeautifulSoup(file_obj, 'html.parser')

            links = soup.find_all('a', href=True)
            print(links)
            for link in links:
                link_href = urllib.parse.urljoin(wiki_page, link.get('href'))
                link_str = str(link_href)
                if check_link(link_str):
                    token = link_str[len(wiki_page):]
                    print(token)
                    if (token in graph_g1.keys()) and (name not in graph_g1[token]) and (name.lower() != token.lower()):
                        graph_g1[token].append(name)
    return graph_g1


def get_links_g2(folder):
    global graph_g2
    for file_name in os.listdir(folder):
        index = file_name.find('.html')
        name = file_name[:index]

        f = folder + '/' + file_name
        if '.DS' not in f:
            file_obj = codecs.open(f, 'r', encoding='utf-8')
            soup = BeautifulSoup(file_obj, 'html.parser')

            links = soup.find_all('a', href=True)
            for link in links:
                link_href = urllib.parse.urljoin(wiki_page, link.get('href'))
                link_str = str(link_href)
                if check_link(link_str):
                    token = link_str[len(wiki_page):]
                    if (name in graph_g2.keys()) and (token in graph_g2.keys()) and (name not in graph_g2[token]) \
                            and (name.lower() != token.lower()):
                            graph_g2[token].append(name)
    return graph_g2


#Task 2
def calculate_l1(pr, new_pr):
    l1_val = 0
    for p in pr.keys():
        l1_val += abs(new_pr[p] - pr[p])
    return l1_val


def converge(l1, err, name):
    length = len(l1)
    global counter
    file_name = 'l1_values' + name + '.txt'
    if length < 4:
        return False
    if (l1[0] < err) and (l1[1] < err) and (l1[2] < err) and (l1[3] < err):
        f = open(file_name, 'w+')
        while length > 0:
            f.write('Iteration: ')
            f.write(str(counter+1))
            f.write(' , value: ')
            f.write(str(l1[length-1]))
            f.write('\n')
            length -= 1
            counter += 1
        f.close()
        return True
    return False


def find_sink(outlink_list):
    sinks = []
    for name, count in outlink_list.items():
        if name != '' and count == 0:
            print('sink:')
            print(name)
            sinks.append(name)
    return sinks


def find_max_in(d):
    max_in = 0
    key = ''
    for k, v in d.items():
        if max_in < len(d[k]):
            max_in = len(d[k])
            key = k
    return key


def count_source(g):
    count = 0
    for k, v in g.items():
        if len(g[k]) == 0:
            count += 1
    return count


def page_rank_g1(g, alpha, error, name):
    stats = name + '_stat.txt'
    f = open(stats, 'w+')
    max_out = find_max_index(outlink1_count)
    num_max_out = outlink1_count[max_out]
    max_in = find_max_in(g)
    num_max_in = len(g[max_in])

    f.write('Max in-degree: ')
    f.write(str(num_max_in))
    f.write('\n')
    f.write('Max out-degree: ')
    f.write(str(num_max_out))
    f.write('\n')

    l1 = []
    count = 0
    pr = {}
    new_pr = {}
    if len(g) == 0:
        return {}
    n = len(g.keys())
    print('n is', n)

    sinks = find_sink(outlink1_count)
    f.write('Number of sinks: ')
    f.write(str(len(sinks)))
    f.write('\n')

    source = count_source(g)
    f.write('Number of sources: ')
    f.write(str(source))
    f.write('\n')

    f.write('\n')
    f.write('Values of sum of all PageRanks while iterating:')
    f.write('\n')

    pr_val = 1.0 / n
    for k in g.keys():
        pr[k] = pr_val

    while not converge(l1, error, name):
        # print(str(converge(l1, error, name)))
        sink_pr = 0
        for sink in sinks:
            sink_pr += pr[sink]

        for p in g.keys():
            new_pr_val = (1.0 - alpha)/n
            val = ((alpha * sink_pr)/n)
            new_pr_val += val
            for q in g[p]:
                out_num = float(outlink1_count[q])
                new_pr_val += ((alpha * pr[q]) / out_num)
            new_pr[p] = new_pr_val
        l1_val = calculate_l1(pr, new_pr)
        l1.insert(0, l1_val)
        count += 1
        print(count)
        sum_pr = 0
        for p in g.keys():
            sum_pr += new_pr[p]
        for p in g.keys():
            pr[p] = new_pr[p]
            new_pr[p] = 0
        f.write('Iteration: ')
        f.write(str(count))
        f.write(', value: ')
        f.write(str(sum_pr))
        f.write('\n')

    f.close()
    final_g = order_page(pr)
    return final_g


def page_rank_g2(g, alpha, error, name):
    stats = name + '_stat.txt'
    f = open(stats, 'w+')
    max_out = find_max_index(outlink2_count)
    num_max_out = outlink2_count[max_out]
    max_in = find_max_in(g)
    num_max_in = len(g[max_in])

    f.write('Max in-degree: ')
    f.write(str(num_max_in))
    f.write('\n')
    f.write('Max out-degree: ')
    f.write(str(num_max_out))
    f.write('\n')

    l1 = []
    count = 0
    pr = {}
    new_pr = {}
    if len(g) == 0:
        return {}
    n = len(g.keys())
    print('n is', n)

    sinks = find_sink(outlink2_count)
    f.write('Number of sinks: ')
    f.write(str(len(sinks)))
    f.write('\n')

    source = count_source(g)
    f.write('Number of sources: ')
    f.write(str(source))
    f.write('\n')

    f.write('\n')
    f.write('Values of sum of all PageRanks while iterating:')
    f.write('\n')

    pr_val = 1.0 / n
    for k in g.keys():
        pr[k] = pr_val

    while not converge(l1, error, name):
        print(str(converge(l1, error, name)))
        sink_pr = 0
        for sink in sinks:
            print(sink)
            sink_pr += pr[sink]

        for p in g.keys():
            new_pr_val = (1.0 - alpha)/n
            val = ((alpha * sink_pr)/n)
            new_pr_val += val
            for q in g[p]:
                out_num = float(outlink2_count[q])
                new_pr_val += ((alpha * pr[q]) / out_num)
            new_pr[p] = new_pr_val
        l1_val = calculate_l1(pr, new_pr)
        l1.insert(0, l1_val)
        count += 1
        print(count)
        sum_pr = 0
        for p in new_pr.keys():
            sum_pr += new_pr[p]
        for p in pr.keys():
            pr[p] = new_pr[p]
            new_pr[p] = 0
        f.write('Iteration: ')
        f.write(str(count))
        f.write(', value: ')
        f.write(str(sum_pr))
        f.write('\n')

    f.close()
    final_g = order_page(pr)
    return final_g


def find_max_index(d):
    max_val = None
    key = ''
    if len(d.keys()) != 0:
        for k in d.keys():
            if max_val is None or max_val < d[k]:
                key = k
                max_val = d[k]
        return key


def order_page(pr):
    g = {}
    size = len(pr)
    while size != 0:
        max_index = find_max_index(pr)
        if max_index is not None:
            g[max_index] = pr[max_index]
            del pr[max_index]
        size -= 1
    return g


def print_pagerank(g, name):
    count = 0
    pr_name = name + '_pagerank.txt'
    f = open(pr_name, 'w+')

    for page, score in g.items():
        if count < 50:
            f.write(page)
            f.write(', score:')
            f.write(str(score))
            f.write('\n')
            count += 1
    f.close()


def draw_outlinks_g2(file_name):
    global outlink_2
    file_obj = open(file_name, "r")

    for line in file_obj:
        comma = line.find(", anchor")
        name = line[len(wiki_page):comma]
        outlink_2[name] = []
        outlink2_count[name] = 0
    file_obj.close()
    # print(outlink_1)


def get_outlinks_2(folder):
    global outlink_2
    global outlink2_count
    for file_name in os.listdir(folder):
        print(file_name)
        index = file_name.find('.html')
        name = file_name[:index]
        print(name)

        f = folder + '/' + file_name
        print(f)
        if '.DS' not in f:
            file_obj = codecs.open(f, 'r', encoding='utf-8')
            soup = BeautifulSoup(file_obj, 'html.parser')

            links = soup.find_all('a', href=True)
            print(links)
            for link in links:
                link_href = urllib.parse.urljoin(wiki_page, link.get('href'))
                link_str = str(link_href)
                if check_link(link_str):
                    token = link_str[len(wiki_page):]
                    print(token)
                    if (name in outlink_2.keys()) and (token in outlink_2.keys()) and (token not in outlink_2[name]) \
                            and (name.lower() != token.lower()):
                        outlink_2[name].append(token)
                        outlink2_count[name] += 1


def reset():
    global counter
    counter = 0


#Task 3
def count_inlink(d):
    inlink1_count = dict()
    for key, value in d.items():
        inlink1_count[key] = 0
        for v in value:
            inlink1_count[key] += 1
    return inlink1_count


def inlink_page_rank(g):
    result = {}
    inlink_count = count_inlink(g)
    i = 0
    while i < 20:
        index = find_max_index(inlink_count)
        result[index] = inlink_count[index]
        del inlink_count[index]
        i += 1
    return result


def print_inlink_rank(d, name):
    f = open(name, 'w+')
    for k, v in d.items():
        link = wiki_page + k
        f.write(link)
        f.write(', count:')
        f.write(str(v))
        f.write('\n')
    f.close()


def page_rank_4_iterations(g, alpha, name):
    stats = name + '_stat.txt'
    iter = 0
    f = open(stats, 'w+')
    max_out = find_max_index(outlink1_count)
    num_max_out = outlink1_count[max_out]
    max_in = find_max_in(g)
    num_max_in = len(g[max_in])

    f.write('Max in-degree: ')
    f.write(str(num_max_in))
    f.write('\n')
    f.write('Max out-degree: ')
    f.write(str(num_max_out))
    f.write('\n')

    l1 = []
    count = 0
    pr = {}
    new_pr = {}
    if len(g) == 0:
        return {}
    n = len(g.keys())
    print('n is', n)

    sinks = find_sink(outlink1_count)
    f.write('Number of sinks: ')
    f.write(str(len(sinks)))
    f.write('\n')

    source = count_source(g)
    f.write('Number of sources: ')
    f.write(str(source))
    f.write('\n')

    f.write('\n')
    f.write('Values of sum of all PageRanks while iterating:')
    f.write('\n')

    pr_val = 1.0 / n
    for k in g.keys():
        pr[k] = pr_val

    while iter < 4:
        sink_pr = 0
        for sink in sinks:
            print(sink)
            sink_pr += pr[sink]

        for p in g.keys():
            new_pr_val = (1.0 - alpha)/n
            val = ((alpha * sink_pr)/n)
            new_pr_val += val
            for q in g[p]:
                out_num = float(outlink1_count[q])
                new_pr_val += ((alpha * pr[q]) / out_num)
            new_pr[p] = new_pr_val
        l1_val = calculate_l1(pr, new_pr)
        l1.insert(0, l1_val)
        count += 1
        print(count)
        sum_pr = 0
        for p in new_pr.keys():
            sum_pr += new_pr[p]
        for p in pr.keys():
            pr[p] = new_pr[p]
            new_pr[p] = 0
        f.write('Iteration: ')
        f.write(str(count))
        f.write(', value: ')
        f.write(str(sum_pr))
        f.write('\n')
        iter += 1

    for val in l1:
        f.write('L1 values:')
        f.write('\n')
        f.write(str(val))

    f.close()
    final_g = order_page(pr)
    return final_g


def main():
    draw_base_g1('result_crawl_Carbon_footprint.txt')
    get_links_g1('unfocused_crawl_html')
    print_graph(graph_g1, 'g1.txt')
    draw_outlinks_g1('result_crawl_Carbon_footprint.txt')
    get_outlinks_1('unfocused_crawl_html')
    print_graph(outlink_1, 'outlink_g1.txt')

    final_g1_85 = page_rank_g1(graph_g1, 0.85, 0.001, 'g1_0.85')
    print_pagerank(final_g1_85, 'g1_0.85')
    reset()
    final_g1_5 = page_rank_g1(graph_g1, 0.5, 0.001, 'g1_0.5')
    print_pagerank(final_g1_5, 'g1_0.5')
    reset()
    final_g1_65 = page_rank_g1(graph_g1, 0.65, 0.001, 'g1_0.65')
    print_pagerank(final_g1_65, 'g1_0.65')
    reset()
    final_g1_4_iter = page_rank_4_iterations(graph_g1, 0.85, 'g1_4_iter')
    print_pagerank(final_g1_4_iter, 'g1_4_iter')

    inlink_rank = inlink_page_rank(graph_g1)
    print_inlink_rank(inlink_rank, 'inlink_rank_g1.txt')

    draw_base_g2('result_crawl_Carbon_footprint_focused.txt')
    get_links_g2('focused_crawl_html')
    print_g2(graph_g2)
    draw_outlinks_g2('result_crawl_Carbon_footprint_focused.txt')
    get_outlinks_2('focused_crawl_html')
    print_graph(outlink_2, 'outlink_g2.txt')
    final_g2 = page_rank_g2(graph_g2, 0.85, 0.001, 'g2')
    print_pagerank(final_g2, 'g2')


main()

