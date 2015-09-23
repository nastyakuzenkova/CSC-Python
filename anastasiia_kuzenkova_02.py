# task1
def compose(func1, func2):
    return lambda x: func1(func2(x))


def constantly(x):
    def inner(*args, **kwargs):
        return x
    return inner


def flip(func):
    def inner(*args, **kwargs):
        return func(*reversed(args), **kwargs)
    return inner


def curry(func, *args):
    def inner(*new_args):
        return func(*(args + new_args))
    return inner


# task2
def enumerate(a, start=0):
    return zip(range(start, len(a) + start), a)


def which(predicate, a):
    return [i for i in range(len(a)) if predicate(a[i])]


def all(predicate, a):
    return len(a) == len(list(filter(predicate, a)))


def any(predicate, a):
    return len(list(filter(predicate, a))) > 0


# task3
OK, ERROR = "OK", "ERROR"


def char(ch):
    def inner(input):
        if not input:
            return ERROR, "eof", input
        elif input[0] != ch:
            return ERROR, "expected " + ch + " got " + input[0], input
        else:
            return OK, ch, input[1:]
    return inner


def any_of(chars):
    def inner(input):
        if not input:
            return ERROR, "eof", input
        elif input[0] not in chars:
            return ERROR, "expected any of " + chars + " got " + input[0], input
        else:
            return OK, input[0], input[1:]
    return inner


def chain(*args):
    def inner(input):
        saved_input = input
        acc = []
        for arg in args:
            tag, result, leftover = arg(input)
            if tag == ERROR:
                return tag, result, saved_input
            acc.append(result)
            input = leftover
        return OK, acc, input
    return inner


def choice(*args):
    def inner(input):
        for arg in args:
            tag, result, leftover = arg(input)
            if tag == OK:
                return tag, result, leftover
        return ERROR, 'none matched', input
    return inner


def many(parser, empty=True):
    def inner(input):
        acc = []
        tag, result, leftover = parser(input)
        if not empty and tag == ERROR:
            return tag, result, leftover
        while tag == OK:
            acc.append(result)
            input = leftover
            tag, result, leftover = parser(input)
        return OK, acc, leftover
    return inner


def skip(parser):
    def inner(input):
        tag, result, leftover = parser(input)
        return tag, None if tag == OK else result, leftover
    return inner


def transform(p, f):
    def inner(input):
        tag, res, leftover = p(input)
        return tag, f(res) if tag == OK else res, leftover
    return inner


def sep_by(parser, separator):
    def inner(input):
        tag, first_result, first_leftover = parser(input)
        if tag == ERROR:
            return tag, first_result, first_leftover
        tag, result, leftover = many(transform(chain(separator, parser), lambda xs: xs[1]))(first_leftover)
        return tag, result if tag == ERROR else [first_result] + result, leftover
    return inner


def parse(parser, input):
    tag, result, leftover = parser(input)
    assert tag == OK and not leftover, (result, leftover)
    return result


lparen, rparen = skip(char("(")), skip(char(")"))
ws = skip(many(any_of(" \r\n\t"), empty=False))
number = transform(many(any_of("1234567890"), empty=False), lambda digits: int("".join(digits)))
op = any_of("+-*/")


def sexp(input):
    args = sep_by(choice(number, sexp), ws)
    p = chain(lparen, op, skip(ws), args, rparen)
    p = transform(p, lambda res: (res[1], res[3]))
    return p(input)
