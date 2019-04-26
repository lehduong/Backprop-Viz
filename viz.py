import networkx as nx
import matplotlib.pyplot as plt
from tree import *

def find_edges(head):
    ret = []
    if isinstance(head,Variable):
        return ret
    else:
        left_edges = find_edges(head.lhs)
        right_edges = find_edges(head.rhs)
        ret = ret + left_edges + right_edges
        if head.lhs.name != head.rhs.name:
            ret.append((head.lhs.name,head.name,head.lhs_grad))
            ret.append((head.rhs.name,head.name,head.rhs_grad))
        else:
            ret.append((head.lhs.name,head.name,2*head.lhs_grad))
        return ret

def find_nodes(head):
    ret = dict()
    if isinstance(head,Variable):
        ret[head.name] = 'var'
        return ret
    else:
        left_nodes = find_nodes(head.lhs)
        right_nodes = find_nodes(head.rhs)
        ret.update(left_nodes)
        ret.update(right_nodes)
        ret[head.name] = 'add' if head.op == '+' else 'mul'
        return ret