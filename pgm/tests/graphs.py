#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.networks.graph

Influence Diagram


"""

__author__ = "Argentina Ortega Sainz"
__copyright__ = "Copyright 2015, Argentina Ortega Sainz"
__credits__ = ["Argentina Ortega Sainz"]
__date__ = "July 15, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sainz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development"

import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node(1)
G.add_nodes_from([2,3])
#H=nx.path_graph(10)
#G.add_nodes_from(H) #Add the nodes from H to G
#G.add_node(H) #Add H as a node

#G.add_edge(1,2)
#e=(2,3)
#G.add_edge(*e)# unpack edge tuple*
#G.add_edges_from([(1,2),(1,3)])



#Example
N= nx.MultiDiGraph()
N.add_nodes_from(['A1','A2','A3','A4','A5','A6'])
N.add_edges_from([('A1','A2'),('A1','A3'),('A2','A4'),('A2','A5'),('A3','A5'),('A3','A6')])


ex = nx.MultiDiGraph()
ex.add_nodes_from(['a','b','c','d','e','f','g','h','i','j','k','l','d1','d2','d3','d4','v1','v2','v3','v4'])
ex.add_edges_from([('a','c'),('b','c'),('b','d'),('b','d1'),('d','f'),('c','e'),('d','e'),('e','g')])
ex.add_edges_from([('e', 'd2'), ('f', 'd2'), ('f', 'h'), ('h', 'j'), ('h', 'k'), ('k', 'v3'), ('j', 'v3')])
ex.add_edges_from([('d4','l'), ('l', 'v4'), ('i', 'l')])
ex.add_edges_from([('d1','d'), ('d1', 'v1'), ('d2', 'i'), ('d2', 'd3'), ('d3', 'd4'), ('d4', 'l')])


#nx.draw_graphviz(ex)
#nx.draw_networkx_edge_labels(ex,)
nx.draw_networkx(ex,with_labels=True)

ex2 = nx.MultiGraph(ex)
plt.figure()
nx.draw_networkx(ex2)

#print nx.is_chordal(ex2)
#print nx.chordal_graph_cliques(ex2)
print nx.find_cliques(ex2)

cli = nx.make_max_clique_graph(ex2)

plt.figure()
nx.draw_networkx(cli,with_labels=True)

