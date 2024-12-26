#!/bin/python3
from sys import argv


def differ(ang1,ang2):
    offset = 180 - ang1
    ang1 += offset
    ang2 += offset
    if ang2 < 0:
        ang2 += 360
    if ang1 < ang2 and abs(ang2 - ang1) < 180:
        return 'cw'
    else:
        return 'cc'


def differ_t(ang1,ang2,test):
    res = differ(ang1,ang2)
    if res == test:
        print(f"Test case for {ang1} {ang2} matched")
    else:
        print(f"Test case for {ang1} {ang2} did not match")
if __name__ == "__main__":

    differ_t(90,100,'cw')
    differ_t(90,80,'cc')
    differ_t(90,170,'cw')
    differ_t(90,190,'cw')
    differ_t(90,260,'cw')
    differ_t(90,280,'cc')
    differ_t(90,10,'cc')
    differ_t(90,350,'cc')
