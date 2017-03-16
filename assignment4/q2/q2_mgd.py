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

np.random.shuffle(entries)

k = 0
l = 0
w = np.zeros(feature_len) * 1.0
w_grad = np.zeros(feature_len) * 1.0
b = 0.0
b_grad = 0.0
fk = [C * entries_len]
delta_list = [0]
eta = 0.00001
epsilon = 0.01
batch_size = 20

start = time.clock()

while True:

    mini_batch = copy.deepcopy(entries[l * batch_size : min(entries_len, (l + 1) * batch_size)])

    second_sum = np.zeros(feature_len)
    for entry in mini_batch:
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
    for entry in mini_batch:
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
    elif 1 == k:
        delta = abs(fk[k - 1] - fk[k]) / fk[k - 1] * 100
        delta_list.append(delta)
    else:
        delta = abs(fk[k - 1] - fk[k]) / fk[k - 1] * 100
        delta_curr = 0.5 * delta_list[k - 1] + 0.5 * delta
        delta_list.append(delta_curr)
        # show progress
        if k % 10 == 0:
            print "#", k, "error:", fk_tmp, "delta:", delta_curr
        if delta_curr <= epsilon:
            break

    # increment # of iteration
    k += 1
    l = (l + 1) % ((entries_len + batch_size - 1) / batch_size)

end = time.clock()
elapsed = end - start
print elapsed

if os.path.isfile('mini.txt'):
    os.remove("mini.txt")
if os.path.isfile('mini.time.txt'):
    os.remove("mini.time.txt")

with open('mini.txt', 'a') as write_file:
    for idx, each in enumerate(fk):
        write_file.write(str(idx) + "," + str(each) + '\n')
with open('mini.time.txt', 'a') as write_file:
    write_file.write(str(elapsed))