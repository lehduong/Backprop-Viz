from parsimonious.grammar import Grammar
import numpy as np
import re

grammar = Grammar(
    """
        expr = (term add expr) /  term
        term = (factor mul term) /  factor
        factor = (left expr right) / const 
        add = "+"
        mul = "*"
        left = "("
        right = ")"
        const = ~"[A-Z 0-9]*"i
     """)


def variableNameParsing(txt: str):
    ret = list()
    regex = r"[A-Za-z]+"
    matches = re.finditer(regex, txt, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        ret.append(match.group())

    return ret
