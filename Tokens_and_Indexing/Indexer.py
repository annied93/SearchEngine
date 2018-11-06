import os
import csv

source = 'tokens'
size_key = 'index_size'
index_dir = 'indices_files'
bigram_dir = 'bigrams'
trigram_dir = 'trigrams'
p_dir = 'Position_Search'
stat_dir = 'corpus_statistics'


# Open and read the raw token file
def open_read_file(file):
    file = source + '/' + file
    text = open(file, 'r')
    return text


# Get the unigrams from the token list
def get_uni_words(name, text, uni_index):
    for word in text:
        if word not in uni_index:
            uni_index[word] = dict()
            uni_index[word][name] = 1
        else:
            if name not in uni_index[word]:
                uni_index[word][name] = 1
            else:
                uni_index[word][name] = uni_index[word][name] + 1
        uni_index[word][size_key] = len(uni_index[word])
    return uni_index


# Print the inverted index to a file
def print_index(f_name, index_dict):
    f = open(f_name, 'w+')
    for key in sorted(index_dict.keys()):
        newkey = key[:len(key)-1]
        term = newkey + ' ' + '->'
        f.write(term)
        f.write(' ')
        for doc, val in index_dict[key].items():
            if doc is not size_key:
                f.write('(')
                f.write(doc)
                f.write(',')
                f.write(str(val))
                f.write(')')
                f.write(',')
                f.write(' ')
        f.write('(')
        f.write(size_key)
        f.write(',')
        num = index_dict[key][size_key]
        f.write(str(num))
        f.write(')')
        f.write('\n')
    f.close()


# Make the unigram index
def make_uni_index():
    uni_index = {}
    for file in os.listdir(source):
        if '.DS' not in file:
            print(file)
            ind = file.find('.txt')
            name = file[:ind]
            text = open_read_file(file)
            uni_index = get_uni_words(name, text, uni_index)
    print_index('indices_files/unigram_index.txt', uni_index)
    print('unigram indexing completed')
    return uni_index


# Add the bigrams to the index
def add_bigram_index(file, bigram_index):
    if '.DS' not in file:
        file = bigram_dir + '/' + file
        f = open(file, 'r')
        ind = file.find('.txt')
        length = len(bigram_dir) + 1
        name = file[length:ind]
        for term in f:
            if term not in bigram_index:
                bigram_index[term] = dict()
                bigram_index[term][name] = 1
            else:
                if name not in bigram_index[term]:
                    bigram_index[term][name] = 1
                else:
                    bigram_index[term][name] = bigram_index[term][name] + 1


# Write a list to a file
def write_to_file(index_list, file_name, d):
    f = d + '/' + file_name + '.txt'
    file = open(f, 'w+')
    for line in index_list:
        file.write(line)
        file.write('\n')
    file.close()


# Create the bigrams from the list of tokens
def make_bigrams(file_name, unigram_list):
    i = 0
    bigram_list = []
    while i < len(unigram_list)-2:
        bigram = unigram_list[i][:len(unigram_list[i])-1] + ' ' + unigram_list[i + 1][:len(unigram_list[i+1])-1]
        print(bigram)
        bigram_list.append(bigram)
        i += 1
    write_to_file(bigram_list, file_name, bigram_dir)


# Create the bigram files
def make_bigram_files():
    counter = 0

    for file in os.listdir(source):
        if '.DS' not in file:
            ind = file.find('.txt')
            name = file[:ind]
            text = open_read_file(file)
            unigram_list = []
            for line in text:
                unigram_list.append(line)
            make_bigrams(name, unigram_list)
            counter += 1
            print(str(counter), name, 'done')


# Create the bigram inverted index
def make_bigram_inverted_index(d):
    make_bigram_files()
    bigram_index = {}
    counter = 0
    for file in os.listdir(d):
        add_bigram_index(file, bigram_index)
        print(str(counter), file, 'done')
    for key, l in bigram_index.items():
        bigram_index[key][size_key] = len(l)
    print_index('indices_files/bigram_index.txt', bigram_index)
    print('bigram indexing completed')
    return bigram_index


# Add a trigram file to the index
def add_trigram_index(file, trigram_index):
    file = trigram_dir + '/' + file
    if '.DS' not in file:
        f = open(file, 'r')
        ind = file.find('.txt')
        length = len(trigram_dir) + 1
        name = file[length:ind]
        for term in f:
            if term not in trigram_index:
                trigram_index[term] = dict()
                trigram_index[term][name] = 1
            else:
                if name not in trigram_index[term]:
                    trigram_index[term][name] = 1
                else:
                    trigram_index[term][name] = trigram_index[term][name] + 1


