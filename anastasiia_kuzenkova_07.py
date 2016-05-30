import traceback
import functools
from enum import Enum


class assert_raises:
    def __init__(self, error_type):
        self.error_type = error_type

    def __enter__(self):
        pass

    def __exit__(self, exc_type, *other_exc_info):
        assert exc_type, 'did not raise {!r}'.format(self.error_type.__name__)
        return exc_type == self.error_type


class closing:
    def __init__(self, opener):
        self.opener = opener

    def __enter__(self):
        self.handle = self.opener
        return self.handle

    def __exit__(self, *exc_info):
        self.handle.close()
        del self.handle


class log_exceptions:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            traceback.print_exception(exc_type, exc_val, exc_tb)
            return True


def with_context(manager):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            with manager:
                func(*args, **kwargs)
        return inner

    return wrapper


class Op(Enum):
    NEXT = ('Ook.', 'Ook?')
    PREV = ('Ook?', 'Ook.')
    INC = ('Ook.', 'Ook.')
    DEC = ('Ook!', 'Ook!')
    PRINT = ('Ook!', 'Ook.')
    INPUT = ('Ook.', 'Ook!')
    START_LOOP = ('Ook!', 'Ook?')
    END_LOOP = ('Ook?', 'Ook!')


def ook_tokenize(source_code):
    all_op = {op.value: op for op in Op}
    commands = []
    instructions = source_code.split(' ')
    for command in zip(instructions[::2], instructions[1::2]):
        commands.append(all_op[command])
    return commands


print(ook_tokenize("Ook. Ook! Ook! Ook."))


