import serial
import serial.tools.list_ports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading
import time


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.ser = serial.Serial(baudrate=250000, timeout=1)
#        self.t = threading.Thread(name='recivedata',target = self.ReadData,daemon=True )
#        self.m = multiprocessing.Process(None,self.ReadData)
#         self.m.start()
        self.data_list = np.array([0, 0, 0], dtype='float32')
        self.filename = ""
        self.is_save = True
        self.init_window("Pulsometr")

    def init_window(self, name):
        self.title(name)
        self.state('zoomed')
        self.minsize(1280, 720)
        self.configure(background='white')
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        menubar = Menu(self)
        self.config(menu=menubar)
        file = Menu(menubar, tearoff=0)
        file.add_command(label="New", command=self.Createfile)
        file.add_command(label="Open...", command=self.Openfile)
        file.add_command(label="Save", command=self.Save)
        file.add_command(label="Save as...", command=self.Save_as)
        file.add_separator()
        file.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file)
        options = Menu(menubar, tearoff=0,)
        self.data_switch = StringVar(value='A')
        data = Menu(options, tearoff=0)
        data.add_radiobutton(label="Only Lux", variable=self.data_switch, value='L', command=self.Plot)
        data.add_radiobutton(label="Only Pressure", variable=self.data_switch, value='P', command=self.Plot)
        data.add_radiobutton(label="Lux and Preassure", variable=self.data_switch, value='A', command=self.Plot)
        options.add_cascade(label="Data", menu=data)
        self.port = StringVar(value=serial.tools.list_ports.comports(include_links=False)[-1].device)
        self.ports_menu = Menu(options, tearoff=0, postcommand=self.Ports)
        options.add_cascade(label="Select port", menu=self.ports_menu)
        menubar.add_cascade(label="Options", menu=options)

        self.Plot(False)
        self.connect = ttk.Button(self, text="Connect", command=self.Connect)
        self.connect.place(relx=0.42, rely=0.0, anchor=NW)
        self.start = ttk.Button(self, text="Start", command=self.Start)
        self.start.place(relx=0.58, rely=0.0, anchor=NE)
        self.pressure = ttk.Label(self, text="0", width=5, borderwidth=2, relief="groove")
        self.pressure.place(relx=0.501, rely=0.005, anchor=N)
        self.min = ttk.Entry(self)
        self.min.place(relx=0.68, rely=0.961, width=40, anchor=NW)
        minlabel = ttk.Label(self, text="min= ", width=8, borderwidth=2)
        minlabel.place(relx=0.65, rely=0.961, width=40, anchor=NW)
        self.max = ttk.Entry(self)
        self.max.place(relx=0.76, rely=0.961, width=40, anchor=NW)
        maxlabel = ttk.Label(self, text="max= ", width=8, borderwidth=2)
        maxlabel.place(relx=0.73, rely=0.961, width=40, anchor=NW)
        cut = ttk.Button(self, text="Cut", command=self.Cut)
        cut.place(relx=0.8, rely=0.96, anchor=NW)

    def on_exit(self):
        self.IsSave()
        self.quit()

    def Ports(self):
        self.ports_menu.delete(0, 1)
        for ports in serial.tools.list_ports.comports(include_links=False):
            self.ports_menu.add_radiobutton(label=ports.device, variable=self.port, value=ports.device)

    def Connect(self):
        if(self.ser.is_open):
            self.ser.close()
            self.connect['text'] = "Connect"
            self.t._is_stopped = True
            self.t.join()
        else:
            try:
                self.ser.port = self.port.get()
                self.ser.open()
                self.connect['text'] = "Disconnect"
                self.t = threading.Thread(name='recivedata', target=self.ReadData, daemon=True)
                self.t.start()
            except serial.serialutil.SerialException:
                messagebox.showerror("Error", "Unable to connect port " + self.port.get())

    def Start(self):
        if(self.start['text'] == 'Stop'):
            self.start["text"] = "Start"
            self.ser.write(b'O')
            self.Plot()

        elif(self.ser.is_open):
            self.IsSave()
            self.is_save = False
#            self.connect.state= "DISABLED"
            self.ser.flush()
            self.ser.write(b'C')
