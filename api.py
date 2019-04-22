from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from abc import ABC
import numpy as np
from NameCreator import NameCreator
#from parser import *
from visitor import IniVisitor, BackwardVisitor
from tree import Variable, Expression, create_binary_tree
from viz import find_edges, find_nodes
import networkx as nx
import matplotlib.pyplot as plt

text = "b*(c+a*(k+a))+a*x"

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


def parse(text: str):
    print("Expr: "+text)
    tree = grammar.parse(text)
    iv = IniVisitor()
    output = iv.visit(tree)
    NameCreator.resetCounter()
    lookup = dict()
    lookup['b'] = Variable('b', 5)
    lookup['c'] = Variable('c', 7)
    lookup['a'] = Expression(lookup['b'], '+', lookup['c'], 'a')

    tree = create_binary_tree(output, lookup)
    bv = BackwardVisitor()
    ctx = {'grad': 1, 'op': '+', 'value': 0}
    bv.visit(tree, ctx)
    print(tree)
    d = dict()
    for k in lookup:
        d[k] = lookup[k].value
    print(d)
    #####################

    e = find_edges(tree)
    v = find_nodes(tree)
    colormap = list()
    for k in v:
        if v[k] == 'var':
            colormap.append('#3F51B5')
        elif v[k] == 'add':
            colormap.append('#FFC107')
        else:
            colormap.append('#F44336')
    v = list(v)
    #colormap = np.arange(len(colormap))/10
    e.reverse()
    G = nx.DiGraph()

    G.add_nodes_from(v)
    for edge in e:
        src, tgt, w = edge
        G.add_edge(tgt, src, weight=w)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    norm = plt.Normalize(1, 4)
    cmap = plt.cm.RdYlGn
    fig, ax = plt.subplots()
    plt.title('draw_networkx')
    pos = nx.drawing.nx_agraph.graphviz_layout(
        G, prog='dot', args='-Nfontsize=10 -Nwidth="10" -Nheight="1" -Nmargin=0 -Gfontsize=8')
    nx.draw(G, pos, with_labels=True, arrows=True,
            node_size=1500, node_color=colormap)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()


parse(text)
