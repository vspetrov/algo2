#!/usr/bin/python
def calc_area(rects):
    r1 = rects[0]
    r2 = rects[1]
    r3 = rects[2]

    s1 = r1[0]*r1[1]
    s2 = 0
    if (r2[1] > r1[1]):
        s2 = s1 + (r2[1]-r1[1])*r2[0]
    else:
        s2 = s1

    s3 = 0

    if (r3[1] > r2[1]):
        s3 = s2 + (r3[1]-r2[1])*r3[0]
    else:
        s3 = s2

    return s3

def get_optimal_area(data):
    rects = []
    for i in range(3):
        r = sorted((data[i*2],data[i*2+1]),reverse=True)
        rects.append(r)
    rects = sorted(rects,key=lambda r: r[0],reverse = True)

    a1 = calc_area(rects)
    rects[2][0],rects[2][1] = rects[2][1],rects[2][0]
    rects = sorted(rects,key=lambda r: r[0],reverse = True)
    a2 = calc_area(rects)
    rects[2][0],rects[2][1] = rects[2][1],rects[2][0]
    rects[1][0],rects[1][1] = rects[1][1],rects[1][0]
    rects = sorted(rects,key=lambda r: r[0],reverse = True)
    a3 = calc_area(rects)
    rects[2][0],rects[2][1] = rects[2][1],rects[2][0]
    rects = sorted(rects,key=lambda r: r[0],reverse = True)
    a4 = calc_area(rects)
    area = [a1,a2,a3,a4]
    return min(area)

def main():
    file = open('test.txt')
    for line in file.readlines():
        data = [int(v) for v in line.split()]
        area = get_optimal_area(data)
        print line, ": ", area
    file.close()

if __name__ == '__main__':
    main()
