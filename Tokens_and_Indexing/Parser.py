import re
import contractions
import nltk
from bs4 import BeautifulSoup
import os

folder = 'unfocused_crawl_html'
out_dir = 'tokens'
punc = [',', '.', ')', '(', '=', '``', '/', '\\', '\'\'', ':', ';', '\'', '#', '&', '!', '$', '?', '%', '+', '++',
        '...', '*', '{', '}', '|', '_', '-']


# Open the file for reading
def __open_file(file):
    file = folder + '/' + file
    text = open(file, 'r')
    return text


# Strip the text of all the elements from the raw HTML to generate clean text
def __strip_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    body = soup.body
    if body is None:
        return None

    for sub in soup.find_all(id='siteSub'):
        sub.decompose()
    for script in soup.find_all('script'):
        script.decompose()
    for wall in soup.find_all(role='navigation'):
        wall.decompose()
    for tag in soup.find_all('table'):
        tag.decompose()
    for thumb in soup.find_all(class_='thumb tright'):
        thumb.decompose()
    for jump in soup.find_all(class_='mw-jump-link'):
        jump.decompose()
    for hat in soup.find_all(class_='hatnote'):
        hat.decompose()
    for tag in soup.find_all('li'):
        tag.decompose()
    for el in soup.find_all(class_='navbox'):
        el.decompose()
    for footer in soup.find_all(role='contentinfo'):
        footer.decompose()
    text = body.get_text(separator='\n')
    return text


# Remove regex from the text
def __remove_regex(text):
    return re.sub('\[[^]]*\]', '', text)


# The main function to strip the raw HTML of the tags and elements, then remove regex
def __remove_noise(text):
    text = __strip_text(text)
    text = __remove_regex(text)
    return text


# Replace some common contractions
def __replace_contractions(text):
    return contractions.fix(text)


# Get all the text in the content
def _get_all_text(name):
    text = __open_file(name)
    text = __remove_noise(text)
    text = __replace_contractions(text)
    ind = text.find('See also')
    if ind == -1:
        ind = text.find('References')
    return text[:ind]


# Remove punctuations from the text
def __remove_punctuation(word):
    if '(' in word:
        word = word.replace('(', '')
    if ')' in word:
        word = word.replace(')', '')
    if '*' in word:
        word = word.replace('*', '')
    if '"' in word:
        word = word.replace('"', '')
    if '=' in word:
        word = word.replace('=', '')
    if '.' in word:
        word = word.replace('.', '')
    if ',' in word:
        word = word.replace(',', '')
    if '/' in word:
        word = word.replace('/', '')
    if '\\' in word:
        word = word.replace('\\', '')
    if word in punc:
        return ''
    if '//' in word or '..' in word:
        return ''
    if word.find('.') == 0 and not(word[1].isdigit()):
        return ''

    return word


# Convert the text to lowercase
def __to_lowercase(word):
    new_word = word.lower()
    if 'wiki' in word:
        return ''
    return new_word


# Tokenize the text
def __tokenizing(text):
    words = nltk.word_tokenize(text)
    print(words)
    unique_words = []
    for word in words:
        new_word = __remove_punctuation(word)
        new_word = __to_lowercase(new_word)
        if new_word is not '':
            unique_words.append(new_word)

    print(unique_words)
    return unique_words


# Print the tokens to file
def _print_to_file(name, words):
    ind = name.find('.html')
    file = out_dir + '/' + name[:ind] + '.txt'
    f = open(file, 'w+')
    for word in words:
        f.write(str(word))
        f.write('\n')
    f.close()


# Main program to execute the Parser program for tokenization
def main():
    for file_name in os.listdir(folder):
        if '.DS' not in file_name:
            text = _get_all_text(file_name)
            words = __tokenizing(text)
            _print_to_file(file_name, words)
    print('Done!')


main()
