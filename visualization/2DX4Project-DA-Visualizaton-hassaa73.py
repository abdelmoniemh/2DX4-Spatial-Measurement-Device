import serial
import math
import numpy as np
import open3d as o3d

print('start')
s = serial.Serial('COM3', 115200)
print("Opening: " + s.name)

ALLdata = []
for x in range(10): #read all inputs from n rotations
    data = []
    print(f"\n rotation{x} begun\n")
    while(1):# run until recieve the keyword 'break' to signify end of data stream
        temp = ""
        while(1): #read until a newline character which is end on sentence/word
            x = s.read()
            c = x.decode()  
            if c == '\n':
                break
            temp += c
        data.append(temp)
        #print(temp)
        if temp == 'break':
            print(f"\n rotation{x} completed\n")
            break
    ALLdata.append(data)


print("Closing: " + s.name)
s.close();
for i in range(len(ALLdata)):
    ALLdata[i] = ALLdata[i][10:len(ALLdata[i])-1]


for x in range(len(ALLdata)):
    for i in range(len(ALLdata[x])):# cylindrical coordinates -> rectangular coordinates
        r = int(ALLdata[x][i].split(', ')[1])
        divisor = (len(ALLdata[x])/2)
        ALLdata[x][i] = [ r*math.cos(i*math.pi/divisor), int(r*math.sin(i*math.pi/divisor)), x*100] 
    
xyz = open("tof_radar.xyz", "w")
for x in range(len(ALLdata)): #writing coordinates to xyz file
    for i in range(len(ALLdata[x])):
        xyz.write(f"{ALLdata[x][i][1]} {ALLdata[x][i][0]} {ALLdata[x][i][2]}\n")
xyz.close()
    


pcd = o3d.io.read_point_cloud("tof_radar.xyz", format="xyz") #read coordinates from xyz file

points = list(np.asarray(pcd.points)) #convert into mutable python list
for i in range(len(points)):
    points[i] = list(points[i])

lines = []

for i in range(len(ALLdata)): # connect points within a singular plane
    for j in range(len(ALLdata[i])):
        j = j + (i*len(ALLdata[i]))
        lines.append([j,(j+1)%(len(ALLdata[i])) + len(ALLdata[i])*i])
      
for i in range(len(ALLdata)-1): #connect planes with lines
    for j in range(len(ALLdata[i])):
        j = j + (i*len(ALLdata[i]))
        lines.append([j, j+len(ALLdata[i])])

#print(lines)

colors = [[1, 0, 0] for i in range(len(lines))]
line_set = o3d.LineSet() #init lineset object to plot
line_set.points = o3d.Vector3dVector(np.asarray(pcd.points))
line_set.lines = o3d.Vector2iVector(lines)
line_set.colors = o3d.Vector3dVector(colors)


o3d.visualization.draw_geometries([line_set]) #plot geometry

