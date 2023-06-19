import numpy as np
import csv
import matplotlib.pyplot as plt
import math
from mpl_toolkits.mplot3d import Axes3D


time_sec = []
lidar_angle_degree = []
lidar_range_meter = []

with open('ydlidar_20230612164330.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        time_sec.append((row[0]))
        a=(row[1])
        a = a.strip("[]")  # Remove the square brackets
        a = a.split(",")  # Split the string into individual elements
        a = [float(x) for x in a] 
        lidar_angle_degree.append(a)
        b=(row[2])
        b = b.strip("[]")  # Remove the square brackets
        b = b.split(",")  # Split the string into individual elements
        b = [float(x) for x in b] 
        lidar_range_meter.append(b)

# lat_data = []
# long_data = []
heading_data = []

with open('gpsPlus_20230612164330.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        # lat_data.append((row[1]))
        # long_data .append((row[2]))
        heading_data.append(float(row[5]))

# print(time_sec)
# print(lidar_angle_degree)
# print(lidar_range_meter)

# print(lat_data[10])
# print(long_data)
# print(heading_data)

# อ่านข้อมูล GPS จากไฟล์ .csv
data = []
with open('gpsPlus_20230612164330.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# แปลงพิกัดทางภูมิศาสตร์ (latitude, longitude) เป็นพิกัด XYZ ในกรอบพื้นผิวโลก (World Frame)
earth_radius = 6371000  # รัศมีของโลก (หน่วยเมตร)
positions = []
for row in data:
    lat = float(row['gps_recentLatitudeN'])
    lon = float(row['gps_recentLongitudeE'])
    alt = 0.0  # สมมุติว่าหุ่นยนต์อยู่ในระดับความสูงเดียวกับพื้นผิวโลก
    x = (earth_radius + alt) * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
    y = (earth_radius + alt) * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
    z = (earth_radius + alt) * math.sin(math.radians(lat))
    positions.append((x, y, z))

xs = [pos[0] for pos in positions]
ys = [pos[1] for pos in positions]
# print(len(xs))

# กำหนดขนาดของหน้าต่างกราฟ
plt.figure(figsize=(12, 8))  # กำหนดขนาดเป็น 8x6 นิ้ว
for i in range(len(lidar_range_meter)):

   
    x = []
    y = []
    for j in range((len(lidar_angle_degree[i]))):
        if 0<=heading_data[i] and heading_data[i]<=90:
            x.append(xs[i]+lidar_range_meter[i][j]*np.sin(np.radians(lidar_angle_degree[i][j])))
            y.append(ys[i]+lidar_range_meter[i][j]*np.cos(np.radians(lidar_angle_degree[i][j])))
        elif 90<heading_data[i] and heading_data[i]<=180:
          
            x.append(-1*(xs[i]+lidar_range_meter[i][j]*np.sin(np.radians(lidar_angle_degree[i][j]))))
            y.append(ys[i]+lidar_range_meter[i][j]*np.cos(np.radians(lidar_angle_degree[i][j])))
        elif 180<heading_data[i] and heading_data[i]<=270:
         
            x.append(-1*(xs[i]+lidar_range_meter[i][j]*np.sin(np.radians(lidar_angle_degree[i][j]))))
            y.append(-1*(ys[i]+lidar_range_meter[i][j]*np.cos(np.radians(lidar_angle_degree[i][j]))))
        elif 270<heading_data[i] and heading_data[i]<=360:
          
            x.append(1*(xs[i]+lidar_range_meter[i][j]*np.sin(np.radians(lidar_angle_degree[i][j]))))
            y.append(-1*(ys[i]+lidar_range_meter[i][j]*np.cos(np.radians(lidar_angle_degree[i][j]))))

    plt.clf() 
    plt.plot(xs[:i+1], ys[:i+1],'g') 
    plt.scatter(xs[i], ys[i], color='red')
    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.pause(.3)

    
plt.show()