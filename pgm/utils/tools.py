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


def node_types(graph):
    chance = []
    decision = []
    utility = []

    for n in graph:
        if graph.node[n]['type'] == 'chance':
            chance.append(n)
        elif graph.node[n]['type'] == 'decision':
            decision.append(n)
        elif graph.node[n]['type'] == 'utility':
            utility.append(n)

    nodes = {'chance':chance, 'decision':decision, 'utility':utility}

    return nodes

def node_type(n):
    return n['type']

def reverse_edge(graph, edge):
    #graph.remove_edge(edge[0], edge[1])
    graph.add_edge(edge[1], edge[0])

def draw_graph(graph, pos=None, size=600, alpha=0.9, show=False, save=False):
    title = graph.graph['title']

    plt.figure()
    plt.axis('off')

    if pos==None:
        p = nx.graphviz_layout(graph, prog='dot')
    else:
        p=pos

    node_dict = node_types(graph)
    chance, decision, utility = node_dict.get('chance'), node_dict.get('decision'), node_dict.get('utility')

    if len(chance) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=chance, node_size=size, node_shape='o', alpha=alpha, node_color='w')
    if len(decision) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=decision, node_size=size, node_shape='s',alpha=alpha, node_color='g')
    if len(utility) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=utility, node_size=size, node_shape='D', alpha=alpha, node_color='r')

    nx.draw_networkx_edges(graph, pos=p)
    nx.draw_networkx_labels(graph, pos=p)

    if save:
        nx.write_dot(graph, title + '.dot')
        plt.savefig(title + '.png')

    if show:
        plt.show()