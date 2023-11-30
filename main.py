
import os
import sys
from tkinter import ttk
from tkinter import *
import tkinter as tk
import customtkinter as ctk
from customtkinter import CTkButton, CTkImage
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import webbrowser
import psutil
from tkinter.filedialog import askopenfilename
import time

def file_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception as e:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


## include the appropriate folder address for chromedriver.exe
driver_path = file_path(r'chromedriver.exe')
driver = webdriver.Chrome(driver_path, options=opt)













# splash_screen
splash_win = Tk()
splash_win.geometry("400x280")
splash_win.overrideredirect(True)

image_0 = Image.open('./sp.png')
back_end = ImageTk.PhotoImage(image_0)


label = Label(splash_win, image=back_end, highlightthickness=0,
              relief='flat', borderwidth=0)
label.place(x=0, y=0)

screen_width = splash_win .winfo_screenwidth()
screen_height = splash_win .winfo_screenheight()
x_pos = int(screen_width / 2 - 500 / 2)
y_pos = int(screen_height / 2 - 500 / 2)
splash_win .geometry(f"+{x_pos}+{y_pos}")


def open_file_1():
	subprocess.Popen(['python', 'sniffer.py'])


def open_file_2():
	subprocess.Popen(['python', 'vulFinal.py'])
# def open_file_2():
# 	subprocess.Popen(['python', 'sniffer.py'])


def open_file_3():
	subprocess.Popen(['python', 'tryarp.py'])

def open_file_4():
	subprocess.Popen(['python', 'ddosdet.py'])


def open_file():
	file = askopenfilename()
	os.system('"%s"' % file)


def open_browser(e):
	webbrowser.open_new("https://www.google.co.in")


