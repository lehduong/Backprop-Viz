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

text = "a+b+c*a"

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

def parse_expr(text,lookup):
    tree = grammar.parse(text)
    iv = IniVisitor()
    output = iv.visit(tree)
    return create_binary_tree(output,lookup)

def create_lookup(list):
    #list = [("a","1"),("b","2"),("c","a+b")]
    lookup = dict()
    for name,value in list:
        try:
            v = float(value)  
            tensor = Variable(name,float(value))
            lookup[name] = tensor
        except ValueError:
            tensor = parse_expr(value,lookup)
            tensor.name = name
            lookup[name] = tensor
    return lookup

def plot_grad_tree_from_expr(expr:str,lookup):
    #expr = "a+b*d+c"
    #lookup
    grammar_tree = grammar.parse(expr)
    
    iv = IniVisitor()
    output = iv.visit(grammar_tree)
    forward_tree = create_binary_tree(output,lookup)
    
    v = BackwardVisitor()
    ctx = {'grad':1,'op':'+','value':0}
    v.visit(forward_tree,ctx)

    plt = plot_grad_tree_from_tree(forward_tree)
    plt.show()

def plot_grad_tree_from_tree(tree):
    v = find_nodes(tree)
    e = find_edges(tree)

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
    #pos = nx.drawing.nx_agraph.graphviz_layout(G, prog='dot', args='-Nfontsize=10 -Nwidth="10" -Nheight="1" -Nmargin=0 -Gfontsize=8')
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True,
            node_size=1500, node_color=colormap)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    return plt

def parse(text: str):
    print("Expr: "+text)
    l = [("a","2"),("b","3"),("c","a+b")]
    lookup = create_lookup(l)
    plot_grad_tree_from_expr(text,lookup)

parse(text)
