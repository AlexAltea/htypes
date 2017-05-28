#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Native types.
"""

import operator

# Helpers
def get_value(value, bits, signed):
    if isinstance(value, nint):
        value = value.v
    mask = 2**bits - 1
    if signed and value & (1 << (bits - 1)):
        return value | ~mask
    else:
        return value & mask

def ensure_native(lhs, rhs):
    assert isinstance(lhs, nint) or isinstance(rhs, nint)
    if not isinstance(lhs, nint):
        lhs = nint(lhs, rhs.b, rhs.s)
    if not isinstance(rhs, nint):
        rhs = nint(rhs, lhs.b, lhs.s)
    return lhs, rhs

# Promotions
def promote_bits(lhs, rhs):
    return max(lhs.b, rhs.b)
def promote_signed(lhs, rhs):
    return lhs.s & rhs.s

# Operators
def op_binary(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    bits = promote_bits(lhs, rhs)
    signed = promote_signed(lhs, rhs)
    result = op(
        get_value(lhs, bits, signed),
        get_value(rhs, bits, signed))
    return nint(result, bits, signed)

def op_relational(lhs, rhs, op):
    lhs, rhs = ensure_native(lhs, rhs)
    bits = promote_bits(lhs, rhs)
    signed = promote_signed(lhs, rhs)
    lhs_int = get_value(lhs, bits, signed)
    rhs_int = get_value(rhs, bits, signed)
    return op(lhs_int, rhs_int)

# Native Integer
class nint(object):
    def __init__(self, value=0, bits=32, signed=True):
        self.b = bits
        self.s = signed
        self.m = (1 << bits) - 1
        self.set(value)

    def set(self, value):
        if self.s and value & (1 << (self.b - 1)):
            self.v = value | ~self.m
        else:
            self.v = value & self.m

    def __str__(self):
        return str(int(self))
    def __int__(self):
        return int(self.v)

    def op_binary_inplace(self, value, op):
        result_int = op(self.v, value)
        self.set(result_int)
        return self

    # Binary operations
    def __add__       (self, rhs):  return op_binary(self, rhs, operator.__add__)
    def __sub__       (self, rhs):  return op_binary(self, rhs, operator.__sub__)
    def __mul__       (self, rhs):  return op_binary(self, rhs, operator.__mul__)
    def __floordiv__  (self, rhs):  return op_binary(self, rhs, operator.__floordiv__)
    def __truediv__   (self, rhs):  return op_binary(self, rhs, operator.__floordiv__)
    def __mod__       (self, rhs):  return op_binary(self, rhs, operator.__mod__)
    def __and__       (self, rhs):  return op_binary(self, rhs, operator.__and__)
    def __or__        (self, rhs):  return op_binary(self, rhs, operator.__or__)
    def __xor__       (self, rhs):  return op_binary(self, rhs, operator.__xor__)
    def __lshift__    (self, rhs):  return op_binary(self, rhs, operator.__lshift__)
    def __rshift__    (self, rhs):  return op_binary(self, rhs, operator.__rshift__)

    # Reflected binary operation
    def __radd__      (self, lhs):  return op_binary(lhs, self, operator.__add__)
    def __rsub__      (self, lhs):  return op_binary(lhs, self, operator.__sub__)
    def __rmul__      (self, lhs):  return op_binary(lhs, self, operator.__mul__)
    def __rfloordiv__ (self, lhs):  return op_binary(lhs, self, operator.__floordiv__)
    def __rtruediv__  (self, lhs):  return op_binary(lhs, self, operator.__floordiv__)
    def __rmod__      (self, lhs):  return op_binary(lhs, self, operator.__mod__)
    def __rand__      (self, lhs):  return op_binary(lhs, self, operator.__and__)
    def __ror__       (self, lhs):  return op_binary(lhs, self, operator.__or__)
    def __rxor__      (self, lhs):  return op_binary(lhs, self, operator.__xor__)
    def __rlshift__   (self, lhs):  return op_binary(lhs, self, operator.__lshift__)
    def __rrshift__   (self, lhs):  return op_binary(lhs, self, operator.__rshift__)

    # In-place operations
    def __iadd__      (self, v):  return self.op_binary_inplace(v, operator.__add__)
    def __isub__      (self, v):  return self.op_binary_inplace(v, operator.__sub__)
    def __imul__      (self, v):  return self.op_binary_inplace(v, operator.__mul__)
    def __ifloordiv__ (self, v):  return self.op_binary_inplace(v, operator.__floordiv__)
    def __itruediv__  (self, v):  return self.op_binary_inplace(v, operator.__floordiv__)
    def __imod__      (self, v):  return self.op_binary_inplace(v, operator.__mod__)
    def __iand__      (self, v):  return self.op_binary_inplace(v, operator.__and__)
    def __ior__       (self, v):  return self.op_binary_inplace(v, operator.__or__)
    def __ixor__      (self, v):  return self.op_binary_inplace(v, operator.__xor__)
    def __ilshift__   (self, v):  return self.op_binary_inplace(v, operator.__lshift__)
    def __irshift__   (self, v):  return self.op_binary_inplace(v, operator.__rshift__)

    def __eq__        (self, rhs):  return op_relational(self, rhs, operator.__eq__)
    def __ne__        (self, rhs):  return op_relational(self, rhs, operator.__ne__)
    def __lt__        (self, rhs):  return op_relational(self, rhs, operator.__lt__)
    def __le__        (self, rhs):  return op_relational(self, rhs, operator.__le__)
    def __ge__        (self, rhs):  return op_relational(self, rhs, operator.__ge__)
    def __gt__        (self, rhs):  return op_relational(self, rhs, operator.__gt__)


# Shorthands
class int8(nint):
    def __init__(self, value=0):
        super(int8, self).__init__(value, bits=8, signed=True)
class int16(nint):
    def __init__(self, value=0):
        super(int16, self).__init__(value, bits=16, signed=True)
class int32(nint):
    def __init__(self, value=0):
        super(int32, self).__init__(value, bits=32, signed=True)
class int64(nint):
    def __init__(self, value=0):
        super(int64, self).__init__(value, bits=64, signed=True)

class uint8(nint):
    def __init__(self, value=0):
        super(uint8, self).__init__(value, bits=8, signed=False)
class uint16(nint):
    def __init__(self, value=0):
        super(uint16, self).__init__(value, bits=16, signed=False)
class uint32(nint):
    def __init__(self, value=0):
        super(uint32, self).__init__(value, bits=32, signed=False)
class uint64(nint):
    def __init__(self, value=0):
        super(uint64, self).__init__(value, bits=64, signed=False)