import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt

words_name = "words_stream.txt"
count_name = "counts.txt"
hash_param = "hash_params.txt"

delta = math.e ** -5
epsilon = math.e * (10 ** -4)
prime = 123457
buckets = int(math.e / epsilon)
print "sys params:", delta, epsilon, prime, buckets

params = []
param_file = open(hash_param, "r")
for line in param_file:
    items = line.strip().split("\t")
    params.append((int(items[0]), int(items[1])))
param_file.close()
print "hash params", params

# hash functions
def my_hash(ab, prime, buckets, x):
    res = []
    length = len(ab)
    for i in xrange(length):
        y = x % prime
        v = (ab[i][0] * y + ab[i][1]) % prime
        r = v % buckets
        res.append(r)
    return res

# define the hash matrix
matrix = np.zeros((len(params), buckets))

# start to read words file
start1 = time.clock()
words_file = open(words_name, "r")
record_num = 0
for line in words_file:
    record_num += 1
    if record_num % (10 ** 6) == 0:
        print record_num, "records are processed ..."
    x = int(line.strip())
    hash_val = my_hash(params, prime, buckets, x)
    for i in xrange(len(params)):
        matrix[i][hash_val[i]] += 1
words_file.close()
end1 = time.clock()
print "total time for record:", (end1 - start1)
print record_num, "records"

error_record = []
freq_record = []
# calculate the error
start2 = time.clock()
count_file = open(count_name, "r")
count_num = 0
for line in count_file:
    count_num += 1
    if count_num % (10 ** 4) == 0:
        print count_num, "counts are processed ..."
    items = line.strip().split("\t")
    idx = int(items[0])
    fi = int(items[1])
    hash_val = my_hash(params, prime, buckets, idx)
    fi_tilde = sys.maxint
    for i in xrange(len(params)):
        fi_tilde = min(fi_tilde, matrix[i][hash_val[i]])
    error = (fi_tilde - fi) / (fi * 1.0)
    error_record.append(error)
    freq_record.append(fi / (1.0 * record_num))
count_file.close()
end2 = time.clock()
print "total time for count:", (end2 - start2)
print count_num, "words"

print "total", record_num, "records"
print "total", count_num, "words"

plt.loglog(freq_record, error_record, "+")
plt.title("Relative Error vs Word Frequency")
plt.xlabel("Word Frequency (log)")
plt.ylabel("Relative Error (log)")
plt.grid()
plt.savefig("q4result.png")
plt.show()
print "Well Done!"




