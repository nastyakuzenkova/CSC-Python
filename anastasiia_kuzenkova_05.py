import functools
import collections

Factor = collections.namedtuple('Factor', ['elements', 'levels'])


def factor(seq):
    code_seq = []
    code_dict = collections.OrderedDict()
    current_code = 0
    for s in seq:
        if s not in code_dict:
            code_dict[s] = current_code
            current_code += 1
        code_seq.append(code_dict[s])
    return Factor(code_seq, code_dict)


assert factor(['a', 'a', 'b']) == \
       Factor(elements=[0, 0, 1],
              levels=collections.OrderedDict([('a', 0), ('b', 1)]))

assert factor(['a', 'b', 'c', 'b', 'a']) == \
       Factor(elements=[0, 1, 2, 1, 0],
              levels=collections.OrderedDict([('a', 0), ('b', 1), ('c', 2)]))

CacheInfo = \
    collections.namedtuple('CacheInfo',
                           ['hits', 'misses', 'maxsize', 'currsize'])


def lru_cache(func=None, *, maxsize=64):
    cache = collections.OrderedDict()
    misses = 0
    hits = 0

    if func is None:
        def without_brackets(func):
            return lru_cache(func, maxsize=maxsize)

        return without_brackets

    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key in cache:
            nonlocal hits
            hits += 1
            cache.move_to_end(key)
            return cache[key]
        else:
            nonlocal misses
            misses += 1
            result = func(*args, **kwargs)
            if len(cache) >= maxsize:
                if cache:
                    cache.popitem()
            else:
                cache[key] = result
            return result

    inner.cache_info = lambda: CacheInfo(hits, misses, maxsize, len(cache))

    def clear():
        cache.clear()
        nonlocal misses
        misses = 0
        nonlocal hits
        hits = 0

    inner.cache_clear = clear
    return inner


def group_by(seq, key_func):
    result = collections.defaultdict(list)
    for elem in seq:
        result[key_func(elem)].append(elem)
    return result


def invert(d):
    result = collections.defaultdict(set)
    for key in d:
        result[d[key]].add(key)
    return result


def export_graph(g, labels, path):
    file = open(path, 'w')
    file.write('graph {\n')
    edges = []
    for v in g:
        file.write('{0} [label=\"{1}\"]\n'.format(v, labels[v]))
        for paired_v in g[v]:
            if v <= paired_v and (v, paired_v) not in edges:
                file.write('{0} -- {1}\n'.format(v, paired_v))

    file.write('}\n')
    file.close()


def hamming(seq1, seq2):
    assert len(seq1) == len(seq2)
    length = len(seq1)
    distance = 0
    for i in range(length):
        if seq1[i] != seq2[i]:
            distance += 1
    return distance


def build_graph(words, mismatch_percent):
    g = {w: [] for w in range(len(words))}
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if len(words[i]) == len(words[j]):
                if mismatch_percent * len(words[i]) / 100 >= \
                        hamming(words[i], words[j]):
                    g[i].append(j)
                    g[j].append(i)
    return g


def find_connected_components(g):
    visited = [False] * len(g)
    components = []

    def dfs(v):
        visited[v] = True
        for u in g[v]:
            if not visited[u]:
                component.append(u)
                dfs(u)

    for vertex in range(len(g)):
        if not visited[vertex]:
            component = [vertex]
            dfs(vertex)
            components.append(component)

    return components


def find_consensus(words):
    result = []
    frequency_dict = {w: [] for w in range(len(words[0]))}
    for i in range(len(words)):
        for j in range(len(words[i])):
            frequency_dict[j].append(words[i][j])
    for i in frequency_dict:
        c = collections.Counter(frequency_dict[i])
        result.append((c.most_common(1)[0][0]))
    return ''.join(result)


def correct_typos(words, mismatch_percent):
    new_words = [word for word in words]
    g = build_graph(words, mismatch_percent)
    components = find_connected_components(g)
    for component in components:
        component_words = []
        for index in component:
            component_words.append(words[index])
        word = find_consensus(component_words)
        for index in component:
            new_words[index] = word
    return new_words
