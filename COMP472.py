'''
Created on May 11, 2020
@author: Jesutomi
----------------------------------------------------------
Assignment 1
written by Olasubulumi Ogo-Oluwa Jesutomi ID:40055693
For COMP 472 Section AH?- Summer 2020
------------------------------------------------------------
'''
import matplotlib.patches as mpatches
import shapefile
import matplotlib.pyplot as plt
import numpy as np
import time
import math

class grid_box(object):
    '''
    Each grid box contain 4 coordinates, 6 lines and box value after set threshold
    '''
    def __init__(self, p1,p2,p3,p4,value):
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.p4=p4
        self.value=value
        self.lines=[]
        self.__setlines__()
        
    def __checkdiagonal__(self,a,b): 
        if format(abs(a[0] -b[0]), '.1g') == format(abs(a[1] -b[1]), '.1g'):
            return True
        else:
            return False
    def __setlines__(self):
        if self.value==0:
            for i in self.get_all_coordinates():
                for j in self.get_all_coordinates():
                    if not np.array_equal(i, j):
                        if self.__checkdiagonal__(i,j):
                            self.lines.append(line(i,j, 1.5))
                        else:
                            self.lines.append(line(i,j, 1))
        else :
            self.lines.append(line(self.p1, self.p2, 1000))
            self.lines.append(line(self.p2, self.p3, 1000))
            self.lines.append(line(self.p3, self.p4, 1000))
            self.lines.append(line(self.p4, self.p1, 1000))
            self.lines.append(line(self.p3, self.p1, 1000))
            self.lines.append(line(self.p2, self.p4, 1000))

    def get_all_lines(self):
        return self.lines
    def get_all_coordinates(self):
        return [self.p1,self.p2,self.p3,self.p4]
    
    
    
class line(object):
    '''
    Each line contain 2 coordinates,weight of the line and bool to see if the line is passable
    '''
    def __init__(self, p1,p2,weight=None):
        self.p1=p1
        self.p2=p2
        self.weight=weight
        self.passable=self.__isPassable__()
    def is_boundaryline(self,a):
        if bool(set(a).intersection(set(self.p1))) and bool(set(a).intersection(set(self.p2))):
            return True
        else:
            return False
        
    def is_diagonal(self): 
        if format(abs(self.p1[0] -self.p2[0]), '.1g') == format(abs(self.p1[1] -self.p2[1]), '.1g'):
            return True
        else:
            return False
    def get_coordinate(self):
        return [self.p1,self.p2]
    
    def get_invcoordinate(self):
        return [self.p2,self.p1]
    
    def checkpoint(self,point):
        if format(abs(point[0] -self.p1[0]), '.3f') == format(0, '.3f')and format(abs(point[1] -self.p1[1]), '.3f')  == format(0, '.3f') :
#             print(format(point[0] -self.p1[0], '.3f'),format(point[1] -self.p1[1], '.3f'))
            return True
        elif format(abs(point[0] -self.p2[0]), '.3f')  == format(0, '.3f') and format(abs(point[1] -self.p2[1]), '.3f')== format(0, '.3f') :
            return True
        else:
            return False
    def neighbour(self,point):
        if tuple(self.p1)==point:
            return tuple(self.p2 )
        elif tuple(self.p2)==point:
            return tuple(self.p1 )
        
    def __isPassable__(self):
        if self.weight == 1000:
            return False
        elif self.weight == 1.3:
            return True
        elif self.weight == 1.5:
            return True  
        elif self.weight == 1:
            return True 
        else:
            return False


    def set_Weight(self,weight):
        self.weight=weight
        self.passable=self.__isPassable__()
        
