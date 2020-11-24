"""
This module for arithmetic funcs
"""


def add(a_arg: int, b_arg: int):
    """
    this function for addition
    """
    return a_arg + b_arg


def sub(a_arg: int, b_arg: int):
    """
    this function for substraction
    """
    return a_arg - b_arg


def mult(a_arg: int, b_arg: int):
    """
    this function for mult
    """
    return a_arg * b_arg


def div(a_arg: int, b_arg: int):
    """
    this function for div
    """
    return a_arg // b_arg


if __name__ == "__main__":
    varA, varB = 10, 20
    resss = add(varA, varB) + sub(varA, varB) * \
        div(varA, varB) / mult(varA, varB)
    print("Result:", resss)
