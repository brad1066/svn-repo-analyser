import os
from tkinter import *
from tkinter import ttk, messagebox as mb, filedialog as fd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from Codebase import Codebase

class FileGrowthGraphApp(Tk):

    svnPath = None

    def __init__(self, *args, **kwargs):
        styleDbPath = kwargs['style_db'] if "style_db" in kwargs else None
        if styleDbPath: del kwargs['style_db']

        self.GLOBAL_DATA = kwargs['data'] if "data" in kwargs else {}
        if self.GLOBAL_DATA: del kwargs['data']
        
        Tk.__init__(self, *args, **kwargs)

        if (os.path.exists(styleDbPath or "style.db")):
            self.option_readfile(styleDbPath)

        self.dropdownFrame = Frame(self)
        self.graphFrame = Frame(self)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.dropdownFrame.grid_columnconfigure(0, weight=1)

        # Create a Combobox for file selection
        self.fileComboxbox = ttk.Combobox(self.dropdownFrame, values=self.getFileList(), width=50)
        self.fileComboxbox.set("Select a file")
        self.fileComboxbox.grid(row=0, column=0, pady=10, padx=10)

        # Create a button to generate the graph
        Button(self.dropdownFrame, text="Generate Graph", command=self.generateGraph).grid(row=0, column=1, pady=10, padx=10)

        # Save Button
        Button(self, text="Save Image", command=self.saveImage).grid(row=2, column=1, pady=10, padx=10)

        # Create a Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # Pack frames
        self.dropdownFrame.grid(row=0, column=0, columnspan=2, sticky=EW, padx=10, pady=10)
        self.graphFrame.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5)

    def getFileList(self):
        if "SVNRoot" in self.GLOBAL_DATA:
            root_directory = self.GLOBAL_DATA['SVNRoot']
        else:
            root_directory = findRootSVN(os.getcwd())

        if root_directory is None:
            ("Error: Could not find SVN root directory.")
            return []

        files = []
        repoFiles = runCommand(["svn", "list", "-R", root_directory])[0].split("\n")
        for fileName in repoFiles:
            fileName = fileName.strip("\r")
            if os.path.isfile(os.path.join(root_directory, fileName)):
                files.append(fileName)

        return files

    def generateGraph(self):
        selectedFile = self.fileComboxbox.get()
        if selectedFile == "Select a file":
            return

        selectedFile = os.path.join(findRootSVN(os.getcwd()), selectedFile.strip("\r"))

        fileOccurrences = Codebase.getFileGrowth(selectedFile)

        revisions = sorted(map(int, fileOccurrences.keys()))

        counts = [sum(data.values()) for data in fileOccurrences.values()]

        cumulativeCounts = np.cumsum(counts)

        # Clear previous plot
        self.ax.clear()

        self.ax.plot(revisions, cumulativeCounts, marker='o')
        self.ax.set(xlabel='Revision Number', ylabel='Total code growth', title='Code Growth depiction')

        self.canvas.draw()

    def saveImage(self):
        # Prompt user to choose a file for saving the image
        filePath = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if filePath:
            # Save the current figure as an image
            self.fig.savefig(filePath)
            mb.showinfo("Saved", f"Image saved to {filePath}")

if __name__ == "__main__":
    app = Tk()
    FileGrowthGraphApp(app).pack(side="top", fill="both", expand=True)
    app.mainloop()
