import gzip
import bz2
import io
import random


# task 1
def capwords(string, sep=None):
    capwords_list = list(map(lambda word: word.capitalize(),
                             string.split(sep)))
    if sep is not None:
        return sep.join(capwords_list)
    else:
        return ' '.join(capwords_list)


assert capwords('foo,,bar,', sep=',') == 'Foo,,Bar,', \
    'capwords: test 1 not passed.'
assert capwords(' foo \nbar\n') == 'Foo Bar', \
    'capwords: test 2 not passed.'


def cut_suffix(string, suffix):
    if string.endswith(suffix):
        return string.rpartition(suffix)[0]
    return string


assert cut_suffix('foobar', 'bar') == 'foo', \
    'cut_suffix: test 1 not passed.'
assert cut_suffix('foobar', 'foo') == 'foobar', \
    'cut_suffix: test 2 not passed.'


def boxed(string, fill, pad):
    string = ' ' + string + ' '
    n_center = len(string) + pad * 2
    string_frame = fill * n_center
    return '\n'.join([string_frame,
                      string.center(n_center, fill), string_frame])


def find_all(string, substring):
    acc = []
    start = 0
    end = len(string)
    while string.find(substring, start, end) != -1:
        found_index = string.find(substring, start, end)
        acc.append(found_index)
        start = found_index + 1
    return acc


assert find_all('abracadabra', 'a') == [0, 3, 5, 7, 10],\
    'find_all: test not passed'


def common_prefix(first, second, *args):
    strings = list((first, second) + args)
    min_string = min(strings)
    while False in list(map(lambda string:
                            string.startswith(min_string), strings)):
        min_string = min_string[:len(min_string) - 1]
    return min_string


assert common_prefix('abra', 'abracadabra', 'abrasive') \
       == 'abra', 'common_prefix: test 1 not passed'
assert common_prefix('abra', 'foobar') \
       == '', 'common_prefix: test 2 not passed'


# task 2
def reader(path, mode='rb', encoding=None):
    extension = path.rpartition('.')[2]
    if extension == 'gz' or extension == 'gzip':
        return gzip.open(path, mode=mode, encoding=encoding)
    if extension == 'bz2' or extension == 'bzip2':
        return bz2.open(path, mode=mode, encoding=encoding)
    return open(path)


def parse_shebang(path):
    file = open(path)
    line = file.readline()
    emp, sep, shebang_path = line.partition('#!')
    if shebang_path == '':
        return None
    return shebang_path.strip()


# task 3
def words(file):
    words_list = []
    for line in file:
        words_list += line.split(' ')
    return list(filter(lambda w: w, words_list))


handle = io.StringIO("""Ignorance    is the curse of God;
 knowledge is the wing wherewith we fly to heaven.""")
assert words(handle) == ['Ignorance', 'is', 'the', 'curse', 'of',
                         'God;\n', 'knowledge', 'is', 'the',
                         'wing', 'wherewith', 'we', 'fly', 'to', 'heaven.'],\
    'words : test not passed'


def transition_matrix(word_list):
    matrix = {}
    for i in range(len(word_list) - 2):
        word_u = word_list[i]
        word_v = word_list[i + 1]
        word_next = word_list[i + 2]
        if (word_u, word_v) not in matrix:
            matrix[word_u, word_v] = []
        if word_next not in matrix[word_u, word_v]:
            matrix[word_u, word_v].append(word_next)
    return matrix


handle = io.StringIO("""Ignorance    is the curse of God;
 knowledge is the wing wherewith we fly to heaven.""")
language = words(handle)
m = transition_matrix(language)
assert m['is', 'the'] == ['curse', 'wing'], \
    'transition_matrix: test not passed'


def markov_chain(words_list, transition_matrix_dict, n):
    first_word = random.choice(words_list)
    second_word = random.choice(words_list)
    sentence = [first_word, second_word]
    while n > 2:
        if (first_word, second_word) in transition_matrix_dict:
            third_word = \
                random.choice(transition_matrix_dict[first_word, second_word])
        else:
            third_word = random.choice(words_list)
        sentence.append(third_word)
        first_word = second_word
        second_word = third_word
        n -= 1
    return ' '.join(sentence)


def snoop_says(path, n):
    words_list = words(open(path))
    transition_matrix_dict = transition_matrix(words_list)
    return markov_chain(words_list, transition_matrix_dict, n)
