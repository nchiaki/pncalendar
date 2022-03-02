#!/usr/bin/env python3
#   coding: utf-8
'''
素数カレンダー: 0001/01/01からの日数をカウントし、それが素数となる時の年月日を表示する
'''

import math
import time as tm
import calendar as cal
import argparse
import threading as thrd
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

maxnumofcal = 10000
outmax = 0
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
    print('{}: {:04}/{:02}/{:02}'.format(prm, yr, mt, dday))

def bannerout(prm, yr, mt, dday):
    global preyr, premt, mtday
    if (preyr != yr) or (premt != mt):
        if 0 < mtday:
            print(bckblk, end='', flush=True)
            while mtday <= 31:
                print('{:02}'.format(mtday), end='', flush=True)
                mtday += 1
            print(endsgr, end='', flush=True)

        mtday = 1
        print('\r\n{}: '.format(prm), end='', flush=True)
        print('{:04}/{:02}/'.format(yr,mt), end='', flush=True)

        print(bckblk, end='', flush=True)
        while mtday < dday:
            print('{:02}'.format(mtday), end='', flush=True)
            mtday += 1
        print(endsgr, end='', flush=True)

        prmday = chrred + '{:02}'.format(dday) + endsgr
        print(prmday, end='', flush=True)
        mtday = dday + 1
        preyr = yr
        premt = mt
    else:
        print(bckblk, end='', flush=True)
        while mtday < dday:
            print('{:02}'.format(mtday), end='', flush=True)
            mtday += 1
        print(endsgr, end='', flush=True)

        prmday = chrred + '{:02}'.format(dday) + endsgr
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
        elif outopt == 'nrml':
            normalout(day, yr, mt, dday)
        day += 1
    elif (outyear != 0) and (outyear < yr):
        global mtday
        if 0 < mtday:
            print(bckblk, end='', flush=True)
            while mtday <= 31:
                print('{:02}'.format(mtday), end='', flush=True)
                mtday += 1
            print(endsgr, end='', flush=True)
        print()
        exit()
    else:
        prmpt = ('-', '\\', '|', '/')
        print('{}\r'.format(prmpt[day%4]), end='', flush=True)
        lstyr = outyear - yr
        if (1 < lstyr):
            day += lstyr * 31
        else:
            day += 1

    return day

def do_prime(cnt, vl):
    #upprvl = int(math.sqrt(vl))
    upprvl = vl
    #print('upprvl:{upprvl}')
    for dv in range(upprvl):
        if 1 < dv:
            if (vl % dv) == 0:
                vl += 1
                break
    else:
        #print('day2dal({vl})')
        vl = day2dal(vl)
        cnt += 1
        #tm.sleep(1)
    #vl += 1
    return cnt, vl

def term_prime(strv, endv):
    cnt = 0
    vl = strv
    while vl <= endv:
        cnt, vl = do_prime(cnt, vl)
        if (0 < outmax) and (outmax <= cnt):
            break

def thrd_print(strv, endv, cnt):
    print('term_prime({strv}, {endv}) {cnt}')

def main():
    global outopt, primeterm, outyear
    argp = argparse.ArgumentParser(description='素数カレンダー: 0001/01/01からの日数をカウントし、それが素数となる時の年月日を表示する')
    argp.add_argument('-of', '--outformat', choices=['nrml', 'bnnr', 'none'], default='nrml', help='表示方法選択')
    argp.add_argument('-prm', '--prime', metavar='<number>', type=int, nargs='*', help='素数範囲指定:開始値 [終了値]')
    argp.add_argument('-cnt', '--count', metavar='<number>', type=int, default=0, help='表示回数指定')
    argp.add_argument('-y', '--year', metavar='<year>', type=int, default=0, help='表示対象西暦')
    #argp.add_argument('-mlt', '--multi', action='store_true', help='並列処理を有効にする')
    argp.add_argument('-mlt', '--multi', choices=['thrd','prcs','prcspl','none'], default='none', help='並列処理を有効にする')

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
            print('The end value is less than the start value.')
            exit()

    #print('{outmax}:{vl} - {vlend}:{outyear}')
    if vlend == 0:
        while True:
            cnt, vl = do_prime(cnt, vl)
            if (0 < outmax) and (outmax <= cnt):
                break
    else:
        if args.multi == 'none':
            term_prime(vl, vlend)
        else:
            numofcal = (vlend - vl) + 1
            if numofcal <= maxnumofcal:
                term_prime(vl, vlend)
            else:
                thrdtbl = []
                numofcalthrd = int(numofcal / maxnumofcal)
                fraction = int(numofcal % maxnumofcal)
                if args.multi == 'prcspl':
                    thrds = numofcalthrd
                    if 0 < fraction:
                        thrds += 1
                    exectr = ThreadPoolExecutor(max_workers=thrds)

                subend = (vl + maxnumofcal) - 1
                ttlcnt = 0
                for x in range(numofcalthrd):
                    nwcnt = subend - vl + 1
                    if args.multi == 'thrd':
                        thrdtbl.append(thrd.Thread(target=term_prime, args=[vl, subend]))
                        thrdtbl[-1].start()
                    elif args.multi == 'prcs':
                        thrdtbl.append(Process(target=term_prime, args=[vl, subend]))
                        thrdtbl[-1].start()
                    elif args.multi == 'prcspl':
                        thrdtbl.append(exectr.submit(term_prime, vl, subend))
                    else:
                        thrdtbl.append(thrd.Thread(target=thrd_print, args=[vl, subend, nwcnt]))
                        thrdtbl[-1].start()
                    ttlcnt += nwcnt
                    vl += maxnumofcal
                    subend += maxnumofcal
                if 0 < fraction:
                    nwcnt = vlend - vl + 1
                    if args.multi == 'thrd':
                        thrdtbl.append(thrd.Thread(target=term_prime, args=[vl, vlend]))
                        thrdtbl[-1].start()
                    elif args.multi == 'prcs':
                        thrdtbl.append(Process(target=term_prime, args=[vl, vlend]))
                        thrdtbl[-1].start()
                    elif args.multi == 'prcspl':
                        thrdtbl.append(exectr.submit(term_prime, vl, vlend))
                    else:
                        thrdtbl.append(thrd.Thread(target=thrd_print, args=[vl, vlend, nwcnt]))
                        thrdtbl[-1].start()
                    ttlcnt += nwcnt

                if args.multi == 'prcspl':
                    for t in thrdtbl:
                        t.result(timeout=None)
                    '''
                    runs = len(thrdtbl)
                    while 0 < runs:
                        runs = 0
                        for t in thrdtbl:
                            if t.running():
                                runs += 1
                        #tm.sleep(0.001)
                    '''
                    exectr.shutdown()
                else:
                    for t in thrdtbl:
                        t.join()

                print('Total:{}'.format(ttlcnt))
                pass

if __name__ == '__main__':
    main()
