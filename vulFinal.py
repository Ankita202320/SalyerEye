from tkinter import *
import nmap
import psutil
import netifaces
import os
import datetime
import time
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import speedtest
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
# Create the tkinter window


# Define IP range to scan
ip_range = "192.168.164.131"

# Define port range to scan
port_range = "1-500"

# Perform port scan using nmap
nm = nmap.PortScanner()
nm.scan(hosts=ip_range, ports=port_range, arguments="-A")

open_ports = []
bytes_sent_diff = 0
bytes_recv_diff = 0
cpu_usage = 0
memory_usage = 0
download_speed = 0
upload_speed = 0

for host in nm.all_hosts():
    if nm[host].state() == "up":
        if "tcp" in nm[host]:
            for port in nm[host]["tcp"]:
                if nm[host]["tcp"][port]["state"] == "open":
                    open_ports.append(f"Port {port}: {nm[host]['tcp'][port]['name']}")

    # Check network load and bandwidth usage
    net_io_counters = psutil.net_io_counters()
    bytes_sent = net_io_counters.bytes_sent
    bytes_recv = net_io_counters.bytes_recv
    time.sleep(1)
    net_io_counters = psutil.net_io_counters()
    bytes_sent_diff = net_io_counters.bytes_sent - bytes_sent
    bytes_recv_diff = net_io_counters.bytes_recv - bytes_recv

    # Check CPU usage and memory usage
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    # Get network speed
    interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
    speed_test = speedtest.Speedtest()
    download_speed = round(speed_test.download() / 10**6)
    upload_speed = round(speed_test.upload() / 10**6)


# Check disk usage
disk_usage = psutil.disk_usage(os.path.abspath(os.sep))
total_disk_space = round(disk_usage.total / 1024**3)
used_disk_space = round(disk_usage.used / 1024**3)
free_disk_space = round(disk_usage.free / 1024**3)

# Define the data
parameters = ['Total disk space', 'Used disk space', 'Free disk space', 'Disk usage', 'CPU usage', 'Memory usage', 'Download speed', 'Upload speed']
values = [total_disk_space, used_disk_space, free_disk_space, disk_usage.percent, cpu_usage, memory_usage, download_speed, upload_speed]

# Create a DataFrame from the data
df = pd.DataFrame({'Parameters': parameters, 'Values': values})





'''width = 8
height = 6

# Create a figure with the specified size
plt.figure(figsize=(width, height))'''

# Set the figure size
'''fig, ax = plt.subplots(figsize=(12, 8))
ax.set_facecolor('black')
fig.patch.set_facecolor('black')'''

width = 12
height = 8

# Create a figure
fig = plt.figure()

# Set the figure size using figsize attribute
fig.set_size_inches(width, height)

# Get the axes
ax = fig.add_subplot(1, 1, 1)

# Customize the figure and axes as needed
ax.set_facecolor('black')
fig.patch.set_facecolor('black')








# Change axis color to white
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.spines['bottom'].set_edgecolor('white')
ax.spines['left'].set_edgecolor('white')

# Create the bar plot
bar_plot = plt.bar(df['Parameters'], df['Values'], color=['cyan', 'aquamarine', 'lightseagreen', 'darkturquoise', 'cadetblue', 'teal', 'mediumseagreen', 'turquoise'])

# Add value labels on top of each bar
for i, v in enumerate(df['Values']):
    plt.text(i, v + 1, str(v), ha='center', va='bottom', fontweight='bold', color="white")

# Get system uptime
output = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
system_uptime = output[3:]  # Remove "up "

# Add hostname, bytes sent, bytes received, and open ports information on the left side of the graph
'''plt.text(-0.4, max(df['Values']) + 21, f"Hostname: Kaliuser", color="white", fontsize=10, fontweight='bold')
plt.text(-0.4, max(df['Values']) + 19, f"System Uptime: {system_uptime}", color="white", fontsize=10, fontweight='bold')
plt.text(-0.4, max(df['Values']) + 17, f"Bytes Sent: {bytes_sent_diff}", color="white", fontsize=10, fontweight='bold')
plt.text(-0.4, max(df['Values']) + 15, f"Bytes Received: {bytes_recv_diff}", color="white", fontsize=10, fontweight='bold')'''
#plt.text(-0.4, max(df['Values']) + 11, f"Open Ports: {len(open_ports)}", color="white", fontsize=10, fontweight='bold')

# Set y-axis limits to accommodate the additional text labels
plt.ylim(0, max(df['Values']) + 15)

# Add a text box to display open ports information
open_ports_info = '\n'.join(open_ports)
#plt.text(-0.4, 49, f"Open Ports:\n{open_ports_info}", color="white", fontsize=10, fontweight='bold')

# Set labels and title
plt.xlabel('Parameters -------->', color="cyan" )
plt.ylabel('Real-Time Values ------->', color="cyan")
plt.title('Real-Time Vulnerability Check Within Own Network', color="cyan", fontweight='bold', pad=40)
plt.subplots_adjust(left=0.1, bottom=0.4)

# Adjust the bottom margin to move the graph downwards
#plt.subplots_adjust(left=0.1, bottom=0.2)


#resize window
new_figure_width = 12
new_figure_height = 25
fig.set_size_inches(new_figure_width, new_figure_height)

#try
plt.annotate(f"Hostname: Kaliuser", (+0.1, -0.5), xycoords='axes fraction', color="white", fontsize=12, fontweight='bold')
plt.annotate(f"System Uptime: {system_uptime}", (+0.1, -0.55), xycoords='axes fraction', color="white", fontsize=12, fontweight='bold')
plt.annotate(f"Bytes Sent: {bytes_sent_diff}", (+0.1, -0.6), xycoords='axes fraction', color="white", fontsize=12, fontweight='bold')
plt.annotate(f"Bytes Received: {bytes_recv_diff}", (+0.1, -0.65), xycoords='axes fraction', color="white", fontsize=12, fontweight='bold')
plt.annotate(f"Open port:{open_ports_info}",(+0.1,-0.7),xycoords='axes fraction', color="white", fontsize=12, fontweight='bold')
# Rotate x-axis labels if needed
plt.xticks(rotation=45)

# Show the plot
plt.show()


