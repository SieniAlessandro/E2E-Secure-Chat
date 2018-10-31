import tkinter as tk
from tkinter import ttk

class Scrollable(ttk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, background, width=16):
        self.scrollbar = tk.Scrollbar(frame, width=width)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, bd = 0, bg=background, yscrollcommand=self.scrollbar.set,  highlightbackground="red", highlightcolor="red", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar.config(command=self.canvas.yview, background=background)

        self.canvas.bind('<Configure>', self.__fill_canvas)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        # base class initialization
        tk.Frame.__init__(self, frame, bg=background)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)
    def setCanvasWidth(self, width):
        self.canvas.configure(width=width)
    def _on_mousewheel(self, event):
        (lo, hi) = self.scrollbar.get()
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            return
        if event.delta < 0:
            self.canvas.yview_scroll(1, "unit")
        elif event.delta > 0:
            self.canvas.yview_scroll(-1, "unit")
    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)
    def update(self):
        "Update the canvas and the scrollregion"
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
