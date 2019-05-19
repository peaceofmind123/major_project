# Copyright Ashish Paudel, 2019. All rights reserved.
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
import copy

# Constants
PAGE_TITLE = "Data Labeler"
FIG_SIZE = (10, 10)
DPI = 200
LOAD_BTN_TEXT = "Load Images"
PREV_BTN_TEXT = "Previous"
NEXT_BTN_TEXT = "Next"
RECT_FACE_COLOR = (1, 1, 1, 0)
RECT_EDGE_COLOR = "r"
LINE_WIDTH = 1
POINT_SIZE = 2
KEYCODE_ESCAPE = "escape"
BTNPRESS_EVENT_NAME = "button_press_event"
KEYPRESS_EVENT_NAME = "key_press_event"
MOUSEMOVE_EVENT_NAME = "motion_notify_event"
LARGE_FONT = ("Verdana", 12)
IMAGE_DIR = "images"

matplotlib.use("TkAgg")
matplotlib.interactive(True)


class DataLabeler(tk.Tk):
    """
    The main application class.
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, PAGE_TITLE)
        self.filenames = []
        self.clicked_points = []
        self.click_count = 0
        self.point_plot = None
        self.image_points = dict()
        self.rect = None
        self.temp_rect = None
        self.img = None
        self.f = Figure(figsize=FIG_SIZE, dpi=DPI)
        self.a = self.f.add_subplot(111)
        self.a.autoscale(tight=True)
        self.filePointer = 0
        topFrame = tk.Frame(self)
        topFrame.pack()

        button1 = ttk.Button(topFrame, text=LOAD_BTN_TEXT,
                             command=lambda: self.onLoadImages())
        button2 = ttk.Button(topFrame, text=PREV_BTN_TEXT,
                             command=lambda: self.onPrevious())
        button3 = ttk.Button(topFrame, text=NEXT_BTN_TEXT,
                             command=lambda: self.onNext())

        button2.pack(side=tk.LEFT)
        button1.pack(side=tk.LEFT)
        button3.pack(side=tk.LEFT)

        if len(self.filenames) != 0:
            self.img = mpimg.imread(self.filenames[0])
            self.a.imshow(self.img)

        self.agg = FigureCanvasTkAgg(self.f, self)
        self.agg.mpl_connect(BTNPRESS_EVENT_NAME, self.on_click)
        self.agg.mpl_connect(KEYPRESS_EVENT_NAME, self.on_undo)
        self.agg.mpl_connect(MOUSEMOVE_EVENT_NAME, self.on_move)
        self.agg.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.agg, self)
        toolbar.update()
        self.agg._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.agg._tkcanvas.focus_force()
        print(self.focus_displayof())

    def on_click(self, event):
        """
        The click handler for the matplotlib canvas element
        """
        self.agg._tkcanvas.focus_force()  # needed to enable keypress detection
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
                                              self.clicked_points[1][1] - self.clicked_points[0][1], edgecolor=RECT_EDGE_COLOR,
                                              facecolor=RECT_FACE_COLOR, linewidth=LINE_WIDTH)
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
                    [event.xdata], [event.ydata], c=RECT_EDGE_COLOR, s=POINT_SIZE)
                self._refreshImage()
                self.agg.draw()

    def on_move(self, event):

        if self.click_count != 1:
            return

        if self.temp_rect is not None:
            self.temp_rect.remove()
            self.temp_rect = None

        self.temp_rect = patches.Rectangle(tuple(
            self.clicked_points[0]),
            event.xdata-self.clicked_points[0][0],
            event.ydata-self.clicked_points[0][1],
            facecolor=RECT_FACE_COLOR,
            edgecolor=RECT_EDGE_COLOR,
            linewidth=LINE_WIDTH)

        self.a.add_patch(self.temp_rect)
        self.agg.draw()

    def on_undo(self, event):
        sys.stdin.flush()
        print(event.key)

        if event.key == KEYCODE_ESCAPE:

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
        for root, directories, files in os.walk(os.path.join(os.path.dirname(sys.argv[0]), IMAGE_DIR)):
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
            try:
                with open('data.json', "r") as dataFile:
                    data = dataFile.read()
                    if data is not None and data != '':
                        jsonData = json.loads(data)
                        self.image_points = copy.deepcopy(
                            {**jsonData, **self.image_points})
                with open('data.json', 'w') as dataFile:
                    dataFile.write(json.dumps(self.image_points))
            except FileNotFoundError:
                with open('data.json', 'w') as dataFile:
                    dataFile.write(json.dumps(self.image_points))

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


app = DataLabeler()

app.mainloop()
