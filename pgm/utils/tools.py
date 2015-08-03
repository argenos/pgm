#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tools for dealing with nodes and drawing graphs.

Example:
    Examples.... bla bla bla::
        
        $ python example.py

Section break

"""

import matplotlib.pyplot as plt
import networkx as nx

__author__ = "Argentina Ortega Sainz"
__copyright__ = "Copyright 2015, Argentina Ortega Sainz"
__credits__ = ["Argentina Ortega Sainz"]
__date__ = "July 19, 2015"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Argentina Ortega Sainz"
__email__ = "argentina.ortega@smail.inf.h-brs.de"
__status__ = "Development"

__all__ = ['node_types', 'draw_graph']


def node_types(graph):
    chance = []
    decision = []
    utility = []
    cliques = []

    for n in graph:
        if graph.node[n]['type'] == 'chance':
            chance.append(n)
        elif graph.node[n]['type'] == 'decision':
            decision.append(n)
        elif graph.node[n]['type'] == 'utility':
            utility.append(n)
        elif graph.node[n]['type'] == 'clique':
            cliques.append(n)

    nodes = {'chance': chance, 'decision': decision, 'utility': utility, 'clique': cliques}

    return nodes

def edge_type(graph):
    informational = []
    functional = []
    conditional = []
    moral = []
    triangulated = []

    for e1, e2 in graph.edges_iter():
        t = graph.edge[e1][e2]['type']
        if t is 'informational':
            informational.append((e1,e2))
        elif t is 'functional':
            functional.append((e1,e2))
        elif t is 'conditional':
            conditional.append((e1,e2))
        elif t is 'moral':
            moral.append((e1,e2))
        elif t is 'triangulated':
            triangulated.append((e1,e2))

    edges = {'informational':informational, 'functional':functional,
             'conditional':conditional, 'moral':moral,
             'triangulated':triangulated}
    return edges




def node_type(n):
    return n['type']


def reverse_edge(graph, edge):
    # graph.remove_edge(edge[0], edge[1])
    graph.add_edge(edge[1], edge[0])


# TODO: [ ] Plot edges type
def draw_graph(graph, pos=None, size=600, alpha=0.9, show=False, save=False):
    if graph.name == '':
        title = 'graph'
    else:
        title = graph.name

    plt.figure()
    plt.axis('off')

    if pos is None:
        p = nx.graphviz_layout(graph, prog='dot')
    else:
        p = pos

    node_dict = node_types(graph)
    chance, decision, utility = node_dict.get('chance'), node_dict.get('decision'), node_dict.get('utility')
    # cliques = node_dict.get('clique')

    if 'type' in graph.graph:
        if graph.graph['type'] is 'moral':
            print 'moral'
            edges_dict = edge_type(graph)
            edges = []
            moral_links = edges_dict.get('moral')
            for e in graph.edges():
                if e not in moral_links:
                    edges.append(e)
            nx.draw_networkx_edges(graph, pos=p, edgelist=moral_links, edge_color='r', style='dashed')
            nx.draw_networkx_edges(graph, pos=p, edgelist=edges)
            nx.draw_networkx_labels(graph, pos=p)

        elif graph.graph['type'] is 'triangulated':
            print 'triangulated'
            edges = []
            edges_dict = edge_type(graph)
            triangulated_links = edges_dict.get('triangulated')
            for e in graph.edges():
                if e not in triangulated_links:
                    edges.append(e)
            nx.draw_networkx_edges(graph, pos=p, edgelist=triangulated_links, edge_color='b', style='dashed')
            nx.draw_networkx_edges(graph, pos=p, edgelist=edges)
            nx.draw_networkx_labels(graph, pos=p)
            # nx.draw_networkx_edges(graph, pos=p, edgelist=triangulated_links, edge_color='b', style='dashed')

        elif graph.graph['type'] is 'junction_tree':
            print 'junction_tree'
            edge_labels = []
            for u, v in graph.edges():
                edge_labels.append(((u, v),
                                    'in: u=%(u_in).2f p=%(p_in).2f\nout: u=%(u_out).2f p=%(p_out).2f\n%(separator)s'
                                    % graph.get_edge_data(u, v)))
            nx.draw_networkx(graph, pos=p, node_size=900, node_color='w')
            nx.draw_networkx_edge_labels(graph, pos=p, edge_labels=dict(edge_labels),
                                         bbox=dict(boxstyle='square', fc='w', ec='k'), rotate=False)

        elif graph.graph['type'] is 'join_tree':
            print 'join_tree'
            nx.draw_networkx(graph, pos=p, node_size=900, node_color='w')
            #nx.draw_networkx_edge_labels(graph, pos=p)
    else:
        print 'other'
        nx.draw_networkx_edges(graph, pos=p)
        nx.draw_networkx_labels(graph, pos=p, node_size=900)

    if len(chance) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=chance, node_size=size, node_shape='o', alpha=alpha, node_color='w')
    if len(decision) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=decision, node_size=size, node_shape='s', alpha=alpha, node_color='g')
    if len(utility) > 0:
        nx.draw_networkx_nodes(graph, p, nodelist=utility, node_size=size, node_shape='D', alpha=alpha, node_color='r')

    # Edges type: nx.draw_networkx_edges(G, pos, edgelist=edges, width=6, alpha=0.5, edge_color='b', style='dashed')

    triangulated_links = nx.get_edge_attributes(graph, 'triangulated')

    #if triangulated_links:
        #nx.draw_networkx_edges(graph, pos=p, edgelist=triangulated_links, edge_color='b', style='dashed')

    # nx.draw_networkx_edges(graph, pos=p)
    # nx.draw_networkx_labels(graph, pos=p)

    if save:
        nx.write_dot(graph, title + '.dot')
        plt.savefig(title + '.png')

    if show:
        plt.show()
