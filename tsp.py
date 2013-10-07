#!/usr/bin/pypy
import numpypy as np

def solve(data,size):
    max_size=2**(size-2)
    A1 = np.ones([max_size,size],float)
    A2 = np.ones([max_size,size],float)

def main():
    print "Starting solving TSP"
    file=open("data/tsp.txt")
    size = int(file.readline())
    cities=[]
    for line in file.readlines():
        (x,y) = [float(x) for x in line.split()]
        cities.append((x,y))


    print cities

    solve(cities,size)
if __name__ == '__main__':
    main()
