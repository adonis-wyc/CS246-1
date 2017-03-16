import time
import numpy as np
import os
import copy

# some helper functions
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# some common parameters
train_name = "features.txt"
target_name = "target.txt"
entries_len = file_len(train_name)
feature_len = 122
C = 100

# gradient descent
train_file = open(train_name, "r")
target_file = open(target_name, "r")

# the last element in each line of entries is the target
entries = []
for line in train_file:
    features = line.strip().split(",")
    entries.append(map(int, features))

for (idx, line) in enumerate(target_file):
    target = line.strip()
    entries[idx].append(int(target))

k = 0
w = np.zeros(feature_len) * 1.0
w_grad = np.zeros(feature_len) * 1.0
b = 0.0
b_grad = 0.0
fk = [C * entries_len]
eta = 0.0000003
epsilon = 0.25

start = time.clock()

while True:
    # calculate new w using old b, w
    # w_new = w
    # for ii in xrange(feature_len):
    #     second_sum = 0.0
    #     for entry in entries:
    #         x = entry[:-1]
    #         y = entry[-1]
    #         xw = sum(x * w)
    #         cond = y * (xw + b)
    #         if cond >= 1:
    #             pass
    #         else:
    #             second_sum -= y * x[ii]
    #     w_new[ii] = w[ii] - eta * (w[ii] + C * second_sum)

    second_sum = np.zeros(feature_len)
    for entry in entries:
        x = np.array(entry[:-1])
        y = np.array(entry[-1])
        xw = sum(x * w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            second_sum -= y * x
    w_new = w - eta * (w + C * second_sum)


    # calculate new b using old b, w
    b_sum = 0.0
    for entry in entries:
        x = entry[:-1]
        y = entry[-1]
        xw = sum(x * w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            b_sum -= y
    b_new = b - eta * C * b_sum

    # update w and b
    w = copy.deepcopy(w_new)
    b = copy.deepcopy(b_new)

    # calculate error
    fk_tmp = 0.5 * sum(w * w)
    second_item = 0.0
    for entry in entries:
        x = entry[:-1]
        y = entry[-1]
        xw = sum(x * w)
        cond = y * (xw + b)
        if cond >= 1:
            pass
        else:
            second_item += 1 - cond
    fk_tmp += C * second_item
    fk.append(fk_tmp)

    # calculate delta
    if 0 == k:
        pass
    else:
        delta = abs(fk[k - 1] - fk[k]) / fk[k - 1] * 100
        # show progress
        if k % 10 == 0:
            print k, "iteration:", fk_tmp, "delta:", delta
        if delta <= epsilon:
            break

    # increment # of iteration
    k += 1

end = time.clock()
elapsed = end - start
print elapsed

if os.path.isfile('batch.txt'):
    os.remove("batch.txt")
if os.path.isfile('batch.time.txt'):
    os.remove("batch.time.txt")

with open('batch.txt', 'a') as write_file:
    for idx, each in enumerate(fk):
        write_file.write(str(idx) + "," + str(each) + '\n')
with open('batch.time.txt', 'a') as write_file:
    write_file.write(str(elapsed))
