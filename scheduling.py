#!/usr/bin/python

def build_schedule(data):
#    data = sorted(data, cmp=lambda x,y: y[0] - x[0] if 0 == x[2]-y[2] else y[2]-x[2])
    data = sorted(data, cmp=lambda x,y: 1 if y[3]-x[3] >= 0 else -1)

    sum = 0
    length = 0
    for job in data:
        length += job[1]
        sum += job[0]*length

    print "Sum: ",sum
def main():
    data=[]
    for line in open('jobs.txt').readlines()[1:]:
        l = line.split()
        data.append([int(l[0]), int(l[1]), int(l[0])-int(l[1]), float(l[0])/float(l[1])])

    build_schedule(data)

if __name__ == "__main__":
    main()
