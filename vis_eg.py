import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

v = ['a',
 'b',
 'c',
 '@temp_0',
 '@temp_1',
 'd',
 '@temp_2',
 'e',
 '@temp_3',
 'f',
 'g',
 '@temp_4',
 '@temp_5',
 '@temp_6',
 '@temp_7',
 '@temp_8']

e = [('b', '@temp_0'),
 ('c', '@temp_0'),
 ('a', '@temp_1'),
 ('@temp_0', '@temp_1'),
 ('d', '@temp_2'),
 ('a', '@temp_2'),
 ('e', '@temp_3'),
 ('a', '@temp_3'),
 ('f', '@temp_4'),
 ('g', '@temp_4'),
 ('@temp_4', '@temp_5'),
 ('a', '@temp_5'),
 ('@temp_3', '@temp_6'),
 ('@temp_5', '@temp_6'),
 ('@temp_2', '@temp_7'),
 ('@temp_6', '@temp_7'),
 ('@temp_1', '@temp_8'),
 ('@temp_7', '@temp_8')]
 
colormap = ['r',
 'r',
 'r',
 'y',
 'b',
 'r',
 'b',
 'r',
 'b',
 'r',
 'r',
 'y',
 'b',
 'y',
 'y',
 'y']

e.reverse()
G = nx.DiGraph()

G.add_nodes_from(v)
G.add_edges_from(e)

plt.title('draw_networkx')
pos=nx.drawing.nx_agraph.graphviz_layout(G, prog='dot',args='-Nfontsize=10 -Nwidth="10" -Nheight="1" -Nmargin=0 -Gfontsize=8')
nx.draw(G, pos, with_labels=True, arrows=True,node_size=1000,node_color=colormap)
plt.show()

# fig = plt.figure()

# G = nx.Graph()
# G.add_edges_from(e)
# G.add_nodes_from(v)

# pos=nx.drawing.nx_agraph.graphviz_layout(G, prog='dot')
# edges = nx.draw_networkx_edges(G, pos, edge_color = 'w',with_labels=True)
# nodes = nx.draw_networkx_nodes(G, pos, node_color = 'g',with_labels=True)

# white = (1,1,1,1)
# black = (0,0,0,1)

# colors = [white for edge in edges.get_segments()]

# def update(n):
#     global colors

#     try:
#         idx = colors.index(white)
#         colors[idx] = black
#     except ValueError:
#         colors = [white for edge in edges.get_segments()]

#     edges.set_color(colors)
#     return edges, nodes

# anim = FuncAnimation(fig, update, interval=150, blit = True) 

# plt.show()