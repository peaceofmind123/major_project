import matplotlib
import gc
import json
from dicttoxml import dicttoxml
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.image as mpimg
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, filedialog

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)
matplotlib.interactive(True)

class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="bird.jpg")
        tk.Tk.wm_title(self, "Data Labeler")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        frame = PageThree(container, self)

        self.frames[PageThree] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageThree)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class PageThree(tk.Frame):
    def onclick(self,event):
        print(event.x, event.y, event.xdata, event.ydata)
        if event.xdata is not None and event.ydata is not None:
            self.click_count += 1
            self.clicked_points.append((event.xdata, event.ydata))

            if self.click_count == 2:
                if self.clicked_points[0][0] > self.clicked_points[1][0]:
                    self.clicked_points = [self.clicked_points[1], self.clicked_points[0]]
                self.image_points[self.filenames[self.filePointer]] = list(self.clicked_points)
                self.point_plot.remove()
                self.rect = patches.Rectangle(tuple(self.clicked_points[0]),
                                                   self.clicked_points[1][0] - self.clicked_points[0][0],
                                                   self.clicked_points[1][1] - self.clicked_points[0][1], edgecolor='r',
                                                   facecolor=(1, 1, 1, 0), linewidth=1)
                self.a.add_patch(self.rect)
                self.point_plot = None

                self.click_count = 0
                self.clicked_points = []
                self.agg.draw()
                print(self.image_points)
                self._save()

            elif self.click_count == 1:
                if self.rect is not None:
                    self.rect.remove()
                    self.rect = None
                if self.point_plot is not None:
                    self.point_plot = None
                gc.collect()
                self.point_plot = self.a.scatter([event.xdata], [event.ydata],c='r',s=20)
                self.a.autoscale(tight=True)
                self.agg.draw()

    def onSelectImages(self):
        filenames = list(filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                         filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*"))))

        if len(filenames) != 0:
            if len(self.filenames) == 0:
                self.filenames = filenames
            else:

                self.filenames.extend(filenames)

            self._refreshImage()

    def _save(self):
        if self.image_points is not None and len(self.image_points) > 0:
            with open('data.json',"w+") as dataFile:
                dataFile.write(json.dumps(self.image_points))

            with open('data.xml','w+') as dataFileX:
                dataFileX.write(str(dicttoxml(self.image_points)))

    def _refreshImage(self):

        try:
            if self.img is not None:
                for i in range(len(self.a.images)):
                    del self.a.images[i]

                del self.img
                self.img = None
                gc.collect() # for efficiency
            self.img = mpimg.imread(self.filenames[self.filePointer])
        except Exception as e:
            print(e)
            return

        self.a.imshow(self.img, cmap='gray')

        self.agg.draw()

    def onPrevious(self):
        if self.filePointer > 0:
            self.filePointer -= 1
            if self.rect is not None:
                self.rect.set_visible(False)
            self._refreshImage()

    def onNext(self):
        if self.filePointer < len(self.filenames)-1:
            self.filePointer += 1
            if self.rect is not None:
                self.rect.set_visible(False)
            self._refreshImage()


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Labeling UI", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.filenames = []
        self.clicked_points = []
        self.click_count = 0
        self.point_plot = None
        self.image_points = dict()
        self.rect = None
        self.img = None
        self.f = Figure(figsize=(10, 10), dpi=200)
        self.a = self.f.add_subplot(111)
        self.a.autoscale(tight=True)
        self.filePointer = 0
        topFrame = tk.Frame(self)
        topFrame.pack()

        button1 = ttk.Button(topFrame, text="Select Images",
                             command=lambda: self.onSelectImages())
        button2 = ttk.Button(topFrame, text="Previous",
                             command=lambda: self.onPrevious())
        button3 = ttk.Button(topFrame, text="Next",
                             command=lambda: self.onNext())

        button2.pack(side=tk.LEFT)
        button1.pack(side=tk.LEFT)
        button3.pack(side=tk.LEFT)


        if len(self.filenames) != 0:
            self.img = mpimg.imread(self.filenames[0])
            self.a.imshow(self.img)

        self.agg = FigureCanvasTkAgg(self.f, self)
        self.agg.mpl_connect('button_press_event', self.onclick)
        self.agg.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.agg, self)
        toolbar.update()
        self.agg._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()

app.mainloop()




