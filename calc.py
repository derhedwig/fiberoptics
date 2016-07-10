#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

############
#  1.OTDR  #
############

pw50 = np.loadtxt("./messungen/OTDR_PW50.dat")
pw100 = np.loadtxt("./messungen/OTDR_PW100.dat")

# Search 'x' in the 0 column of 'data' and return the index i.e. position 
# in 'data'. If no exact match, return index of the first bigger value 
# encountered. (This is very unefficient... should use divide and conquer.)
def find_x(x, data):
    for idx in np.arange(len(data)):
        if (data[idx,0] >= x):
            break
    return idx

# Ok, with divide and conquer. 'a' should be an ordered array of ints.
def bsearch(x, a):
    def bsearch_loop(x, a, focus):
        idx = focus[int((focus[len(focus)-1] - focus[0])/2)]
        if len(focus) <= 1:
            return idx
        elif a[idx] == x:
            return idx
        elif a[idx] < x:
            return bsearch_loop(x, a, range(idx+1, focus[len(focus)-1]+1))
        elif a[idx] > x:
            return bsearch_loop(x, a, range(focus[0], idx))
        else:
            print('Shit happened.')
            return -1
    return bsearch_loop(x, a, range(0, len(a)))

###  Spleiß Verluste  ###

# array[start:end] returns the segment including start but not end.
seg1 = pw50[bsearch(68.6499, pw50[:,0]):bsearch(2040.2, pw50[:,0])+1].copy()
seg2 = pw50[bsearch(2102.74, pw50[:,0]):bsearch(4038.13, pw50[:,0])+1].copy()
seg3 = pw50[bsearch(4066, pw50[:,0]):bsearch(5939, pw50[:,0])+1].copy()
seg4 = pw50[bsearch(5995, pw50[:,0]):bsearch(8094, pw50[:,0])+1].copy()

def lin(x, a, b):
    return a + b*x

# a[:,n] returns the n-th column of a multidimensional array a.
# fit1 contains a tuple: [y-axis-intercept, slope]
fit1 = curve_fit(lin, seg1[:,0], seg1[:,1])[0]
fit2 = curve_fit(lin, seg2[:,0], seg2[:,1])[0]
fit3 = curve_fit(lin, seg3[:,0], seg3[:,1])[0]
fit4 = curve_fit(lin, seg4[:,0], seg4[:,1])[0]
print('Spleiss Verluste')
print('----------------\n')
print('fit1', fit1)
print('fit2', fit2)
print('fit3', fit3)
print('fit4', fit4)
print('1. splice pos. 1:', '2044.44,', lin(2044.44, *fit1))
print('1. splice pos. 2:', '2044.44,', lin(2044.44, *fit2))
print('2. splice pos. 1:', '4038,', lin(4038, *fit2))
print('2. splice pos. 2:', '4038,', lin(4038, *fit3))
print('plug pos. 1:', '5949,', lin(5949, *fit3))
print('plug pos. 2:', '5949,', lin(5949, *fit4))
print('Verlust 1. Spleiss =', 
        lin(2044.44, *fit1) - lin(2044.44, *fit2))
print('Verlust 2. Spleiss =', 
        lin(4038, *fit2) - lin(4038, *fit3))
print('Verlust 2. Spleiss =', 
        lin(5949, *fit3) - lin(5949, *fit4))

###  Todeszonen  ###

steck_x = 5949 
daemp1_x = 6025
daemp2_x = 6025
daemp1_y = lin(daemp1_x, fit4[0]+0.5, fit4[1])
daemp2_y = lin(daemp2_x, *fit4)
plt.plot(pw50[:,0], lin(pw50[:,0], fit4[0]+0.5, fit4[1]))
dead_x = 5994
dead_y = lin(dead_x, fit4[0]+0.5, fit4[1])
dead = dead_x - steck_x
print('\nTodeszone')
print('---------\n')
print('steck_x =', steck_x)
print('daemp1_y =', daemp1_y)
print('daemp2_y =', daemp2_y)
print('dead_x =', dead_x)
print('dead_y =', dead_y)
print('dead =', dead)

####################
#  2. KOMPONENTEN  #
####################

def findmax(a):
    i = 0
    idx = 0
    maximum = 0
    for j in range(0,len(a)):
        if a[j] >= a[i]:
            i = j
            maximum = a[j]
            idx = j
    return [maximum, idx]

def reverse(a):
    idx_forw = 0
    idx_back = len(a) - 1
    while idx_forw < idx_back:
        tmp = a[idx_forw]
        a[idx_forw] = a[idx_back]
        a[idx_back] = tmp
        idx_forw = idx_forw + 1
        idx_back = idx_back - 1
    return a 


fbg = np.loadtxt("./messungen/fbg-01.dat")
fbg_max = fbg[findmax(fbg[:,1])[1]]
print('\nBragg-Gitter')
print('------------\n')
print('fbg_max =', fbg_max)
plt.title(r'Plot')
plt.plot(pw50[:,0], pw50[:,1])
#plt.plot(pw100[:,0], pw100[:,1])
#plt.show()
