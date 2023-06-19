import numpy as np
import csv
import matplotlib.pyplot as plt
import math

from matplotlib.animation import FuncAnimation

time_sec = []
lidar_angle_degree = []
lidar_range_meter = []

with open('ydlidar_20230612164330.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        time_sec.append((row[0]))
        a = row[1].strip("[]").split(",") # Remove the square brackets and Split the string into individual elements
        a = [float(x) for x in a]
        lidar_angle_degree.append(a)
        b = row[2].strip("[]").split(",")
        b = [float(x) for x in b]
        lidar_range_meter.append(b)

heading_data = []

with open('gpsPlus_20230612164330.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        heading_data.append(float(row[5]))

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
    alt = 0.0
    x = (earth_radius + alt) * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
    y = (earth_radius + alt) * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
    z = (earth_radius + alt) * math.sin(math.radians(lat))
    positions.append((x, y, z))

# ตำเเหน่งการเคลื่อนที่ของหุ่นยนต์ ในเเกน x เเละ y
xs = [pos[0] for pos in positions]
ys = [pos[1] for pos in positions]


def run_animation():
    # อัปเดตข้อมูลกราฟหรือองค์ประกอบกราฟตามต้องการ
    fig, ax = plt.subplots()
    x_data = []
    y_data = []
    scat = ax.scatter([], [], color='red')
    line, = ax.plot([], [], 'g')

    def update(frame):
        # x_data.append(xs[frame])
        # y_data.append(ys[frame])
        # scat.set_offsets(np.c_[xs[frame], ys[frame]])
        # line.set_data(x_data, y_data)
        # line.set_label('Robot Path')
        x = []
        y = []
        for j in range(len(lidar_angle_degree[frame])):
            # เช็ค quadrant ของข้อมูล lidra ตาม heading จาก GPS
            if 0<=heading_data[frame] and heading_data[frame]<=90:
                x.append(xs[frame]+lidar_range_meter[frame][j]*np.sin(np.radians(lidar_angle_degree[frame][j])))
                y.append(ys[frame]+lidar_range_meter[frame][j]*np.cos(np.radians(lidar_angle_degree[frame][j])))
            elif 90<heading_data[frame] and heading_data[frame]<=180:
          
                x.append(-1*(xs[frame]+lidar_range_meter[frame][j]*np.sin(np.radians(lidar_angle_degree[frame][j]))))
                y.append(ys[frame]+lidar_range_meter[frame][j]*np.cos(np.radians(lidar_angle_degree[frame][j])))
            elif 180<heading_data[frame] and heading_data[frame]<=270:
         
                x.append(-1*(xs[frame]+lidar_range_meter[frame][j]*np.sin(np.radians(lidar_angle_degree[frame][j]))))
                y.append(-1*(ys[frame]+lidar_range_meter[frame][j]*np.cos(np.radians(lidar_angle_degree[frame][j]))))
            elif 270<heading_data[frame] and heading_data[frame]<=360:
          
                x.append(1*(xs[frame]+lidar_range_meter[frame][j]*np.sin(np.radians(lidar_angle_degree[frame][j]))))
                y.append(-1*(ys[frame]+lidar_range_meter[frame][j]*np.cos(np.radians(lidar_angle_degree[frame][j]))))
        ax.clear()  # ล้างเนื้อหากราฟ
        ax.scatter(x, y, label='Data points')
        ax.legend()
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        

    # สร้างอนิเมชันที่ใช้ฟังก์ชัน update เพื่ออัปเดตกราฟในแต่ละเฟรม โดยใช้ข้อมูลจาก xs และแสดงผลเฟรมที่ 0 ถึงความยาวของ xs ตามลำดับ โดยแต่ละเฟรมจะแสดงผลเป็นเวลา 300 มิลลิวินาที (หรือ 0.3 วินาที)
    ani = FuncAnimation(fig, update, frames=range(len(xs)), interval=300, repeat=False)
    # repeat=False เพื่อให้เล่นรอบเดียว ถ้าจบต้องรัน codeใหม่

    is_anim_running = True  # เพิ่มตัวแปรเก็บสถานะการเล่น

    def play_pause(event):
        nonlocal is_anim_running  # เพิ่ม nonlocal เพื่อเปลี่ยนแปลงตัวแปรภายในฟังก์ชัน
        if is_anim_running:
            ani.event_source.stop()
            is_anim_running = False
        else:
            ani.event_source.start()
            is_anim_running = True
    
    play_pause_button = plt.Button(ax=plt.axes([0.8, 0.9, 0.15, 0.04]), label='Play/Pause')
    play_pause_button.on_clicked(play_pause)

    plt.show()


run_animation()