# Make the list of trigrams
def make_trigrams(file_name, unigram_list):
    i = 0
    trigram_list = []
    while i < len(unigram_list)-3:
        trigram = unigram_list[i][:len(unigram_list[i])-1] + ' ' + unigram_list[i + 1][:len(unigram_list[i+1])-1] + ' ' + unigram_list[i+2][:len(unigram_list[i+2])-1]
        print(trigram)
        trigram_list.append(trigram)
        i += 1
    write_to_file(trigram_list, file_name, trigram_dir)


# Create trigram files for storage
def make_trigram_files():
    counter = 0
    for file in os.listdir(source):
        if '.DS' not in file:
            unigram_list = []
            ind = file.find('.txt')
            name = file[:ind]
            text = open_read_file(file)
            for line in text:
                unigram_list.append(line)
            make_trigrams(name, unigram_list)
            counter += 1
            print(str(counter), name, 'done')


# Make the full trigram inverted index
def make_trigram_inverted_index(d):
    counter = 0
    make_trigram_files()
    trigram_index = {}
    for file in os.listdir(d):
        add_trigram_index(file, trigram_index)
        print(str(counter), file, 'done')
        counter += 1
    for key, l in trigram_index.items():
        trigram_index[key][size_key] = len(l)
    print_index('indices_files/trigram_index.txt', trigram_index)
    print('trigram indexing completed')
    return trigram_index


# Get the location of unigrams in the file
def get_unigram_location(file, unigram_index):
    newfile = source + '/' + file
    if '.DS' not in newfile:
        counter = 0
        f = open(newfile, 'r')
        ind = file.find('.txt')
        name = file[:ind]
        for term in f:
            term = term[:len(term)-1]
            if term not in unigram_index:
                unigram_index[term] = dict()
            if name not in unigram_index[term]:
                unigram_index[term][name] = []
            unigram_index[term][name].append(counter)
            counter += 1


# Delta encoding for the unigram locations
def delta_encoding_index(unigram_index):
    for key, l in unigram_index.items():
        for term, val in unigram_index[key].items():
            if term is not size_key:
                temp = unigram_index[key][term]
                carry = temp[0]
                newloc = list()
                newloc.append(carry)
                if len(temp) > 1:
                    for num in temp[1:]:
                        newnum = num - carry
                        newloc.append(newnum)
                        carry += newnum
                    unigram_index[key][term] = newloc
    print('Finish delta encoding')


# Get the inverted index with location storage for unigrams
def get_unigram_location_inverted_index(source):
    unigram_index = {}
    for file in os.listdir(source):
        get_unigram_location(file, unigram_index)
    for key, l in unigram_index.items():
        unigram_index[key][size_key] = len(l)
    print('Done with location inverted index')
    delta_encoding_index(unigram_index)
    print_index('indices_files/unigram_with_location.txt', unigram_index)
    return unigram_index


# Count how many unique terms are there in a document
def count_in_file(d, file):
    temp_list = []
    f = d + '/' + file
    if '.DS' not in f:
        text = open(f, 'r')
        for line in text:
            line = line[:len(line)-1]
            temp_list.append(line)
        return len(set(temp_list))


# Count the terms in each file
def count_terms(d):
    result = {}
    for file in os.listdir(d):
        if '.DS' not in file:
            ind = file.find('.txt')
            f = file[:ind]
            l_result = count_in_file(d, file)
            result[f] = l_result
    return result


# Count the number of unique terms for unigrams, bigrams and trigrams and print result to file
def count():
    unigram_freq = count_terms(source)
    print_dict_to_file(unigram_freq, 'unigram_count.txt', 'indices_files')
    bigram_freq = count_terms(bigram_dir)
    print_dict_to_file(bigram_freq, 'bigram_count.txt', 'indices_files')
    trigram_freq = count_terms(trigram_dir)
    print_dict_to_file(trigram_freq, 'trigram_count.txt', 'indices_files')


# Print a dictionary to file
def print_dict_to_file(l, file_name, d):
    file_name = d + '/' + file_name
    f = open(file_name, 'w+')
    for name, val in l.items():
        f.write(name)
        f.write(': ')
        f.write(str(val))
        f.write('\n')
    f.close()


# Run delta decoding on a list
def delta_decode(list_position):
    if len(list_position) == 1:
        return list_position
    s = list_position[0]
    new_list = list()
    new_list.append(s)
    for num in list_position[1:]:
        new_num = s + num
        new_list.append(new_num)
    print(new_list)
    return new_list


