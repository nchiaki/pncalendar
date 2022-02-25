#!/usr/bin/env python3
#   coding: utf-8
'''
素数カレンダー: 0001/01/01からの日数をカウントし、それが素数となる時の年月日を表示する
'''

import math
import time as tm
import calendar as cal
import argparse

mondys = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
lpmondys = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

esc = '\x1b['
chrred = esc+'31m'
bckblk = esc+'40m'
endsgr = esc+'0m'

preyr = 0
premt = 0
mtday = 0

outopt = 'nrml'
primeterm = []
outyear = 0

def normalout(prm, yr, mt, dday):
    print(f'{prm}: {yr:04}/{mt:02}/{dday:02}')

def bannerout(prm, yr, mt, dday):
    global preyr, premt, mtday
    if (preyr != yr) or (premt != mt):
        if 0 < mtday:
            print(bckblk, end='', flush=True)
            while mtday <= 31:
                print(f'{mtday:02}', end='', flush=True)
                mtday += 1
            print(endsgr, end='', flush=True)

        mtday = 1
        print(f'\r\n{prm}: ', end='', flush=True)
        print(f'{yr:04}/{mt:02}/', end='', flush=True)

        print(bckblk, end='', flush=True)
        while mtday < dday:
            print(f'{mtday:02}', end='', flush=True)
            mtday += 1
        print(endsgr, end='', flush=True)

        prmday = chrred + f'{dday:02}' + endsgr
        print(prmday, end='', flush=True)
        mtday = dday + 1
        preyr = yr
        premt = mt
    else:
        print(bckblk, end='', flush=True)
        while mtday < dday:
            print(f'{mtday:02}', end='', flush=True)
            mtday += 1
        print(endsgr, end='', flush=True)

        prmday = chrred + f'{dday:02}' + endsgr
        print(prmday, end='', flush=True)
        mtday = dday + 1

def day2dal(day):
    dday = day
    yr = 1
    mt = 0
    while True:
        if cal.isleap(yr):
            if 366 < dday:
                dday -= 366
            else:
                for i, m in enumerate(lpmondys):
                    if m < dday:
                        dday -= m
                    else:
                        mt = i + 1
                        break
                break
        else:
            if 365 < dday:
                dday -= 365
            else:
                for i, m in enumerate(mondys):
                    if m < dday:
                        dday -= m
                    else:
                        mt = i + 1
                        break
                break
        yr += 1

    if (outyear == 0) or (outyear == yr):
        if outopt == 'bnnr':
            bannerout(day, yr, mt, dday)
        else:
            normalout(day, yr, mt, dday)
        day += 1
    elif (outyear != 0) and (outyear < yr):
        global mtday
        if 0 < mtday:
            print(bckblk, end='', flush=True)
            while mtday <= 31:
                print(f'{mtday:02}', end='', flush=True)
                mtday += 1
            print(endsgr, end='', flush=True)
        print()
        exit()
    else:
        prmpt = ('-', '\\', '|', '/')
        print(f'{prmpt[day%4]}\r', end='', flush=True)
        lstyr = outyear - yr
        if (1 < lstyr):
            day += lstyr * 31
        else:
            day += 1

    return day

def do_prime(cnt, vl):
    #upprvl = int(math.sqrt(vl))
    upprvl = vl
    #print(f'upprvl:{upprvl}')
    for dv in range(upprvl):
        if 1 < dv:
            if (vl % dv) == 0:
                vl += 1
                break
    else:
        #print(f'day2dal({vl})')
        vl = day2dal(vl)
        cnt += 1
        #tm.sleep(1)
    #vl += 1
    return cnt, vl

def main():
    global outopt, primeterm, outyear
    argp = argparse.ArgumentParser(description='素数カレンダー: 0001/01/01からの日数をカウントし、それが素数となる時の年月日を表示する')
    argp.add_argument('-of', '--outformat', choices=['nrml', 'bnnr'], default='nrml', help='表示方法選択')
    argp.add_argument('-prm', '--prime', metavar='<number>', type=int, nargs='*', help='素数範囲指定:開始値 [終了値]')
    argp.add_argument('-cnt', '--count', metavar='<number>', type=int, default=0, help='表示回数指定')
    argp.add_argument('-y', '--year', metavar='<year>', type=int, default=0, help='表示対象西暦')

    args = argp.parse_args()

    outopt = args.outformat
    if args.prime:
        primeterm = args.prime
    outmax = args.count
    outyear = args.year

    cnt = 0
    vl = 1
    vlend = 0
    if len(primeterm):
        vl = primeterm[0]
        if 2 <= len(primeterm):
            vlend = primeterm[1]
    if (vlend != 0):
        if (vlend < vl):
            print(f'The end value is less than the start value.')
            exit()

    #print(f'{outmax}:{vl} - {vlend}:{outyear}')
    if vlend == 0:
        while True:
            cnt, vl = do_prime(cnt, vl)
            if (0 < outmax) and (outmax <= cnt):
                break
    else:
        while vl <= vlend:
            cnt, vl = do_prime(cnt, vl)
            if (0 < outmax) and (outmax <= cnt):
                break

if __name__ == '__main__':
    main()
