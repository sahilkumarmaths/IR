import pickle
import math
import patricia

fob1 = open('index_file.txt','r')
index = pickle.load (fob1)
fob1.close()


import sys
print "Size of Index in Bytes:" + str(sys.getsizeof(index))

size1 = 0
size2 = 0

counter = 0
for ele in index:
    if "<patricia._NonTerminal" in (str(index[ele])): 
        continue
    size1  += sys.getsizeof(ele)
    size2 += sys.getsizeof(index[ele])
    counter += 1

print "Size of Dictionary in Bytes:" + str(size1)
print "Size of Posting list in Bytes:" + str(size2)


print "No of unique words:" + str(counter)  

min_len = -1
max_len = 0
avg = 0
for ele in index:
    if "<patricia._NonTerminal" in (str(index[ele])): 
        continue
    l = len(index[ele])
    if min_len == -l :
        min_len = l
    elif min_len > l:
        min_len = l
    if max_len < l :
        max_len = l
    avg += l

avg = float(avg)/float(counter)

sum_val = 0
for ele in index:
    if "<patricia._NonTerminal" in (str(index[ele])): 
        continue
    l = len(index[ele])
    sum_val += float(avg-float(l)) * float(avg - float(l))

sum_val = sum_val / float(counter)
standard_dev = math.sqrt(sum_val)

print " Min_len : " + str(min_len)
print " Max_len : " + str(max_len)
print " Avg_len : " + str(avg)
print "Standard dev : " + str(standard_dev)
    
