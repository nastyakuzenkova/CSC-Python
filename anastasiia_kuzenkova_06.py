# 1
def peel(cls):
    return set([member for member in dir(cls)
                if not member.startswith('_')])


class AbstractBase:
    def some_method(self):
        pass


class Base(AbstractBase):
    some_attribute = 42
    _internal_attribute = []

    def some_other_method(self):
        pass


class Closeable(Base):
    def close(self):
        pass


assert peel(Closeable) == {'some_other_method',
                           'some_method',
                           'some_attribute',
                           'close'}, \
    'peel: test not passed'


def implements(interface):
    def wrapper(cls):
        interface_members = peel(interface)
        cls_members = peel(cls)
        for member in interface_members:
            assert member not in cls_members, \
                'method {!r} not implemented'.format(member)
        return cls

    return wrapper


# 2, 3
class Expr:
    def __call__(self, **context):
        pass

    def d(self, wrt):
        pass

    def __str__(self):
        pass

    def __neg__(self):
        return Product(Const(-1), self)

    def __pos__(self):
        return self

    def __add__(self, other):
        return Sum(self, other)

    def __sub__(self, other):
        return Sum(self, -other)

    def __mul__(self, other):
        return Product(self, other)

    def __truediv__(self, other):
        return Fraction(self, other)

    def __pow__(self, power, modulo=None):
        return Power(self, power)

    @property
    def is_constexpr(self):
        return False

    @property
    def simplified(self):
        return self


class Const(Expr):
    def __init__(self, value):
        self.value = value

    def __call__(self, **context):
        return self.value

    def d(self, wrt):
        return Const(0)

    def __str__(self):
        return '{}'.format(self.value)

    @property
    def is_constexpr(self):
        return True


class Var(Expr):
    def __init__(self, variable):
        self.variable = variable

    def __call__(self, **context):
        return self.variable \
            if self.variable not in context \
            else context[self.variable]

    def d(self, wrt):
        return Const(1) if self.variable == wrt.variable \
            else Const(0)

    def __str__(self):
        return '{}'.format(self.variable)

C = Const
V = Var


class BinOp(Expr):
    def __init__(self, expr1, expr2):
        self.expr1, self.expr2 = expr1, expr2

    @property
    def is_constexpr(self):
        return self.expr1.is_constexpr and self.expr2.is_constexpr

    @property
    def simplified(self):
        return C(self()) if self.is_constexpr else \
            self.__class__(self.expr1.simplified, self.expr2.simplified)


class Sum(BinOp):
    def __call__(self, **context):
        return self.expr1(**context) + self.expr2(**context)

    def d(self, wrt):
        return Sum(self.expr1.d(wrt), self.expr2.d(wrt))

    def __str__(self):
        return '(+ {} {})'.format(self.expr1, self.expr2)


class Product(BinOp):
    def __call__(self, **context):
        return self.expr1(**context) * self.expr2(**context)

    def d(self, wrt):
        return Sum(Product(self.expr1.d(wrt), self.expr2),
                   Product(self.expr1, self.expr2.d(wrt)))

    def __str__(self):
        return '(* {} {})'.format(self.expr1, self.expr2)


class Fraction(BinOp):
    def __call__(self, **context):
        return self.expr1(**context) / self.expr2(**context)

    def d(self, wrt):
        return Fraction(Sum(Product(self.expr1.d(wrt), self.expr2),
                            Product(Const(-1),
                                    Product(self.expr1, self.expr2.d(wrt)))),
                        Product(self.expr2, self.expr2))

    def __str__(self):
        return '(/ {} {})'.format(self.expr1, self.expr2)


class Power(BinOp):
    def __call__(self, **context):
        a = self.expr1(**context)
        b = self.expr2(**context)
        if b >= 0:
            result = 1
            for i in range(b):
                result = result * a
            return result
        else:
            result = 1
            for i in range(b):
                result = result / a
            return result

    def d(self, wrt):
        return Product(self.expr1.d(wrt),
                       Product(self.expr2,
                               Power(self.expr1, Sum(self.expr2, Const(-1)))))

    def __str__(self):
        return '(** {} {})'.format(self.expr1, self.expr2)


def newton_raphson(expr, initial, threshold):
    next_value = initial - expr(x=initial) / expr.d(V('x'))(x=initial)
    while abs(next_value - initial) > threshold:
        initial = next_value
        next_value = initial - expr(x=initial) / expr.d(V('x'))(x=initial)
    return next_value