def lowest_node(nodes,points,lines):
    nodes=list(nodes) 
    smallest_node = {'node':nodes[0],'weight':20000}
    for line in points[smallest_node['node']]:
        if lines[line].passable:
            if lines[line].weight< smallest_node['weight']:
                smallest_node['weight']=lines[line].weight
                  
    for node in nodes:
        for line in points[node]:
            if lines[line].passable:
                if lines[line].weight< smallest_node['weight']:
                    smallest_node['node']=node
                    smallest_node['weight']=lines[line].weight
  
    return smallest_node['node']
def construct_path(current,g_values):
    #             find the path
    path={current}
    draw=[]
    temp=current 
     
    while g_values[temp]['previous']:
        new_line=tuple([temp,g_values[temp]['previous']])
        invnew_line=tuple([g_values[temp]['previous'],temp])
        if  new_line in lines.keys(): 
            lines[ new_line].set_Weight(0)
        elif invnew_line in lines.keys():
            lines[invnew_line].set_Weight(0)
        path.add(temp)
        draw.append(new_line)
        temp = g_values[temp]['previous']
#     print(path)
#             for line in path:
#             for line in draw:
#                 print(line)
#                 line_x = np.linspace(line[0][0], line[1][0])
#                 line_y = np.linspace(line[0][1], line[1][1])
#                 plt.plot(line_x, line_y, color=[0, 1, 0])   
    return ('Path found')                

def heuristics(start_point,end_point,lines,points):
    g_values={tuple(start_point ): {'weight':0,'previous':None,'fvalue':0}}
    open_set={tuple(start_point )}
    closed_set=[]
#     h_value = lambda a , b: math.sqrt(((a[0]+b[0])**2)+ ((a[1]+b[1])**2)) 
    h_value = lambda a , b: abs(a[0]-b[0])+ abs(a[1]-b[1])
    while len(open_set) >0:
#         This operation can occur in O(1) time if openSet is a min-heap or a priority queue
        current = lowest_node(open_set,points,lines)
        if current == tuple(end_point ):
            return construct_path(current,g_values)
  
        open_set.remove(current) 
        closed_set.append(current)
        for line_key in points[current]:
            if lines[line_key].passable:
                if lines[line_key].neighbour(current) in closed_set:
                    continue
                else:
                    tempH= lines[line_key].weight #+ g_values[current]['weight'] 
                    if lines[line_key].neighbour(current) in open_set: #if its already in open set, checking if f(n) is better
                        if g_values[lines[line_key].neighbour(current)]['weight']>=tempH: #g_values[lines[line_key].neighbour(current)]['fvalue']>=h_value(lines[line_key].neighbour(current),end_point)+tempH:
                            g_values[lines[line_key].neighbour(current)]['weight']=tempH
                            g_values[lines[line_key].neighbour(current)]['previous']=current
    #                         print('better')
                    else:
                        open_set.add(lines[line_key].neighbour(current))
    #                     print(tempH)
                        g_values[lines[line_key].neighbour(current)]={'weight': tempH ,'previous':current}
                      
                      
    #             f(n):= g(n) + h(n)
    #                 print(g_values[lines[line_key].neighbour(current)])
                    g_values[lines[line_key].neighbour(current)]['fvalue']= h_value(lines[line_key].neighbour(current),end_point)+g_values[lines[line_key].neighbour(current)]['weight']
                  
  
  
  
    # Open set is empty but goal was never reached
    return 'failed to get a path'
     
if __name__ == '__main__':
    sf = shapefile.Reader("shape/crime_dt.shp")
    shapes = sf.shapes()
    
    data = np.array([ x.points[0] for x in shapes])  # getting x,y coordinates in a list
    x, y = data.T
    #setting axis
    axes = plt.axes()
    axes.set_yticks(np.arange(min(y), max(y) + 0.002, 0.002))
    axes.set_xticks(np.arange(min(x), max(x) + 0.002, 0.002))
    # using histogram2d allows you to plot a 2d array based on their positions. bin is how you set the area of your graph 
    H, xedges, yedges = np.histogram2d(x, y, bins=(np.arange(min(x), max(x) + 0.002, 0.002), np.arange(min(y), max(y) + 0.002, 0.002)))
    H = H.T  # Let each row list bins with common y range.
    
    print(H.shape)#count per grid
    grid_coordinate=np.array([[[x,y] for x in xedges] for y in yedges])
