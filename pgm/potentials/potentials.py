#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['unstack_potentials', 'marginalize', 'introduce_evidence', 'mult', 'div', 'align', 'multiply_potentials',
           'group_potentials', 'maxd']

import pandas as pd
from itertools import izip, product, combinations


def unstack_potentials(potentials):
    pots = []
    var = []
    for p in potentials:
        x = p
        if p.ndim != 1:
            for i in p.columns.names:
                x = x.stack(i)
        pots.append(x)
        var.append(set(x.index.names))
    return pots, var


def marginalize(var, table_list):
    """Variable must exist in table.
    var is a list of variables to be summed out. """
    tables, variables = unstack_potentials(table_list)
    result = []
    for t in tables:
        names = list(t.index.names)
        for v in var:
            if v in t.index.names:
                names.remove(v)
        if not len(names) == len(list(t.index.names)):
            #print var
            print t.groupby(level=names).sum().max()
            if (t.groupby(level=names).sum() == 1).all():
                result.append(1)
            else:
                result.append(t.groupby(level=names).sum())
        else:
            if (t == 1).all():
                result.append(1)
            else:
                result.append(t)
    return result


def introduce_evidence(table, evidence):
    tables, variables = unstack_potentials([table])
    t = tables[0]
    ev = []
    index = []

    for i in t.index.names:
        if evidence.has_key(i):
            index.append(i)
            ev.append(evidence.get(i))
    group = t.groupby(level=index)

    if len(ev) == 1:
        return group.get_group(*ev)
    else:
        return group.get_group(tuple(ev))


def mult(pot1, pot2):
    """Tables must be aligned."""
    if isinstance(pot1, int) or isinstance(pot2, int):
        return pot1 * pot2
    elif pot1.ndim == 1 or pot2.ndim == 1:
        return pot1 * pot2
    else:
        t1 = pd.concat([pot1] * pot2.shape[0], axis=0, keys=pot2.index.values, names=pot2.index.names)
        t2 = pd.concat([pot2] * pot1.shape[0], axis=0, keys=pot1.index.values, names=pot1.index.names)
        return t1.sort() * t2.reorder_levels(t1.index.names).sort()


def div(pot1, pot2):
    """Tables must be aligned."""
    if isinstance(pot1, int) or isinstance(pot2, int):
        return pot1 / pot2
    elif pot1.ndim == 1 or pot2.ndim == 1:
        return pot1 / pot2
    else:
        t1 = pd.concat([pot1] * pot2.shape[0], axis=0, keys=pot2.index.values, names=pot2.index.names)
        t2 = pd.concat([pot2] * pot1.shape[0], axis=0, keys=pot1.index.values, names=pot1.index.names)
        return t1.sort() / t2.reorder_levels(t1.index.names).sort()


def align(potentials, v, verbose=False):
    """Potentials must have variables in common, and be unstacked."""
    result = []
    for p in potentials:
        # print p
        # print
        if len(p.index.names) > len(v):
            # print 'DF'
            if len(v) == 1:
                result.append(p.unstack(level=v).sort(axis=1))
            else:
                result.append(p.unstack(level=v).sortlevel(axis=1))
        elif len(p.index.names) == len(v) and len(p.index.names) > 1:
            # print 'Values'
            result.append(p.reorder_levels(v).sort_index())
        else:
            # print 'S'
            result.append(p.sort_index())

    if verbose:
        print 'Verbose'
        for p in result:
            print p
            print

    return result


def multiply_potentials(potentials):
    n = 1
    pot = []
    for p in potentials:
        if isinstance(p, int):
            n = n * p
        else:
            pot.append(p)

    if n != 1:
        p = pot.pop()
        p = p * n
        pot.append(p)

    pots, var = unstack_potentials(pot)
    res = []
    # print var
    v = list(set.intersection(*var))

    while pots:
        # print pots
        if v:
            # print 'Easy!'
            aligned = align(pots, v)
            result = aligned.pop()
            for p in aligned:
                result = mult(result, p)
            return [result]
        else:
            # print 'Simplifying'
            pot1 = pots.pop()
            v1 = var.pop()
            common = [pot1]

            for x in var:
                if set.intersection(x, v1):
                    common.append(pots.pop(var.index(x)))
                    # print var.index(x)
                    var.remove(x)
            if len(common) == 1:
                res.extend(common)
                if len(pots) == 1:
                    res.extend(pots)
                    return res
            else:
                result = multiply_potentials(common)
                result_unstacked, result_var = unstack_potentials(result)
                pots.insert(0, *result_unstacked)
                var.insert(0, *result_var)
            v = list(set.intersection(*var))


def group_potentials(var, potentials):
    pots, pots_v = [], []
    for p in potentials:
        if isinstance(p, int):
            pots.append(p)
        else:
            pots_v.append(p)

    pots_v, v = unstack_potentials(pots_v)

    for p in pots_v:
        if var not in p.index.names:
            pots.append(p)
            pots_v.remove(p)

    return pots, pots_v


def maxd(var, util_list, prob_list):
    ''' Handles a single decision, with its corresponding
    utility potential and probability potential'''
    #print var, util_list
    util_result = []
    prob_result = []

    utils = util_list[:]
    probs = prob_list[:]

    for u in util_list:
        if isinstance(u, int):
            util_result.append(u)
            utils.remove(u)

    for p in prob_list:
        if isinstance(p, int):
            prob_result.append(p)
            probs.remove(p)

    utilities, util_var = unstack_potentials(utils)
    #print 'probs',probs
    if probs:
        probs, prob_var = unstack_potentials(probs)

        probabilities = []

        for p in probs:
            #print var, p.index.names
            #print var not in p.index.names
            if var not in p.index.names:
                prob_result.append(p)
            else:
                probabilities.append(p)
        #print '***'*3
        #print 'Prob\n',probabilities
        for u, p in izip(utilities, probabilities):
            #print u
            #print var
            names = list(u.index.names)
            maxed = []
            names.remove(var)

            if not len(names) == len(list(u.index.names)):
                groups = u.groupby(level=names)
                for n,g in groups:
                    maxed.append(g.argmax())
            else:
                print u

            util = u.loc[maxed].reset_index(level=var, drop=True)
            prob = p.loc[maxed].reset_index(level=var, drop=True)
            util_result.append(util)
            prob_result.append(prob)
    else:
        for u in utilities:
            names = list(u.index.names)
            maxed = []
            names.remove(var)

            if not len(names) == len(list(u.index.names)):
                groups = u.groupby(level=names)
                for n,g in groups:
                    maxed.append(g.argmax())
            else:
                print u

            util = u.loc[maxed].reset_index(level=var, drop=True)
            util_result.append(util)

    return util_result, prob_result