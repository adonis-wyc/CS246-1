"""
Created and last modified by Rao on Feb 5, 2017
This program is used for calculating HITS
"""

import numpy as np

myfile = "graph.txt"
f = open(myfile, 'r')
n = 100
iteration = 40

arcs = []
for l in f:
    items = l.strip().split("\t")
    arcs.append((items[0], items[1]))

L = np.zeros((n, n))
for kk in xrange(len(arcs)):
    i = int(arcs[kk][0]) - 1
    j = int(arcs[kk][1]) - 1
    L[i][j] = 1.0

h = np.ones((n, 1))
a = np.zeros((n, 1))

# a = np.dot(L.T, h_curr)
# print max(a)
# print a.shape
# print a.T
# x = a / max(a)
# print x.T


for it in xrange(iteration):
    a = np.dot(L.T, h)
    a = a / max(a)
    h = np.dot(L, a)
    h = h / max(h)

hh = h.reshape((n,))
aa = a.reshape((n,))

h_list = []
a_list = []
for xx in xrange(n):
    h_list.append((xx, hh[xx]))
    a_list.append((xx, aa[xx]))


def func(val):
    return val[1]

h_sort = sorted(h_list, key = func, reverse = True)
a_sort = sorted(a_list, key = func, reverse = True)

print "top 5 of h"
print h_sort[0:5]
print "last 5 of h"
print h_sort[-5:]
print "top 5 of a"
print a_sort[0:5]
print "last 5 of a"
print a_sort[-5:]

