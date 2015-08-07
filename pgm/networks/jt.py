#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
pgm.networks.jt

Strong Join Tree for Influence Diagrams

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

import networkx as nx
from pgm.potentials.potentials import multiply_potentials

from pgm.utils.tools import node_types, draw_graph


class TriangulatedGraph(object):
    def __init__(self, ugraph, partial_order):
        """


        :type ugraph: DiGraph
        :type partial_order: Tuple
        """
        assert isinstance(ugraph, nx.Graph)
        # assert isinstance(window, list)

        self.ugraph = ugraph.copy()
        # print len(self.ugraph.edges())
        self.window, self.ordering = partial_order

        self.chance, self.decision, self.utility = node_types(self.ugraph)

        self.graph = nx.DiGraph(title='triangulated')
        self.graph.add_nodes_from(self.ugraph.nodes(data=True))
        # print self.graph.node
        # print len(self.graph.edges())
        # self.graph.add_nodes_from(self.ugraph.to_directed())
        # print self.ugraph.edges()

        for e in self.ugraph.edges_iter():
            if self.ordering.get(e[0]) > self.ordering.get(e[1]):
                # print e[0],'->',e[1]
                self.graph.add_edge(e[1], e[0])
            else:
                self.graph.add_edge(e[0], e[1])

        # print self.graph.edges()

        draw_graph(self.graph, True)

    # Get strong elimination order In, Dn, In-1, Dn-1...
    '''
    1. Eliminate simplicial node X; fa(x) is a clique candidate
    2. if fa(x) does not include all remaining nodes go to 1
    3. prune the set of clique candidates by removing sets that are subsets of other clique candidates

    '''


class JoinTree(object):
    def __init__(self):
        pass


class StronJunctionTree(object):
    def __init__(self):
        pass

#TODO Add corresponding graphs either as arguments or as imports from other class
def assign_potentials(junction_tree, verbose=False):
    cliques = []
    nodes = []
    potentials = []
    assigned = []
    remaining = net.nodes() #TODO add Original influence diagram
    # print remaining
    for j in junction_tree.nodes():
        assigned_nodes = []
        p = []
        u = []
        for n, d in net.nodes(data=True):
            if n in remaining:  # and not n in assigned:

                if d['type'] == 'chance':
                    dom = net.predecessors(n)
                    dom.append(n)
                    if set(dom) <= set(j):
                        assigned_nodes.append(n)
                        p.append(d['table'])
                        remaining.remove(n)
                elif d['type'] == 'utility':
                    dom = net.predecessors(n)
                    if set(dom) <= set(j):
                        assigned_nodes.append(n)
                        u.append(d['table'])
                        remaining.remove(n)
                elif d['type'] == 'decision':
                    dom = dcg.predecessors(n) #TODO add directed chordal graph
                    dom.append(n)
                    if set(dom) <= set(j):
                        assigned_nodes.append(n)
                        remaining.remove(n)

        u.extend(p)
        util_potential = multiply_potentials(u)
        prob_potential = multiply_potentials(p)
        cliques.append(j)
        nodes.append(assigned_nodes)
        potentials.append((prob_potential, util_potential))
        if verbose:
            print j
            print util_potential
            print
            print prob_potential
            print


            # print nodes
    potentials_dict = dict(zip(cliques, potentials))
    clique_dict = dict(zip(cliques, nodes))
    return clique_dict, potentials_dict

def collectR(junction_tree, rooted_tree, root):
    print '-----------'
    print root
    jt = junction_tree.copy()
    rt = rooted_tree.copy()
    #print junction_tree.in_edges(root, data=True)
    pot_dic = copy.deepcopy(potential_dict)
    path = list(nx.dfs_postorder_nodes(rooted_tree))
    print
    #path = list(nx.dfs_postorder_nodes(junction_tree, root))
    #path.reverse()
    print path
    #u = path.pop()
    while path:
        u = path.pop()
        #Projecting current cluster to variables in separator
        print '--------'
        v = tuple(*rooted_tree.successors(u)) #each clique only has one child

        prob_pot_u, util_pot_u = pot_dic.get(u)

        if u is not root and rooted_tree.has_edge(u,v):
            print u, v
            for p in rooted_tree.predecessors(u):
                print 'Getting potentials from separators'
                su = jt.edge[p][u]['u_pot']
                sp = jt.edge[p][u]['p_pot']

                if not isinstance(sp, int):
                    prob_pot_u.extend(sp)
                else:
                    prob_pot_u.append(sp)

                if not isinstance(su, int):
                    util_pot_u.extend(su)
                else:
                    util_pot_u.append(su)

            prob_pot_u = multiply_potentials(prob_pot_u)
            util_pot_u = multiply_potentials(util_pot_u)

            d = jt.get_edge_data(u, v)
            sum_out = list(set(u) - set(d['separator']))
            sum_out.sort(key=order.get, reverse=True)
            for ns in sum_out:
                if net.node[ns]['type'] == 'chance':
                    print 'Marginalize ', ns
                    prob_pot_u = marginalize(ns, prob_pot_u)
                    util_pot_u = marginalize(ns, util_pot_u)
                    #print util_pot_u
                    #print
                    #print prob_pot_u
                    #print
                elif net.node[ns]['type'] == 'decision':
                    print 'Marginalize ', ns
                    group_potentials(ns, util_pot_u)
                    util_pot_u, prob_pot_u = maxd(ns, util_pot_u, prob_pot_u)
                    #print util_pot_u
                    #print
                    #print prob_pot_u
                    #print
                elif net.node[ns]['type'] == 'utility':
                    print 'Marginalize ', ns
            jt[u][v]['u_pot']= util_pot_u
            jt[u][v]['p_pot']= prob_pot_u
        else:
            print u


        #u = v
    #print '****'
    #print pot_dic.get(('E', 'B', 'D', 'F', 'D1'))
    return jt

