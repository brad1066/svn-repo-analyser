import os
import subprocess
from tkinter import *
from tkinter import filedialog as fd, messagebox as mb
from datetime import datetime
from XMLInterpreter import XMLInterpreter as XMLI
from CommitLog import CommitLog
from Statistics import FileGrowthGraphApp
from Authors import AuthorStatisticsApp
import numpy as np
import matplotlib.pyplot as plt
from CommitLog import CommitLog
from statistics import mean, stdev
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SVNAnalyserApp(Tk):
    """A class to hold the window data and the UI frames"""
    def __init__(self, *args, **kwargs):
        """The constructor for the TitanicTk Class"""
        # Initialise the object as a Tk, add style options from a file
        Tk.__init__(self, *args, **kwargs)
        if (os.path.exists("style.db")):
            self.option_readfile("style.db")
        self.GLOBAL_DATA = {}

        # Create the container for the content frames and configure it's layout. Fill the window with the container
        self.container = Frame(self)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack(side=TOP, fill=BOTH, expand=True)

        # Create a dictionary to store generated content frames, to make them easily swappable
        self.frames = {}

        # Set the size of the window, and make it not resizable
        self.title("SVN Analyser")
        self.geometry("900x500")
        # self.resizable(0, 0)
        self.loadFrame(StartPage)

    def loadFrame(self, frame):
        """A method to allow the creation and/or loading of stored frames based on the name of the frame"""

        # If the frame has not been loaded in before...
        if frame.__name__ not in self.frames.keys():
            # Create the frame, store it using the name of it's class, and place it into the layout
            self.frames[frame.__name__] = frame(self.container, self)
            self.frames[frame.__name__].grid(row=0, column=0, sticky=NSEW)

        # Bring the frame to the forefront of the window
        self.frames[frame.__name__].tkraise()
        
        
    
    def attemptGetLogs(self):
        # Error handle for lack of directories inputted via svn/ xml buttons
        if ('XMLExportPath' not in self.GLOBAL_DATA or 'SVNRoot' not in self.GLOBAL_DATA):
            return
        # Timestamp and export path for all outputs
        timestamp = datetime.today().strftime("%Y_%m_%d-%H_%M_%S")
        xmlExportPath = self.GLOBAL_DATA['XMLExportPath']
        xmlExportPath = os.path.join(xmlExportPath, f"log-{timestamp}.xml")

        # Open a file to export the output from the svn call
        with open(xmlExportPath, 'w') as logOutput:
            # If SVN log fails, close the file, remove it and exit program with a message
            subprocess.call("svn update", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)
            if (subprocess.call("svn log --xml", stdout=logOutput, stderr=subprocess.STDOUT, shell=True) != 0):
                logOutput.close()
                if (os.path.exists(xmlExportPath)):
                    os.remove(xmlExportPath)
                print("There was an error when attempting an export of the logs. Please try again.\nExiting program")
                return
        interpretor = XMLI(xmlExportPath)
        logsDict = interpretor.getDictionary(interpretor.root)
        self.GLOBAL_DATA['CommitLog'] = CommitLog(logsDict['log']['logentry'])
        
        # New frame loaded once Logs committed to illustrate logs
        self.loadFrame(LogsDetailsPage)

    def attemptGetGrowth(self):
        FileGrowthGraphApp(style_db="trunk/style.db", data=self.GLOBAL_DATA).mainloop()
    
    def attemptGetAuthorPage(self):
        AuthorStatisticsApp(style_db="trunk/style.db", data=self.GLOBAL_DATA).mainloop()



"""" Main Init frame to retrieve root & XML directory """
class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent, self.controller = parent, controller
        
        self.grid_columnconfigure(1, weight=1)

        # tkinter button / label inputs. Upon button press functions are ran to parse data corrently
        self.getRootButton = Button(self, text = "Select the SVN root directory", command = self.selectSVNRepo)
        self.rootPathLabel = Label(self, text="", fg="red")
        self.getXMLButton = Button(self, text = "Select the XML export directory", command = self.selectXMLExportPath)
        self.xmlPathLabel = Label(self, text="", fg="red")

        self.getRootButton.grid(row=0, column=0, sticky=EW)
        self.rootPathLabel.grid(row=0, column=1, sticky=EW)
        self.getXMLButton.grid(row=1, column=0, sticky=EW)
        self.xmlPathLabel.grid(row=1, column=1, sticky=EW)
        Button(self, text="Get Logs", command=self.controller.attemptGetLogs).grid(row=2, column=0, columnspan=2, sticky=EW)

    def selectSVNRepo(self):
        path = fd.askdirectory()
        if (not os.path.isdir(path)):
            self.rootPathLabel.config(text = f"No directory found at '{path}'", fg="red")
            return
    
        # Check if in an SVN repository. If not, continue to next iteration with suitable error
        if (subprocess.call("svn list", cwd=path, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True) != 0):
            self.rootPathLabel.config(text = f"No SVN repository found at '{path}'", fg="red")
            return

        # Move up the directory hierarchy until at the root of the repository
        while (subprocess.call("svn list", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True) == 0):
            path = os.getcwd()
            os.chdir("..")
            
        os.chdir(path)

        self.rootPathLabel.config(text = f"Root at '{path}'", fg="green")
        self.controller.GLOBAL_DATA['SVNRoot'] = path
        
    def selectXMLExportPath(self):
        # directory selection dialog is opened, error handled.
        path = fd.askdirectory()
        if (not os.path.isdir(path)):
            self.xmlPathLabel.config(text = f"No directory found at '{path}'", fg="red")
            return
        # if valid path change label text colour to indicate valid
        self.xmlPathLabel.config(text = f"Export XML to '{path}'", fg="green")
        # dictionary updated
        self.controller.GLOBAL_DATA['XMLExportPath'] = path

class LogsDetailsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.parent, self.controller = parent, controller

        self.updateCommitStatistics()

        # self.controller.geometry("720x480")
        self.grid_rowconfigure(0,weight = 1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)

        self.graphFrame = Frame(self)
        self.infoFrame = Frame(self)
        self.actionButtonsFrame = Frame(self)

        self.totalCommitsLabel = Label(self.infoFrame, text=f"Total number of commits: {self.totalCommits}")
        self.totalDriversLabel = Label(self.infoFrame, text=f"Total Drivers {self.totalDrivers}")
        self.totalNavigatorsLabel = Label(self.infoFrame, text=f"Total Navigators {self.totalNavigators}")
        self.AvgCommitRatingLabel = Label(self.infoFrame, text=f"Average commit rating {self.avgCommitRating:.2f}")
        self.percentPairProgrammedLabel = Label(self.infoFrame, text=f"Percentage of Pair programming {self.percentPairProgrammed:.2f}%")

        self.totalCommitsLabel.pack(side=TOP, fill=X, expand=1)
        self.totalDriversLabel.pack(side=TOP, fill=X, expand=1)
        self.totalNavigatorsLabel.pack(side=TOP, fill=X, expand=1)
        self.AvgCommitRatingLabel.pack(side=TOP, fill=X, expand=1)
        self.percentPairProgrammedLabel.pack(side=TOP, fill=X, expand=1)

        Button(self.actionButtonsFrame, text="Refresh", command=self.refreshLogs).pack(side=TOP, fill=X, expand=1, pady=(5, 0))
        Button(self.actionButtonsFrame, text="Save Image", command=self.saveImage).pack(side=TOP, fill=X, expand=1, pady=(5, 0))
        Button(self.actionButtonsFrame, text="Show Code Growth", command=self.showCodeGrowth).pack(side=TOP, fill=X, expand=1, pady=(5, 0))
        Button(self.actionButtonsFrame, text="Show Author Stats", command=self.showAuthorStats).pack(side=TOP, fill=X, expand=1, pady=(5, 0))
        Button(self.actionButtonsFrame, text="Go back", command=lambda: self.controller.loadFrame(StartPage)).pack(side=TOP, fill=X, expand=1, pady=(5, 0))


        self.graphFrame.grid(row=0, column=0, rowspan=2, sticky=NSEW)
        # info frame for stats
        self.infoFrame.grid(row=0, column=1, sticky=EW)
        self.actionButtonsFrame.grid(row=1, column=1, sticky=EW)

        self.createGraph()


    def updateCommitStatistics(self):
        commitRatings = self.controller.GLOBAL_DATA['CommitLog'].getCommitRatings()

        # These are the datapoints which will be expressed
        self.totalCommits = len(self.controller.GLOBAL_DATA['CommitLog'].commits)
        self.totalDrivers = len(self.controller.GLOBAL_DATA['CommitLog'].getDriverCommitsByName())
        self.totalNavigators= len(self.controller.GLOBAL_DATA['CommitLog'].getNavigatorCommitsByName())
        self.avgCommitRating = sum([rating for rating in commitRatings.values()])/self.totalCommits
        self.percentPairProgrammed = (len(self.controller.GLOBAL_DATA['CommitLog'].getPairProgrammedCommits()) / self.totalCommits)*100
        
    
    # Empty graph canvas, only a base for where 'refreshGraph' method is used to both initialise values after creation and to update

    def createGraph(self):
        # Create a Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphFrame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        self.refreshGraph()

    # Plots the data to the created graph
    def refreshGraph(self):
        self.ax.clear()
        # rates each commit from commit.py and commitlog.py, rating message by len of message + use of drivers/navigators
        commitRatings = self.controller.GLOBAL_DATA['CommitLog'].getCommitRatings()
        x = np.array([int(revision) for revision in commitRatings.keys()])
        y = np.array([int(rating) for rating in commitRatings.values()])
        yTrend = np.polyfit(x, y, 1)
        p = np.poly1d(yTrend)
        
        self.ax.set(xlabel='Revision Number', ylabel='Commit Rating', title='Repository Commit Ratings')

        # red indicates the rating of each commit & blue the trend of commits ratings
        self.ax.plot(x,y, color='red')
        self.ax.plot(x,p(x), color='blue')

        # Draw the new plot
        self.canvas.draw()

    # will re draw graph & update if new logs emmerge
    def refreshLogs(self):
        self.controller.attemptGetLogs()
        self.refreshGraph()
        print("Refreshing Logs")

    # New method
    def showCodeGrowth(self):
        self.controller.attemptGetGrowth()
    
    def showAuthorStats(self):
        self.controller.attemptGetAuthorPage()

    def saveImage(self):
        # Prompt user to choose a file for saving the image
        file_path = fd.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

        if file_path:
            # Save the current figure as an image
            self.fig.savefig(file_path)
            mb.showinfo("Saved", f"Image saved to {file_path}")

        

if __name__ == "__main__":
    if (subprocess.call("svn --version", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True) != 0):
        print("Subversion might not be installed (or on PATH). Please check, and try again")
        exit(0)
        
    app = SVNAnalyserApp()
    app.mainloop()