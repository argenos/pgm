#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm:tools

This module...


Example:
    Examples.... bla bla bla::
        
        $ python example.py

Section break

"""
__author__ = "Argentina Ortega Sainz"
__copyright__ = "Copyright 2015, Argentina Ortega Sainz"
__credits__ = ["Argentina Ortega Sainz"]
__date__ = "July 19, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sainz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development" 


import matplotlib.pyplot as plt
import networkx as nx
from pgm.nodes.chance import Chance
from pgm.nodes.decision import Decision
from pgm.nodes.utility import Utility


def node_types(nodes):
    chance = []
    decision = []
    utility = []
    # decision = [n for n in G if G.node[n]['node'] == 'decision']
    # chance = [n for n in G if G.node[n]['node'] == 'chance']
    # utility = [n for n in G if G.node[n]['node'] == 'utility']
    for n in nodes:
        if isinstance(n, Chance):
            chance.append(n)
        elif isinstance(n, Decision):
            decision.append(n)
        elif isinstance(n, Utility):
            utility.append(n)

    return chance, decision, utility


def draw(graph, title='graph.png', show=False):
    # 's' = square
    # 'D' = diamond
    # 'o' = circle

    plt.figure()

    chance, decision, utility = node_types(graph.nodes())
    pos = nx.graphviz_layout(graph, prog='dot')

    if len(chance) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=chance, node_size=800)
    if len(decision) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=decision, node_size=800, node_shape='s')
    if len(utility) > 0:
        nx.draw_networkx_nodes(graph, pos, nodelist=utility, node_size=800, node_shape='D')

    nx.draw_networkx_edges(graph, pos=pos)
    nx.draw_networkx_labels(graph, pos=pos)

    #nx.write_dot(graph, title + '.dot')
    #plt.savefig(title + '.png')

    if show:
        plt.show()
