import matplotlib


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.image as mpimg
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
        tk.Tk.wm_title(self, "Sea of BTC client")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(PageThree)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(PageThree))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()






class PageThree(tk.Frame):
    def onclick(self,event):
        print(event.x, event.y, event.xdata, event.ydata)

    def onSelectImages(self):
        self.filenames = filedialog.askopenfilenames(initialdir="/", title="Select file",
                                                         filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        if self.filenames is not None:
            img = mpimg.imread(self.filenames[0])
            self.a.imshow(img)
            self.agg.draw()

    def onPrevious(self):
        pass

    def onNext(self):
        pass


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Labeling UI", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.filenames = None
        f = Figure(figsize=(10, 10), dpi=200)
        self.a = f.add_subplot(111)

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


        if self.filenames is not None:
            img = mpimg.imread(self.filenames[0])
            self.a.imshow(img)

        self.agg = FigureCanvasTkAgg(f, self)
        self.agg.mpl_connect('button_press_event', self.onclick)
        self.agg.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.agg, self)
        toolbar.update()
        self.agg._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = SeaofBTCapp()

app.mainloop()




