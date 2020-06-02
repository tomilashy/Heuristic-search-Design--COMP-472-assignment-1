'''
Created on May 11, 2020
https://pythonhosted.org/Python%20Shapefile%20Library/
@author: Jesutomi
----------------------------------------------------------
Assignment 1
written by Olasubulumi Ogo-Oluwa Jesutomi 
For COMP 472 Section AH?- Summer 2020
------------------------------------------------------------
'''

import shapefile
import matplotlib.pyplot as plt
import numpy as np
import time
# sf = shapefile.Reader("shape/crime_dt.shp")
sf = shapefile.Reader("stm_sig/stm_lignes_sig.shp")
shapes = sf.shapes()
# print(len(shapes))
print(dir(shapes[3]))
# print(shapes[3].shapeType)
# first feature of the shapefile
feature = shapes[0]
first = feature.__geo_interface__['coordinates']  
print (first)  # (GeoJSON format)

data = np.array([ x.points[0] for x in shapes])  # getting x,y coordinates in a list
# xdata= np.array([ x.points[0][0] for x in shapes])
# print(len(xdata))
# ydata= np.array([ x.points[0][1] for x in shapes])
# print(len(ydata))
# for shape in shapes:
#     print(shape.__geo_interface__['coordinates'],shape.points)
#     pass
#     
# print(np.where(data==0))
# print(data)

x, y = data.T
# using histogram2d allows you to plot a 2d array based on their positions. bin is how you set the area of your graph 
H, xedges, yedges = np.histogram2d(x, y, bins=(np.arange(min(x), max(x) + 0.002, 0.002), np.arange(min(y), max(y) + 0.002, 0.002)))
H = H.T  # Let each row list bins with common y range.
# scaled down array to range from 0-10
# H = np.array([[((100 - 0) * (a - np.min(H))) / (np.max(H) - np.min(H)) for a in b ] for b in H ])
print(H.shape)#count per grid
checking=np.array([[[x,y] for x in xedges] for y in yedges])
print(np.array([[[x,y] for x in xedges] for y in yedges]).shape)#grid coordinates
print(np.sum(H))#sum of all digits in array
print(np.max(H), np.min(H), np.median(H), np.mean(H))
figcount = 1
'''
Take user location and destination, find optimal path based on percentage and get distance also
'''
threshold = int(input("Enter the threshold value(1-100): ")) 
start_time = time.time()
 

if threshold ==50:
    temp = np.where(H >= np.median(H), np.max(H),np.min(H))
elif threshold !=0:
    temp = np.where(H >= np.percentile(H, threshold), np.max(H),np.min(H))
else:
    temp = H
    temp = np.where(H > np.percentile(H, threshold), 1,0)
#     temp[temp np.percentile(H, i)] = 0
         
val = sorted(list(dict.fromkeys([a for b in temp for a in b])), reverse=True)
#     H[H <  np.percentile(val, 75)] = 0
# H[H <  50] = 0
plt.figure(figcount)
figcount += 1
plt.imshow(temp, interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
# print(temp)
print(np.max(val), np.min(val), np.median(val), np.mean(val))
axes = plt.axes()
axes.set_yticks(np.arange(min(y), max(y) + 0.002, 0.002))
axes.set_xticks(np.arange(min(x), max(x) + 0.002, 0.002))
plt.grid( linewidth=2)
plt.setp(axes.get_xticklabels(), rotation=90)
plt.suptitle(f'This is {threshold} percent threshold', fontsize=16)
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.colorbar().ax.set_ylabel('Counts')
    
# plt.show()
f2 = plt.figure(figcount)
f2.suptitle('This is a somewhat long figure title', fontsize=16)
plt.scatter(x, y)
axes = plt.axes()
axes.set_yticks(np.arange(min(y), max(y) + 0.002, 0.002))
axes.set_xticks(np.arange(min(x), max(x) + 0.002, 0.002))
plt.setp(axes.get_xticklabels(), rotation=90) 
plt.grid()
print("--- %s seconds ---" % (time.time() - start_time))
plt.show()
