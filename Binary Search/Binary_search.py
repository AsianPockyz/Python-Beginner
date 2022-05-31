# impementation of binary search algo
# as well as prove that a binary search algo is faster than a basic naive search that iterates through the entire array
import random
import time

def naive_search(l, target):
    for i in range(len(l)):
        if l[i] == target:
            return i
    return -1

# binary search uses divide and conquer
# leveraging the fact that the list is SORTED
def binary_search(l,target, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high=len(l)-1
    if high < low:
        return -1
    midpoint = (low+high) // 2
    if l[midpoint] == target:
        return midpoint
    elif target < l[midpoint]:
        return binary_search(l, target, low, midpoint-1)
    else:
        return binary_search(l, target, midpoint+1, high)
    
if __name__=='__main__':
    # simple test of functions
    # l = [1,3,5,10,12]
    # target = 10
    # print(naive_search(l,target))
    # print(binary_search(l,target))

    # initialize a sorted list of length 10,000
    length = 10000
    sorted_list = set()
    while len(sorted_list) < length:
        sorted_list.add(random.randint(-3*length,3*length))
    sorted_list = sorted(list(sorted_list))

    start = time.time()
    for target in sorted_list:
        naive_search(sorted_list, target)
    end = time.time()
    print("Basic naive search took: ", (end-start)/length, "seconds")

    start = time.time()
    for target in sorted_list:
        binary_search(sorted_list, target)
    end = time.time()
    print("Binary search took: ", (end-start)/length, "seconds")

    # the printed values then show the timing for how fast a basic naive search completes over 10,000 iterations; compared to the time for a binary search
