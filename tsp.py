#!/usr/bin/pypy
import numpypy as np
import sys
import itertools as it


def get_value(s):
    v = np.int32(0)
    for i in s:
        if i == 0: continue
        v = v | 1 << (i-1)
    return v

def get_value_without_v(s,skip):
    v = np.int32(0)
    for i in s:
        if i ==0 or i == skip:continue
        v = v | 1 << (i-1)
    return v

def get_dist(data,i,j):
    return np.sqrt((data[i][0]-data[j][0])*(data[i][0]-data[j][0])+
(data[i][1]-data[j][1])*(data[i][1]-data[j][1]))

def solve(data,size):
    max_size=2**size
    A = np.ones([max_size,size],float)*sys.float_info.max
    A[0,0] = 0
    for m in range(2,size+1):
        subsets = it.combinations(range(1,size),m-1)

        for s in subsets:
            s = (0,)+s
            v = get_value(s)
            for j in s:
                if 0 == j: continue
                vmin = sys.float_info.max
                v_tmp = get_value_without_v(s,j)
                for k in s:
                    if k == j: continue

                    v_cand = A[v_tmp,k] + get_dist(data,k,j)
                    if v_cand < vmin:
                        vmin = v_cand
                A[v,j] = vmin

    rst = sys.float_info.max
    v = get_value(range(size))
    for j in range(size):
        v_cand = A[v,j] + get_dist(data,j,0)
        if v_cand < rst:
            rst = v_cand

    return rst

def main():
    print "Starting solving TSP"
    file=open("data/tsp.txt")
    size = int(file.readline())
    cities=[]
    for line in file.readlines():
        (x,y) = [float(x) for x in line.split()]
        cities.append((x,y))


    print cities

    print "TSP path length:",solve(cities,size)
if __name__ == '__main__':
    main()
