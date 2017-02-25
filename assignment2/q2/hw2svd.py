from scipy import linalg
import numpy as np
M = np.array(((1, 2), (2, 1), (3, 4), (4, 3)))
print M
print "=================="
U, s, Vh = linalg.svd(M, full_matrices=False);
print "U"
print U
print "s"
print s
print "Vh"
print Vh
print "=================="
O = np.dot(M.T, M)
Evals, Evecs = linalg.eigh(O)
print "Evals"
print Evals
print "Evecs"
print Evecs
list = []
for i in xrange(len(Evals)):
    list.append((Evals[i], (Evecs.T)[i]))
func = lambda x : x[0]
sortedList = sorted(list, key = func, reverse=True)
print "sorted Evals and corresponding Evecs"
print sortedList
print "=================="