#     print(grid_coordinate.shape)
#     print(np.array([[[x,y] for x in xedges] for y in yedges]))#grid coordinates
    
    #input desired crime threshold
    threshold = int(input("Enter the threshold value(1-100): ")) 
     
    
    if threshold ==50:
        temp = np.where(H >= np.median(H), np.max(H),np.min(H))
    elif threshold !=0:
        temp = np.where(H >= np.percentile(H, threshold), np.max(H),np.min(H))
    elif threshold ==0:
        temp = H
        temp = np.where(H > np.percentile(H, threshold), 1,0)
    #     temp[temp np.percentile(H, i)] = 0
    plt.imshow(temp,interpolation='nearest', origin='low', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])         
             
    gridboxes=[]
    for x in range(len(xedges)-1):
        temparr=[]
        for y in range(len(yedges)-1): 
            temparr.append(grid_box(grid_coordinate[x][y],grid_coordinate[x+1][y],grid_coordinate[x][y+1],grid_coordinate[x+1][y+1],temp[x][y]))
        gridboxes.append(temparr)
    
    '''
    getting all lines on the graph
    '''     
    lines={} 
    for i in range(len(gridboxes)):
        for j in range(len(gridboxes[i])):
            for line in gridboxes[i][j].get_all_lines():
                if tuple(map(tuple, line.get_coordinate())) in lines.keys():
                    if not line.is_diagonal():
                        if  line.is_boundaryline([np.max(xedges),np.min(xedges),np.max(yedges),np.min(yedges)]):
                            line.set_Weight(1000)
#                     print('already exist')
                    if line.weight!=lines.get(tuple(map(tuple, line.get_coordinate()))).weight and lines[tuple(map(tuple, line.get_coordinate()))].weight!=1.3:
#                         print(line.weight,lines.get(tuple(map(tuple, line.get_coordinate()))).weight)
                        lines[tuple(map(tuple, line.get_coordinate()))].set_Weight(1.3)
                elif tuple(map(tuple, line.get_invcoordinate())) in lines.keys() :
                    if not line.is_diagonal():
                        if  line.is_boundaryline([np.max(xedges),np.min(xedges),np.max(yedges),np.min(yedges)]):
                            line.set_Weight(1000)
#                     print('already exist')
                    if line.weight!=lines[tuple(map(tuple, line.get_invcoordinate()))].weight and lines[tuple(map(tuple, line.get_invcoordinate()))].weight!=1.3:
#                         print(line.weight,lines.get(tuple(map(tuple, line.get_invcoordinate()))).weight)
                        lines[tuple(map(tuple, line.get_invcoordinate()))].set_Weight(1.3)
                else:
#                     print(tuple(map(tuple, line.get_coordinate())))
                    lines[tuple(map(tuple, line.get_coordinate()))]=line
                    if not line.is_diagonal():
                        if  line.is_boundaryline([np.max(xedges),np.min(xedges),np.max(yedges),np.min(yedges)]):
                            line.set_Weight(1000)
#                 if not line.passable:
#                     print(line.get_coordinate(),line.weight,line.passable)

    '''
    getting all points on the graph
    ''' 
    points={}
    for x in range(len(xedges)):
        for y in range(len(yedges)): 
#             print(tuple(grid_coordinate[x][y]))
            for key,linevalue in lines.items():
#                 print(key,linevalue)
                if linevalue.checkpoint(grid_coordinate[x][y]):
                    if tuple(grid_coordinate[x][y]) in points.keys():
#                         print('exist')
                        points[tuple(grid_coordinate[x][y])].add(key)
                    else:
                        points[tuple(grid_coordinate[x][y])]={key}
                else:
                    pass
    '''
    blocking of the boundaries
    '''    
    for key,pointvalue in points.items():  
        if len(pointvalue)<8:
            for line_key in pointvalue:
