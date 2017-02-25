"""
Created and last modified by Rao on Feb 5, 2017
This program is used for calculating page rank
"""

import numpy as np

myfile = "graph.txt"
f = open(myfile, 'r')
n = 100
iteration = 40
beta = 0.8

arcs = []
for l in f:
    items = l.strip().split("\t")
    arcs.append((items[0], items[1]))

# for ii in xrange(len(arcs)):
#     print arcs[ii]

M = np.zeros((n, n))
# for jj in xrange(len(M)):
#     print M[jj]

for kk in xrange(len(arcs)):
    i = int(arcs[kk][0]) - 1
    j = int(arcs[kk][1]) - 1
    M[j][i] = 1.0

for ii in xrange(n):
    cnt = 0.0
    for jj in xrange(n):
        if M[jj][ii] > 0:
            cnt = cnt + 1.0
    for jj in xrange(n):
        M[jj][ii] = M[jj][ii] / cnt

# sum = 0.0
# for jj in xrange(100):
#     sum = sum + M[jj][2]
#     print M[jj][2]
# print sum

r_curr = np.ones((n, 1))
r_curr = r_curr / (1.0 * n)
r_next = np.zeros((n, 1))

# print r_curr.shape
# print r_curr

for it in xrange(iteration):
    r_next = np.dot(M, r_curr) * beta + (1 - beta) / (1.0 * n)
    r_curr = r_next

# print r_next.T
# print "====================="
# r = np.dot(M, r_curr) * beta + (1 - beta) / (1.0 * n)
# print r.T

# r_sort = sorted(r_next.reshape((n, )), reverse=True)
# print "top 5"
# print r_sort[0:5]
# print "last 5"
# print r_sort[-5:]

val = r_next.reshape((n, ))
# print val

id_val = []
for xx in xrange(n):
    id_val.append((xx, val[xx]))

func = lambda x : x[1]
# def func(x):
#     return x[1]

res = sorted(id_val, key = func, reverse=True)
print "top 5"
print res[0:5]
print "last 5"
print res[-5:]