# Check if the number in a certain range is in the list
def check_num(num, list_num, k):
    possible_nums = list(range(num-k, num+k+1))
    for n in possible_nums:
        if n in list_num:
            return True
    return False


# Get all the documents in the inverted index that contains the two terms within k distance
def get_doc_with_proximity(index_list, term1, term2, k):
    result = []
    d1 = {}
    d2 = {}
    for key in index_list.keys():
        if key.lower() == term1.lower():
            d1 = index_list[key]
        if key.lower() == term2.lower():
            d2 = index_list[key]
    if len(d1) != 0 and len(d2) != 0:
        for name in d1.keys():
            if name in d2.keys() and name is not size_key:
                l1 = delta_decode(d1[name])
                l2 = delta_decode(d2[name])
                for num in l1:
                    if check_num(num, l2, k) and name not in result:
                        print(name)
                        result.append(name)
        file_name = term1 + '_' + term2 + '_' + str(k) + '.txt'
        write_to_file(result, file_name, p_dir)
        return result
    else:
        if term1 not in index_list.keys():
            print(term1, 'not in index list')
        else:
            print(term2, 'not in index list')


# Count frequency of a term in the index
def count_freq(word_dict, term):
    temp = word_dict[term]
    sum_freq = 0
    for key, value in temp.items():
        if key is not size_key:
            sum_freq += temp[key]
    return sum_freq


# Create the storage for term and frequency
def term_freq_dict(word_dict):
    term_freqs = {}
    for key in word_dict.keys():
        term_freqs[key] = count_freq(word_dict, key)
    sorted_val = sorted(term_freqs.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_val


# Print term frequency list to a file
def print_freq(file_name, word_dict):
    file_name = stat_dir + '/' + file_name
    with open(file_name, mode='w') as file:
        file.write('Term')
        file.write(' || ')
        file.write('Term frequency')
        file.write('\n')
        for key, val in word_dict:
            file.write(key[:len(key)-1])
            file.write(' || ')
            file.write(str(val))
            file.write('\n')
    file.close()


# Print term, documents that it exists in and the document count to file
def print_doc_and_freq(file_name, word_dict):
    f = stat_dir + '/' + file_name
    with open(f, 'w') as file:
        for key in sorted(word_dict.keys()):
            if key is not size_key:
                print(key[:len(key)-1])
                file.write(key[:len(key)-1])
                file.write(' || ')
                for doc in word_dict[key]:
                    if doc is not size_key:
                        file.write(doc)
                        file.write(' ')
                file.write('|| ')
                val = word_dict[key][size_key]
                print(str(val))
                file.write(str(val))
                file.write('\n')
    file.close()


# Get all the stop words by taking the top 50 words from the frequency file
def __get_stopword(word_dict):
    stopword = []
    counter = 0
    while counter < 50:
        stopword.append(word_dict[counter])
        counter += 1
    return stopword


# Print stop word list to the file
def get_stopword_list(file_name, word_dict):
    f = stat_dir + '/' + file_name
    stopword = __get_stopword(word_dict)
    with open(f, 'w') as file:
        for key, val in stopword:
            file.write(key[:len(key)-1])
            file.write('\n')
    file.close()


# Main function to run the Indexing
def main():
    uni_grams = make_uni_index()
    bigrams = make_bigram_inverted_index(bigram_dir)
    trigrams = make_trigram_inverted_index(trigram_dir)
    unigram_index = get_unigram_location_inverted_index(source)
    count()
    get_doc_with_proximity(unigram_index, 'carbon', 'emission', 5)
    get_doc_with_proximity(unigram_index, 'carbon', 'emission', 10)
    get_doc_with_proximity(unigram_index, 'greenhouse', 'emission', 6)
    get_doc_with_proximity(unigram_index, 'greenhouse', 'emission', 12)

    unigram_freqs = term_freq_dict(uni_grams)
    print_freq('unigram_freq.csv', unigram_freqs)
    print_doc_and_freq('unigram_doc_freq.csv', uni_grams)
    get_stopword_list('unigram_stopword.txt', unigram_freqs)

    bigram_freqs = term_freq_dict(bigrams)
    print_freq('bigram_freq.csv', bigram_freqs)
    print_doc_and_freq('bigram_doc_freq.csv', bigrams)
    get_stopword_list('bigram_stopword.txt', bigram_freqs)

    trigram_freqs = term_freq_dict(trigrams)
    print_freq('trigram_freq.csv', trigram_freqs)
    print_doc_and_freq('trigram_doc_freq.csv', trigrams)
    get_stopword_list('trigram_stopword.txt', trigram_freqs)


main()
