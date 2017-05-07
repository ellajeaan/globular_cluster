# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 14:14:44 2017

@author: EllaMeyer
"""

import numpy as np
import matplotlib.pyplot as plt

# importing my data and pulling out the necessary coloumns to make the CMD


data = np.loadtxt('ngc5024.csv', comments='#', delimiter=',')
x = data[:,1]
y = data[:,2]
v_mag = data[:,3]
v_mag_error = data[:,4]
vi_col = data[:,5]
vi_col_error = data[:,6]
i_mag = data[:,7]
i_mag_error = data[:,8]

# defining a function to plot the graphs, to minimize my need to have to write out 
# the same syntax repetitively
# inputs: coordinates, a title, and axes
# output: a graph of the given data with the necessary axes inversion to be a proper CMD
def plot(coordx, coordy, title, xax, yax):
    plt.scatter(coordx, coordy, color='k', marker='.')
    plt.title(title)
    plt.xlabel(xax)
    plt.gca().invert_yaxis()
    plt.ylabel(yax)
    plt.grid(b=True, which='both', color='k',linestyle='--')
    plt.show()


# this function is to plot over a narrowed range, so we can example the 
# more detailed parts of the CMD. Also allows for single point of control.
# input: coordinates, a title, axes, and min and max values for X and Y
# output: a graph of the given data narrowed over a particular range
def narrow_range_plot(coordx, coordy, title, xax, yax, xmin, xmax, ymin, ymax):
    plt.scatter(coordx, coordy, color='k', marker='.')
    plt.title(title)
    plt.xlabel(xax)
    plt.axis((xmin,xmax,ymin,ymax))
    plt.ylabel(yax)
    plt.gca().invert_yaxis()
    plt.grid(b=True, which='both', color='k',linestyle='--')
    plt.show()

plot(vi_col,v_mag,'CMD: V Magnitude vs V-I Colour Index of NGC 5024','V-I Colour Index','V Magnitude')
narrow_range_plot(vi_col,v_mag,'CMD: V Magnitude vs V-I Colour Index of NGC 5024','V-I Colour Index','V Magnitude', 0, 1.5, 12, 22)

# this is to change the e_bv into an intrinsic VI colour to be able to find the distance
e_bv = 0.02
e_vi = 1.1 * e_bv
intvi = vi_col - e_vi

plot(intvi,v_mag,'CMD: V Magnitude vs Adjusted V-I Colour Index of NGC 5024','V-I Colour Index','V Magnitude')
narrow_range_plot(intvi,v_mag,'CMD: V Magnitude vs V-I Colour Index of NGC 5024','V-I Colour Index','V Magnitude', -0.15, 1.5, 12, 23)

# finding the horizontal branch average magnitude
horizontal_x = v_mag[(0.4 < vi_col) & (vi_col < 1.0) & (17.5 > v_mag) & (15 < v_mag)]
avg_x_horiz = np.mean(horizontal_x)
print avg_x_horiz

# Finding Cluster Dist using Fe/H ratio and then using magnitudes
Fe_H = -2.1
MV = 0.31*Fe_H + 0.01*Fe_H**2 + 0.894
m = avg_x_horiz
Avvega = (e_vi*3.0)*0.9
d = (10**((m - MV-Avvega)/5.0))*10
print d


absolute_mag = v_mag - 5*np.log10(d/10) + Avvega
narrow_range_plot(intvi,absolute_mag,'Adjusted Colour-Magnitude for NGC 5024','V-I Colour Index','Absolute Visual Magnitude', 0.0, 1.5, -5, 7)

# loading in the data from the 3 isochrones
data1 = np.loadtxt('isochrome_age_12.csv', comments='#', delimiter=',')
data2 = np.loadtxt('isochrome_age_12.5.csv', comments='#', delimiter=',')
data3 = np.loadtxt('isochrone13.csv', comments='#', delimiter=',')

# extract necessary coloumns from each file
v_mag_iso1 = data1[:,8]
i_mag_iso1 = data1[:,11]
v_i1 = v_mag_iso1 - i_mag_iso1

v_mag_iso2 = data2[:,8]
i_mag_iso2 = data2[:,11]
v_i2 = v_mag_iso2 - i_mag_iso2

v_mag_iso3 = data3[:,8]
i_mag_iso3 = data3[:,11]
v_i3 = v_mag_iso3 - i_mag_iso3

# plot the absolute magnitude of the cluster against the intrinsic VI colour mag
# then overlay the line plots of the 3 isochrones
plt.xlim([0,1.5])
plt.ylim([-5, 7])
plt.scatter(intvi, absolute_mag)
plt.plot(v_i1, v_mag_iso1, color='red')
plt.plot(v_i2, v_mag_iso2, color='yellow')
plt.plot(v_i3, v_mag_iso3, color='orange')
plt.gca().invert_yaxis()
plt.title("Absolute Magnitude as a Function of Intrinsic VI and Isochrones Aged 12, 12.5, 13 Gyr")
plt.xlabel("Intrinsic VI")
plt.ylabel("Absolute Magnitude")
plt.show()

