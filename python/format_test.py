from typing import List
import torch
import argparse

# out comment

# https://docs.python.org/3/library/ast.html
# how tf does this work
# def f(a: 'annotation', b=1, c=2, *d, e, f=3, **g):
#     pass

def empty_test():
    return "hi"

def wow7(*args, **kwargs) -> float:
    ''''''
    return None

def single_kwarg(arg1 = 'asdf'):
    return "hi"

def wow5(arg1: str):
    temp = 1
    temp1 = 300
    temp2 = 300
    temp5 = 300
    return None

def wow1(arg1: str) -> float:
    temp = 1
    temp1 = 300
    temp2 = 300
    temp5 = 300
    return None

def wow6(arg1) -> float:
    temp = 1
    temp1 = 300
    temp2 = 300
    temp5 = 300
    return None

if __name__ == "__main__":
    print('asdfhmmm')

def wow(arg11111: str, arg2: dict) -> float:
    # asdf
    temp = 1
    temp1 = 300 # inline comment

    for i in range(3):
        print(i)
    return None


def wow2(arg1: str, arg2: dict, kwarg1: str = '') -> float:
    return None

def wow3(
        arg1: str, arg2: dict, 
        kwarg1: str = '', kwargs2: float = 0
    ) -> float:
    return None

def wow4(
        arg1: str, arg2: dict, 
        asdf
    ) -> float:
    ''''''
    return None