def distributeR(junction_tree, rooted_tree, root):
    print '-----------'
    print root
    jt = junction_tree.copy()
    #rt = rooted_tree.copy()
    rt = rooted_tree.reverse(copy=True)
    pot_dic = copy.deepcopy(potential_dict)
    path = list(nx.dfs_postorder_nodes(rt, root))#.reverse()
    #path.reverse()
    print path

    root_separators = {}
    while path:
        u = path.pop()
        #Projecting current cluster to variables in separator
        print '-'*60
        print u
        prob_pot_u, util_pot_u = pot_dic.get(u)

        v = tuple(*rt.predecessors(u))

        if u is root:
            for v1, u1, d1 in jt.in_edges(u, data=True):
                print v1
                prob = prob_pot_u[:]
                util = util_pot_u[:]
                for v2, u2, d2 in jt.in_edges(u, data=True):
                    if not v1 == v2:
                        prob.extend(d2['p_pot'])
                        util.extend(d2['u_pot'])

                prob = multiply_potentials(prob)
                util = multiply_potentials(util)
                #print util
                #print prob

                sum_out = list(set(u) - set(d1['separator']))
                sum_out.sort(key=order.get, reverse=True)
                for ns in sum_out:
                    if net.node[ns]['type'] == 'chance':
                        print 'Marginalize ', ns
                        prob = marginalize([ns], prob)
                        util = marginalize([ns], util)
                        #print util
                        #print
                        #print prob
                        #print
                    elif net.node[ns]['type'] == 'decision':
                        print 'Marginalize ', ns
                        ut, u_ns = group_potentials(ns, util)
                        pt, p_ns = group_potentials(ns, prob)

                        util, prob = maxd(ns, u_ns, p_ns)
                        util.extend(ut)
                        prob.extend(pt)
                        #print util
                        #print
                        #print prob
                        #print
                    elif net.node[ns]['type'] == 'utility':
                        print 'Marginalize ', ns
                #print util
                #print prob
                jt[root][v1]['u_pot']= util
                jt[root][v1]['p_pot']= prob
        else:
            #v = tuple(*rooted_tree.successors(u)) #each clique only has one child
            if rt.successors(u):
                for p in rt.predecessors(u):
                    print 'Getting potentials from separators'
                    su = jt.edge[p][u]['u_pot']
                    sp = jt.edge[p][u]['p_pot']

                    if not isinstance(sp, int):
                        prob_pot_u.extend(sp)
                    else:
                        prob_pot_u.append(sp)

                    if not isinstance(su, int):
                        util_pot_u.extend(su)
                    else:
                        util_pot_u.append(su)

                prob_pot_u = multiply_potentials(prob_pot_u)
                util_pot_u = multiply_potentials(util_pot_u)

                for v in rt.successors(u):
                    prob = prob_pot_u[:]
                    util = util_pot_u[:]

                    d = jt.get_edge_data(u, v)
                    sum_out = list(set(u) - set(d['separator']))
                    sum_out.sort(key=order.get, reverse=True)
                    for ns in sum_out:
                        if net.node[ns]['type'] == 'chance':
                            print 'Marginalize ', ns
                            prob = marginalize([ns], prob)
                            util = marginalize([ns], util)
                            #print util_pot_u
                            #print
                            #print prob_pot_u
                            #print
                        elif net.node[ns]['type'] == 'decision':
                            print 'Marginalize ', ns
                            ut, u_ns = group_potentials(ns, util)
                            pt, p_ns = group_potentials(ns, prob)

                            util, prob = maxd(ns, u_ns, p_ns)
                            util.extend(ut)
                            prob.extend(pt)
                            #print util_pot_u
                            #print
                            #print prob_pot_u
                            #print
                        elif net.node[ns]['type'] == 'utility':
                            print 'Marginalize ', ns
                    jt[u][v]['u_pot']= util
                    jt[u][v]['p_pot']= prob
    return jt

def query(var, junction_tree):
    pot_dic = copy.deepcopy(potential_dict)
    jt = junction_tree.copy()
    #print clique_dict
    cliques = []
    print
    for c, d in clique_dict.items():
        if var in d:
            cliques.append(c)
            break

    clique = cliques.pop()
    in_edges = jt.in_edges(clique, data=True)
    print clique
    prob, util = pot_dic.get(clique)
    #print list(jt.in_edges(clique))
    for u, v, d in jt.in_edges(clique, data=True):
        #print u
        prob.extend(d['p_pot'])
        util.extend(d['u_pot'])

    prob = multiply_potentials(prob)
    util = multiply_potentials(util)

    sum_out = list(clique)
    sum_out.remove(var)
    sum_out.sort(key=order.get, reverse=True)
    for ns in sum_out:
        if net.node[ns]['type'] == 'chance':
            print 'Marginalize ', ns
            print prob
            print
            print util
            print
            prob = marginalize([ns], prob)
            util = marginalize([ns], util)
            print prob
            print
            print util
            print
        elif net.node[ns]['type'] == 'decision':
            print 'Marginalize ', ns
            print prob
            print
            print util
            print

            ut, u_ns = group_potentials(ns, util)
            pt, p_ns = group_potentials(ns, prob)

            util, prob = maxd(ns, u_ns, p_ns)
            util.extend(ut)
            prob.extend(pt)

        elif net.node[ns]['type'] == 'utility':
            print 'Marginalize ', ns

    print prob
    print util


