outlink = {}
graph = {}
c = 0


def calculate_l1(pr, new_pr):
    l1_val = 0
    for p in pr.keys():
        print(new_pr[p])
        print(pr[p])
        l1_val += abs(new_pr[p] - pr[p])
    print('l1 is ', l1_val)
    return l1_val


def converge(l1, err):
    length = len(l1)
    counter = 0
    if length < 4:
        return False
    if (l1[0] < err) and (l1[1] < err) and (l1[2] < err) and (l1[3] < err):
        f = open('l1_values.txt', 'w+')
        while length > 0:
            f.write('Iteration: ')
            f.write(str(counter+1))
            f.write(str(l1[length-1]))
            f.write('\n')
            length -= 1
        f.close()
        return True
    return False


def find_sink(outlink_list):
    sinks = []
    for name, count in outlink_list.items():
        if name != str(0) and count == str(0):
                sinks.append(name)
                print(name)
    print(sinks)
    return sinks


def page_rank_g(g, alpha, error):
    global c
    l1 = []
    counter = 0
    pr = {}
    new_pr = {}
    if len(g) == 0:
        return {}
    n = len(g.keys())
    print('n is', n)

    sinks = find_sink(outlink)
    pr_val = 1.0 / n
    for k in g.keys():
        pr[k] = pr_val

    while not converge(l1, error):
        print(str(converge(l1, error)))
        sink_pr = 0
        for sink in sinks:
            sink_pr += pr[sink]

        for p in g.keys():
            new_pr_val = (1.0 - alpha)/n
            val = ((alpha * sink_pr)/n)
            new_pr_val += val
            for q in graph[p]:
                out_num = float(outlink[q])
                new_pr_val += ((alpha * pr[q])/ out_num)
            new_pr[p] = new_pr_val
        l1_val = calculate_l1(pr, new_pr)
        l1.insert(0, l1_val)
        counter += 1
        print(counter)
        for p in pr.keys():
            pr[p] = new_pr[p]
            new_pr[p] = 0
    final_g = order_page(pr)
    return final_g


def find_max_index(d):
    max = None
    key = ''
    if len(d.keys()) != 0:
        for k in d.keys():
            if max is None or max < d[k]:
                key = k
                max = d[k]
        return key


def order_page(pr):
    g = []
    size = len(pr)
    while size != 0:
        max_index = find_max_index(pr)
        if max_index is not None:
            g.append(max_index)
            del pr[max_index]
        size -= 1
    return g


def main():
    f = open('test.txt', 'r')
    print(f)
    for line in f:
        string = line.split()
        # print(line)
        # print(string)
        graph[string[0]] = []
        for s in string[1:]:
            graph[string[0]].append(s)
    f.close()
    print(graph)
    for k in graph.keys():
        outlink[k] = 0
    for p in graph.keys():
        for i in graph[p]:
            outlink[i] += 1
    print(outlink)

    final = page_rank_g(graph, 0.85, 0.001)
    print(final)


main()