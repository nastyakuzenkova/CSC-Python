import functools
import math


# task1
def union(*args):
    return functools.reduce(lambda acc, arg: acc | arg, args)


def digits(num):
    acc = []
    while num:
        acc.append(num % 10)
        num //= 10
    return list(reversed(acc))


def lcm(first, second, *args):
    def lcm_pair(x, y):
        return (x * y) // math.gcd(x, y)

    return functools.reduce(lcm_pair, (first, second,) + args)


def compose(first, second, *args):
    return lambda x: functools.reduce(lambda acc, arg: arg(acc),
                                      reversed((first, second,) + args), x)


# task 2
def once(func):
    result = []

    @functools.wraps(func)
    def inner(*args, **kwargs):
        if not result:
            result.append(func(*args, **kwargs))
        return result[0]

    return inner


def with_arguments(deco):
    @functools.wraps(deco)
    def wrapper(*dargs, **dkwargs):
        def decorator(func):
            result = deco(func, *dargs, **dkwargs)
            functools.update_wrapper(result, func)
            return result

        return decorator

    return wrapper


@with_arguments
def trace_if(func, predicate):
    def inner(*args, **kwargs):
        if predicate(*args, **kwargs):
            print(func.__name__, args, kwargs)
        return func(*args, **kwargs)

    return inner


@with_arguments
def n_times(func, times):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        for _ in range(times):
            func(*args, **kwargs)

    return inner


# task 3-4
def project():
    registrations = []

    def inner_register(func=None, *, depends_on=None):
        depends_on = [] if depends_on is None else depends_on
        executed = []

        if func is None:
            def without_brackets(func):
                return inner_register(func, depends_on=depends_on)
            without_brackets.get_dependencies = lambda: depends_on
            return without_brackets

        @functools.wraps(func)
        def inner_inner_register():
            def execute_dependencies(dependencies):
                for func_name in dependencies:
                    if func_name not in executed:
                        func = globals()[func_name]
                        execute_dependencies(func.get_dependencies())
                        if func_name not in executed:
                            executed.append(func_name)
                            func()

            if func not in registrations:
                registrations.append(func)
            execute_dependencies(depends_on)
            return func()

        inner_inner_register.get_dependencies = lambda: depends_on

        return inner_inner_register

    inner_register.get_all = lambda: \
        list(map(lambda x: x.__name__, registrations))
    return inner_register