#                 lines[line_key].set_Weight(1000)
                if not lines[line_key].is_diagonal():
                    if  lines[line_key].is_boundaryline([np.max(xedges),np.min(xedges),np.max(yedges),np.min(yedges)]):
#                         lines[line_key].set_Weight(1000)  
                        print(lines[line_key].passable)    
                           
            print(key,len(pointvalue))

    '''
    Heuristic Search(check 2.1.5 e & f assignment pdf)
    '''
#     x1_coordinate = float(input("Enter the coordinate of x1: ")) 
#     y1_coordinate = float(input("Enter the coordinate of y1: ")) 
#     x2_coordinate = float(input("Enter the coordinate of x2: ")) 
#     y2_coordinate = float(input("Enter the coordinate of y2: ")) 
    x1_coordinate = float(-73.575) 
    y1_coordinate = float(45.496) 
    x2_coordinate = float(-73.557) 
    y2_coordinate = float(45.51) 
    x1_index=np.where(np.absolute(xedges-x1_coordinate) == np.min(np.absolute(xedges-x1_coordinate)))
    y1_index=np.where(np.absolute(yedges-y1_coordinate) == np.min(np.absolute(yedges-y1_coordinate)))
    x2_index=np.where(np.absolute(xedges-x2_coordinate) == np.min(np.absolute(xedges-x2_coordinate)))
    y2_index=np.where(np.absolute(yedges-y2_coordinate) == np.min(np.absolute(yedges-y2_coordinate)))
    start_point=(xedges[x1_index[0]][0], yedges[y1_index[0]][0])
    end_point=(xedges[x2_index[0]][0], yedges[y2_index[0]][0])
    plt.scatter (xedges[x1_index[0]][0], yedges[y1_index[0]][0])
    plt.scatter (xedges[x2_index[0]][0], yedges[y2_index[0]][0])

    start_time = time.time()
    print(heuristics(start_point,end_point,lines,points))
                    
    '''
    Final part for plotting
    '''


    for line in lines.values():
        line_x = np.linspace(line.get_coordinate()[0][0], line.get_coordinate()[1][0])
        line_y = np.linspace(line.get_coordinate()[0][1], line.get_coordinate()[1][1])
        if line.weight == 0:
            plt.plot(line_x, line_y, color=[0, 1, 0])
            '''
            uncomment lines below to see them coloured. line was commented out due to added 3.5 secs to time 
            '''
#         elif line.weight == 1:
#             plt.plot(line_x, line_y, color='#00aeff')    
#         elif line.weight == 1.3 :
#             plt.plot(line_x, line_y, color='#ffffff')
#         elif line.weight == 1.5:
#             plt.plot(line_x, line_y, color='#ffa600')   
#         elif not line.passable:
#             plt.plot(line_x, line_y, color=[1, 0, 0])   
#         else:
#             plt.plot(line_x, line_y, color=[1, 0, 0])
            
         
#     print(grid_coordinate[8][16],temp[8][16])
    plt.grid( linewidth=2)
    plt.setp(axes.get_xticklabels(), rotation=90)
    plt.suptitle(f'This is {threshold} percent threshold', fontsize=16)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    # plt.colorbar().ax.set_ylabel('Counts')
    a = mpatches.Patch(color=[1, 0, 0], label='Blocked path')
    b = mpatches.Patch(color=[0, 1, 0], label='Optimal path')
    c = mpatches.Patch(color='#00aeff', label='1.0 weighted lines')
    d = mpatches.Patch(color='#ffffff', label='1.3 weighted lines')#ff00f7
    e = mpatches.Patch(color='#ffa600', label='1.5 weighted lines')
    plt.legend(handles=[a,b,c,d,e], loc='center left', bbox_to_anchor=(1, 0.5))
      
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