def main():
	# setup
	splash_win.destroy()
	window = tk.Tk()
	window.geometry('1900x865')
	window.title(' ')
	window['bg'] = '#02091B'
	# grid
	window.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1, uniform='a')
	window.rowconfigure(0 ,weight=1)

	def stretch_image(event):
		global resized_tk

	# size
		width = event.width
		height = event.height
		# ceate image
		resized_image = image_original.resize((width, height))
		resized_tk = ImageTk.PhotoImage(resized_image)

		# place on the canvas

		canvas.create_image(0, 0, image=resized_tk, anchor='nw')

	def fill_image(event):
		global resized_tk

		# current ratio
		canvas_ratio = event.width/event.height
		if canvas_ratio > image_ratio:
			width = int(event.width)
			height = int(width/image_ratio)
		resized_image = image_original.resize((width, height))
		resized_tk = ImageTK.PhotoImage(resized_image)
		canvas.create_image(int(event.width/2), int(event.height/2),
		                    anchor='center', image=resized_tk)

	# import image

	image_original = Image.open('ff.png')
	image_ratio = image_original.size[0]/image_original.size[1]
	image_tk = ImageTk.PhotoImage(image_original)

	# buttonframe
	button_Frame = ttk.Frame(window)

	ttk.Style().configure('Black.TFrame', background='black')
	button_Frame.configure(style='Black.TFrame')

	# menu------------------------
	python_dark = Image.open('menu.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image = CTkImage(python_dark)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='Menu',
	                       image=ctk_image, compound='left', bg_color='black',fg_color='black',font=("Tahoma",25,"bold"),width=200,height=40)
	button_ctk.pack(pady=10)
	
	
	#create home button--------------------------
	
	python_dark_1 = Image.open('home.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_1 = CTkImage(python_dark_1)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text=' Home ',
	                       image=ctk_image_1, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	#file --------------------------
	python_dark_2 = Image.open('file.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_2 = CTkImage(python_dark_2)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='   File   ',
	                       image=ctk_image_2, command=open_file,compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	#save-----------------------------
	
	python_dark_3 = Image.open('save.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_3= CTkImage(python_dark_3)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='  Save  ',
	                       image=ctk_image_3, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	#view------------------------
	
	python_dark_4 = Image.open('view.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_4= CTkImage(python_dark_4)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='  View   ',
	                       image=ctk_image_4, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	#settings
	python_dark_5 = Image.open('set.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_5 = CTkImage(python_dark_5)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='Settings',
	                       image=ctk_image_5, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	
	#help------------------------------
	python_dark_6 = Image.open('help.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_6 = CTkImage(python_dark_6)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='  Help    ',
	                       image=ctk_image_6, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
	
	#close-----------------------------------------------
	python_dark_7= Image.open('exit.png').resize((30, 30))

	# Convert the image to CTkImage format
	ctk_image_7= CTkImage(python_dark_7)

	# Create the button with the CTkImage

	button_ctk = CTkButton(button_Frame, text='  Close  ', command=window.destroy,
	                       image=ctk_image_7, compound='left', bg_color='black',font=("Tahoma",20),fg_color='black')
	button_ctk.pack(pady=10)
		
	#resize button...
	'''def resize_buttons(event):
	    # Get the current width and height of the window
	    window_width = event.width
	    window_height = event.height

	    # Calculate the new width and height for the buttons
	    button_width = window_width // 3
	    button_height = window_height // 3

	    # Update the size of the buttons
	    scan_button.place(width=button_width, height=button_height)
	    vul_button.place(width=button_width, height=button_height)
	    arp_button.place(width=button_width, height=button_height)
	    ddos_button.place(width=button_width, height=button_height)
	    br_button.place(width=button_width, height=button_height)'''
	    
	    
	   

	

	# wifi
	image_original1 = Image.open('wifi.png')

	image_tk1 = ImageTk.PhotoImage(image_original1)

	label1 = ttk.Label(button_Frame, image=image_tk1, background='black')
	label1.place(x=41, y=808)

	# eth
	eth = Image.open('eth.png')

	image_tk2 = ImageTk.PhotoImage(eth)

	label2 = ttk.Label(button_Frame, image=image_tk2,background='black')
	label2.place(x=0, y=808)

	window.columnconfigure(0, weight=1)
	window.rowconfigure(0, weight=1)
	button_Frame.grid(column=0, row=0, sticky='nsew')
	button_Frame.columnconfigure(0, weight=1)
	button_Frame.rowconfigure(0, weight=1)

	# button_Frame.grid(column=0 ,row=0,sticky= 'nsew')
	# canvas
	canvas = tk.Canvas(window, background='#02091B', bd=0,
	                   highlightthickness=0, relief='ridge', borderwidth=0)
	canvas.grid(column=1, row=0, columnspan=6, sticky='nsew')
	canvas.create_image(0, 0, image=image_tk, anchor='nw')
	canvas.bind('<Configure>', stretch_image)
	#canvas.bind('<Configure>', resize_buttons)
	#canvas.bind('<Configure>', lambda event: (stretch_image(event), resize_buttons(event)))


	# scan
	scan = Image.open('sc.png')
	scan_tk = ImageTk.PhotoImage(scan)
	scan_button = Button(canvas, text='sci',command=open_file_1, image=scan_tk, bg='#072F38',
	                     activebackground='#072F38', bd=0, highlightthickness=0, borderwidth=0, relief='ridge')
	scan_button.place(x=430, y=420)
	# vul
	vul = Image.open('vul.png')
	vul_tk = ImageTk.PhotoImage(vul)
	vul_button = Button(canvas, text='sci', command=open_file_2,image=vul_tk, bg='#072F38', activebackground='#072F38',
	                    height=65, bd=0, highlightthickness=0, borderwidth=0, relief='ridge')
	vul_button.place(x=860, y=422)
	# arp
	arp = Image.open('ar.png')
	arp_tk = ImageTk.PhotoImage(arp)
	arp_button = Button(canvas, text='sci',command=open_file_3, image=arp_tk, bg='#072F38',
	                    activebackground='#072F38', bd=0, highlightthickness=0, borderwidth=0, relief='ridge')
	arp_button.place(x=430, y=540)
	# ddos
	ddos = Image.open('do.png')
	ddos_tk = ImageTk.PhotoImage(ddos)
	ddos_button = Button(canvas, text='sci',command=open_file_4, image=ddos_tk, bg='#072F38',
	                     activebackground='#072F38', bd=0, highlightthickness=0, borderwidth=0, relief='ridge')
	ddos_button.place(x=860, y=540)
	# br
	br = Image.open('br.png')
	br_tk = ImageTk.PhotoImage(br)
	br_button = Button(canvas, text='sci', image=br_tk, bg='#072F38',
	                   activebackground='#072F38', bd=0, highlightthickness=0, borderwidth=0, relief='ridge',command=lambda: open_browser(1))
	br_button.place(x=640, y=660)
	
	
	#window.bind("<Configure>", resize_buttons)

	# network speed

	class NetworkSpeed(tk.Frame):
			def __init__(self, master):
				super().__init__(master)
				self.download_label = tk.Label(
					self, text="Download Speed: N/A,Upload Speed: N/A")
				# self.upload_label = tk.Label(self, text="Upload Speed: N/A")
				self.download_label.pack()
				# self.upload_label.pack()
				self.pack()
				self.update_speed()

			def update_speed(self):
				try:
					download_speed, upload_speed = get_network_speed()
					self.download_label.config(
						text=f"Download Speed: {download_speed:.2f} Mbps \n Upload Speed: {upload_speed:.2f} Mbps ", bg='black', fg='white')
					# self.upload_label.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
				except psutil.AccessDenied:
					self.download_label.config(text="No internet connection.")
					# self.upload_label.config(text="No internet connection.")
				except KeyboardInterrupt:
					sys.exit()

				self.after(1000, self.update_speed)

	def get_network_speed():
			net_io_counters = psutil.net_io_counters()
			bytes_sent = net_io_counters.bytes_sent
			bytes_recv = net_io_counters.bytes_recv
			time.sleep(1)
			net_io_counters = psutil.net_io_counters()
			bytes_sent_diff = net_io_counters.bytes_sent - bytes_sent
			bytes_recv_diff = net_io_counters.bytes_recv - bytes_recv
			download_speed = bytes_recv_diff / 1000000
			upload_speed = bytes_sent_diff / 1000000
			return download_speed, upload_speed

	speed = NetworkSpeed(button_Frame)
	speed.place(x=82, y=808)
	
	window.mainloop()
splash_win.after(4000, main)
mainloop()

