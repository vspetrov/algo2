#!/usr/bin/pypy
import numpypy as np

def solveKnapsack(items,knapsack_size,number_of_items):
    A = np.zeros((number_of_items+1,knapsack_size+1), dtype='int32')
    for i in range(1,number_of_items+1):
        for j in range(knapsack_size+1):
            v1=A[i-1][j]
            v2=0
            if j-items[i-1][1] > 0:
                v2 = A[i-1,j-items[i-1][1]]+items[i-1][0]
            A[i][j] = max(v1,v2)

    return A[number_of_items][knapsack_size]

def main():
    f = open('data/knapsack1.txt')
    (knapsack_size, number_of_items) = [int(x) for x in f.readline().split()]
    print 'knapsack_size: ',knapsack_size
    print 'number_of_items: ',number_of_items

    items=[]
    for line in f.readlines():
        (value, size) = [int(x) for x in line.split()]
        items.append((value,size))

    assert(len(items) == number_of_items)

    solution = solveKnapsack(items,knapsack_size,number_of_items)
    print 'Optimal solution:',solution
if __name__ == '__main__':
    main()
