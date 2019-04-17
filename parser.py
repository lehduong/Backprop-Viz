from parsimonious.grammar import Grammar
import numpy as np 

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