#            self.ser.write(b'M \xFF\xFF')

            self.start['text'] = "Stop"
        else:
            messagebox.showinfo("Info", "No connection to the port")

    def Save(self):
        if(self.filename == ""):
            self.Save_as()
        if(len(self.data_list) and self.filename != ''):
            file = open(self.filename, "w")
            file.write("time [ms]\tPressure [Hgmm]\tilluminance [lux]\n")
            for row in self.data_list[1:]:
                file.write(np.array2string(row, formatter={'float_kind': lambda x: "%.2f" % x}, precision=3, separator=' \t ').replace('[', '').replace(']', '') + "\n")
            self.is_save = True
            file.close()

    def Save_as(self):
        tmp = asksaveasfilename(title="Chose location", initialfile='data.txt', defaultextension='.txt', filetypes=[('text file', '.txt'), ('all files', '.*')])
        if(len(tmp) != 0):
            self.filename = tmp
            self.Save()

    def Createfile(self):
        self.IsSave()

    def Openfile(self):
        self.IsSave()
        tmp = askopenfilename(title="Chose file", initialfile='data.txt', defaultextension='.txt', filetypes=[('text file', '.txt'), ('all files', '.*')])
        print(tmp)
        if(tmp != ""):
            self.filename = tmp
            file = open(self.filename, "r")
            file.readline()
            for line in file:
                line = line.split("\t")
                line = np.array([float(line[0]), float(line[1]), float(line[2])])
                self.data_list = np.vstack([self.data_list, line])
            file.close()
            # self.Plot()

    def ReadData(self):
        while True:

            while self.ser.in_waiting:
                tmp = self.ser.readline().decode().split()
                self.pressure['text'] = str(tmp[0])
                if(tmp[0] != "OK"):
                    tmp = [float(tmp[0]), float(tmp[1]), float(tmp[2])]
                    tmp = np.array([tmp[0] / 1000, tmp[1], tmp[2]])
                    self.data_list = np.vstack([self.data_list, tmp])
            time.sleep(0.015)

    def IsSave(self):
        if not self.is_save and len(self.data_list) > 3:
            tmp = messagebox.askokcancel("Save", "Would you like to save the data?")
            if(tmp is True):
                self.Save()
        self.data_list = np.array([0, 0, 0], dtype='float32')

    def Plot(self, update=True):
        if(update):
            liste = np.copy(self.data_list)
            if(self.data_switch.get() == 'A' and len(liste) > 3):
                fft1 = np.fft.rfft(self.data_list[1:, 1] - np.mean(liste[1:, 1]), norm="ortho")
                fft2 = np.fft.rfft(self.data_list[1:, 2] - np.mean(liste[1:, 2]), norm="ortho")
                fft1 = np.absolute(fft1)
                fft2 = np.absolute(fft2)
                t = self.data_list[1:, 0]
                freq = np.fft.rfftfreq(t.shape[-1], d=0.025)
                self.ax[0].set_title('Graph of light intensity and pressure from time', fontsize=14)
                self.ax[0].set_ylabel('pressure [Hgmm]', fontsize=12)
                self.ax[1].set_ylabel('illuminance [lx]', fontsize=12)
                self.x1.set_data(liste[1:, 0], liste[1:, 1])
                self.X1.set_data(freq, fft1)
                self.X2.set_data(freq, fft2)
                self.x2.set_data(liste[1:, 0], liste[1:, 2])
                self.ax[0].get_yaxis().set_visible(True)
                self.ax[1].get_yaxis().set_visible(True)
                self.ax[2].get_yaxis().set_visible(True)
                self.ax[3].get_yaxis().set_visible(True)
            elif(self.data_switch.get() == 'P'and len(liste) > 3):
                self.ax[0].set_title('Graph of pressure from time', fontsize=14)
                self.ax[0].set_ylabel('pressure [Hgmm]', fontsize=12)
                self.ax[1].set_ylabel('', fontsize=12)
                self.ax[0].get_yaxis().set_visible(True)
                self.ax[1].get_yaxis().set_visible(False)
                self.ax[2].get_yaxis().set_visible(True)
                self.ax[3].get_yaxis().set_visible(False)
                self.x1.set_data(self.data_list[1:, 0], self.data_list[1:, 1])
                self.x2.set_data([], [])
                #self.X1.set_data(freq, fft1)
                self.X2.set_data([], [])
            elif(self.data_switch.get() == 'L'and len(liste) > 3):
                self.ax[0].set_title('Graph of light intensity from time', fontsize=14)
                self.ax[0].set_ylabel('illuminance [lx]', fontsize=12)
                self.ax[1].set_ylabel('', fontsize=12)
                self.ax[0].get_yaxis().set_visible(False)
                self.ax[1].get_yaxis().set_visible(True)
                self.ax[2].get_yaxis().set_visible(False)
                self.ax[3].get_yaxis().set_visible(True)
                self.x1.set_data([], [])
                self.x2.set_data(self.data_list[1:, 0], self.data_list[1:, 2])
                self.X1.set_data([], [])
                #self.X2.set_data(freq, fft2)

            for x in self.ax:
                x.relim()
                x.autoscale_view()
            self.canvas.draw()

        else:

            fig, ax = plt.subplots(2, 1, constrained_layout=True)
            self.ax = [ax[0], ax[0].twinx(), ax[1], ax[1].twinx()]
            fig.set_figheight(self.winfo_screenheight() / 120)
            fig.set_figwidth(self.winfo_screenwidth() / 120)
            self.canvas = FigureCanvasTkAgg(fig, master=self)
            self.canvas._tkcanvas.place(relx=0.5, rely=0.04, anchor=N)
            self.x1, = self.ax[0].plot([], [], label="pressure")

            self.ax[0].legend(bbox_to_anchor=(1.08, 1.0), loc='upper left', borderaxespad=0.)
            self.ax[0].set_xlabel('time [s]', fontsize=12)
            self.ax[0].set_ylabel('pressure [Hgmm]', fontsize=12)
            self.ax[0].xaxis.set_minor_locator(MaxNLocator(115))
            self.ax[0].xaxis.set_major_locator(MaxNLocator(23))
            self.ax[0].yaxis.set_major_locator(MaxNLocator(11))
            self.ax[0].tick_params(which='major', length=0.1)
            self.ax[0].grid(which='major', alpha=1)
            self.ax[0].grid(which='minor', ls='--', alpha=0.4)
            self.ax[0].set_title('Graph of light intensity and pressure from time', fontsize=14)

            self.x2, = self.ax[1].plot([], [], 'r', label="illuminance")
            self.ax[1].legend(bbox_to_anchor=(1.08, 0.88), loc='upper left', borderaxespad=0.)
            self.ax[1].yaxis.set_major_locator(MaxNLocator(12))
            self.ax[1].set_ylabel('illuminance [lx]', fontsize=12)

            self.X1, = self.ax[2].plot([], label="pressure")
            self.ax[2].legend(bbox_to_anchor=(1.08, 1.0), loc='upper left', borderaxespad=0.)
            self.ax[2].set_xlabel('Freq [Hz]', fontsize=12)
            self.ax[2].xaxis.set_minor_locator(MaxNLocator(115))
            self.ax[2].xaxis.set_major_locator(MaxNLocator(23))
            self.ax[2].tick_params(which='major', length=0.1)
            self.ax[2].grid(which='major', alpha=1)
            self.ax[2].grid(which='minor', ls='--', alpha=0.4)
            self.ax[2].set_ylabel('', fontsize=12)
            self.ax[2].set_title('Fast Fourier Transform', fontsize=14)
            self.X2, = self.ax[3].plot([], 'r', label="illuminance")
            self.ax[3].legend(bbox_to_anchor=(1.08, 0.88), loc='upper left', borderaxespad=0.)
            toolbar = NavigationToolbar2Tk(self.canvas, self)
            toolbar.update()
            timer = fig.canvas.new_timer(interval=500)
            timer.add_callback(self.Plot, True)
            timer.start()

    def Cut(self):
        max = 100000
        min = 0
        tmp = np.array([0, 0, 0])
        if(self.min.get() != ''):
            min = float(self.min.get())
        if(self.max.get() != ''):
            max = float(self.max.get())
        if(min > max):
            messagebox.showerror("Error", 'min > max \n' + str(min) + '  >  ' + str(max))
        else:
            for row in self.data_list:
                if row[0] > min and row[0] < max:
                    tmp = np.vstack([tmp, row])
            self.data_list = tmp
            self.Plot()


if __name__ == '__main__':
    root = Root()
    root.mainloop()
