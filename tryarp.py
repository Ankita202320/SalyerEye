from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP, Ether
import threading
import datetime
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import tkinter as tk
from tkinter import scrolledtext

IP_MAC_PAIRS = {}
ARP_REQ_TABLE = {}
# create counters
fig, ax = plt.subplots()
fake = 0
attack = 0
genuine = 0

def sniff_requests():
    sniff(filter='arp', lfilter=outgoing_req, prn=add_req, iface=conf.iface)

def sniff_replays():
    sniff(filter='arp', lfilter=incoming_reply, prn=check_arp_header, iface=conf.iface)

def incoming_reply(pkt):
    return pkt[ARP].psrc != str(get_if_addr(conf.iface)) and pkt[ARP].op == 2

def outgoing_req(pkt):
    return pkt[ARP].psrc == str(get_if_addr(conf.iface)) and pkt[ARP].op == 1

def add_req(pkt):
    ARP_REQ_TABLE[pkt[ARP].pdst] = datetime.datetime.now()

def check_arp_header(pkt):
    if not pkt[Ether].src == pkt[ARP].hwsrc or not pkt[Ether].dst == pkt[ARP].hwdst:
        return alarm('inconsistent ARP message')
    return known_traffic(pkt)

def known_traffic(pkt):
    global attack, genuine, alarm_area
    if pkt[ARP].psrc not in IP_MAC_PAIRS.keys():
        return spoof_detection(pkt)
    elif IP_MAC_PAIRS[pkt[ARP].psrc] == pkt[ARP].hwsrc:
        genuine += 1
        return raise_alarm('!')
    else:
        print(f"ARP spoofing detected from: ", pkt[ARP].hwsrc)
        alarm_area.insert(tk.END, f"ARP spoofing detected from: "+ pkt[ARP].hwsrc+'\n')
        attack += 1

def spoof_detection(pkt):
    global fake
    ip_ = pkt[ARP].psrc
    t = datetime.datetime.now()
    mac = pkt[0][ARP].hwsrc
    if ip_ in ARP_REQ_TABLE.keys() and (t - ARP_REQ_TABLE[ip_]).total_seconds() <= 5:
        ip = IP(dst=ip_)
        SYN = TCP(sport=40508, dport=40508, flags="S", seq=12345)
        E = Ether(dst=mac)
        if not srp1(E / ip / SYN, verbose=False, timeout=3):
            alarm('No TCP ACK, fake IP-MAC pair')
            fake += 1
        else:
            IP_MAC_PAIRS[ip_] = pkt[ARP].hwsrc
    else:
        send(ARP(op=1, pdst=ip_), verbose=False)

def alarm(alarm_type):
    global alarm_area
    print('Under Attack', alarm_type)
    alarm_area.insert(tk.END, f'Under Attack {alarm_type}\n')

def raise_alarm(alarm_type):
    global alarm_area
    print('Genuine ARP Message', alarm_type)
    alarm_area.insert(tk.END, f'Genuine ARP Message {alarm_type}\n')

def update_pie_chart(num):
    global fake, attack, genuine
    data = [fake, attack, genuine]
   
    colors = ['cyan', 'aquamarine', 'cadetblue']
    labels = ['Fake IP-MAC Pair', 'Attack Happened', 'Genuine ARP']
    
    
    

    total = sum(data)  # Calculate the total count

    # Check if the total count is zero
    if total == 0:
        # Handle the case when all counts are zero
        autopct_param = ''
    else:
        autopct_param = '%1.1f%%'

    try:
    	ax.clear()
    	ax.pie(data, labels=labels, autopct=autopct_param, startangle=90, colors=colors, textprops={'color': 'white'})
    	ax.axis('equal')
    	plt.title('ARP Traffic Visualization',color='cyan')
    	#plt.legend(title='ARP Packets', color='white',loc='center ',bbox_to_anchor=( 0.5, -1))
    	ax.legend(title='ARP Packets', loc='center left', bbox_to_anchor=(1, 0.5), ncol=1)
    	plt.setp(ax.spines.values(), color='white')  # Set axis spines color
    	
    except Exception as e:
        print("Exception occurred:", e)
        print("Data:", data)
        print("Total:", total)

def start_sniffing():
    req_ = threading.Thread(target=sniff_requests, args=())
    req_.start()
    rep_ = threading.Thread(target=sniff_replays, args=())
    rep_.start()

def animate_graph():
    ani = animation.FuncAnimation(fig, update_pie_chart, interval=1000)
    plt.show()

def create_gui():
    global alarm_area
    window = tk.Tk()
    window.title(" ")
    window.configure(bg="black")  # Set background color to black
    window.geometry("900x600")
    #fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('white')  # Set the color of the bottom axis spine
    ax.spines['left'].set_color('white')  # Set the color of the left axis spine
    plt.setp(ax.yaxis.get_ticklabels(), color='white')  # Set tick label colors
    plt.setp(ax.xaxis.get_ticklabels(), color='white')   # Add the legend with custom labels and handles
    plt.setp(ax.spines.values(), color='white')  # Set axis spines color
    	

    



    '''canvas = tk.Canvas(window, width=400, height=300)
    canvas.pack()'''
    

    
    def run():
    	 start_sniffing()
    	 animate_graph()
    
   
    #run()
    start_button = tk.Button(window, text="Start Sniffing", bg= 'black',bd=0,command=run,activebackground='black', highlightthickness=0, borderwidth=0, )
    start_button.pack()

    '''graph_button = tk.Button(window, text="Show Graph", command=animate_graph)
    graph_button.pack()'''

    alarm_area = scrolledtext.ScrolledText(window, width=300, height=200)
    alarm_area.pack()
    alarm_area .configure(bg='black',fg='cyan')

    window.mainloop()

create_gui()



