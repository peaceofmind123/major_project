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
import os
import sys
from tkinter import ttk, filedialog

matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)
matplotlib.interactive(True)


class DataLabeler(tk.Tk):
    def onclick(self, event):
        self.agg._tkcanvas.focus_force()

        print(event.x, event.y, event.xdata, event.ydata)
        if event.xdata is not None and event.ydata is not None:
            self.click_count += 1
            self.clicked_points.append((event.xdata, event.ydata))

            if self.click_count == 2:
                if self.temp_rect is not None:
                    self.temp_rect.remove()
                    self.temp_rect = None
                if self.clicked_points[0][0] > self.clicked_points[1][0]:
                    self.clicked_points = [
                        self.clicked_points[1], self.clicked_points[0]]
                self.image_points[self.filenames[self.filePointer]] = list(
                    self.clicked_points)
                self.point_plot.remove()
                self.rect = patches.Rectangle(tuple(self.clicked_points[0]),
                                              self.clicked_points[1][0] -
                                              self.clicked_points[0][0],
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
                self.point_plot = self.a.scatter(
                    [event.xdata], [event.ydata], c='r', s=2)
                self._refreshImage()
                self.agg.draw()

    def onMove(self, event):

        if self.click_count != 1:
            return

        if self.temp_rect is not None:
            self.temp_rect.remove()
            self.temp_rect = None

        self.temp_rect = patches.Rectangle(tuple(
            self.clicked_points[0]),
            event.xdata-self.clicked_points[0][0],
            event.ydata-self.clicked_points[0][1],
            facecolor=(1, 1, 1, 0),
            edgecolor='r',
            linewidth=1)

        self.a.add_patch(self.temp_rect)
        self.agg.draw()

    def onUndo(self, event):
        sys.stdin.flush()
        print(event.key)

        if event.key == 'escape':

            self.click_count = 0
            self.clicked_points = []

            if self.rect is not None:
                self.rect.remove()
                self.rect = None
            if self.temp_rect is not None:
                self.temp_rect.remove()
                self.temp_rect = None
            if self.point_plot is not None:
                self.point_plot.remove()
                self.point_plot = None
            gc.collect()

            self.agg.draw()

    def onLoadImages(self):
        filenames = []
        for root, directories, files in os.walk('./images'):
            if files is not None:
                for f in files:
                    filenames.append(f'{root}/{f}')

        if len(filenames) != 0:
            if len(self.filenames) == 0:
                self.filenames = filenames
            else:

                self.filenames.extend(filenames)

            self._refreshImage()

    def _save(self):
        if self.image_points is not None and len(self.image_points) > 0:
            with open('data.json', "w+") as dataFile:
                dataFile.write(json.dumps(self.image_points))

            with open('data.xml', 'w+') as dataFileX:
                dataFileX.write(str(dicttoxml(self.image_points)))

    def _refreshImage(self):

        try:
            if self.img is not None:
                for i in range(len(self.a.images)):
                    del self.a.images[i]

                del self.img
                self.img = None
                gc.collect()  # for efficiency
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

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Data Labeler")
        self.filenames = []
        self.clicked_points = []
        self.click_count = 0
        self.point_plot = None
        self.image_points = dict()
        self.rect = None
        self.temp_rect = None
        self.img = None
        self.f = Figure(figsize=(10, 10), dpi=200)
        self.a = self.f.add_subplot(111)
        self.a.autoscale(tight=True)
        self.filePointer = 0
        topFrame = tk.Frame(self)
        topFrame.pack()

        button1 = ttk.Button(topFrame, text="Load Images",
                             command=lambda: self.onLoadImages())
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
        self.agg.mpl_connect('key_press_event', self.onUndo)
        self.agg.mpl_connect('motion_notify_event', self.onMove)
        self.agg.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.agg, self)
        toolbar.update()
        self.agg._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.agg._tkcanvas.focus_force()
        print(self.focus_displayof())


app = DataLabeler()

app.mainloop()
