__author__ = 'Argen'
import numpy as np
import pandas as pd

iterables = [['bar', 'baz', 'foo', 'qux'], ['one', 'two']]
idx = pd.MultiIndex.from_product(iterables, names=['first', 'second'])
values = np.random.randn(8, 4)
t = pd.DataFrame(values, index=idx, columns=['A','B','C','D'])
print t

print t.loc['bar']

print t['A']

print t['A']['bar']

print t.loc['bar','one']

print t.loc[(slice(None),slice('one')),slice('A','C')]

print t.loc[(slice(None),slice('one')),slice('A','C')].sum(1) #0 rows, 1 columns

values = np.zeros((4, ))
s = pd.Series(values)
#print s