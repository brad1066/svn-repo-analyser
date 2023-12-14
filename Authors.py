import os
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from utils import *
from Anonymiser import Anonymiser
from utils import runCommand

class AuthorStatisticsApp(Tk):

    def __init__(self, *args, **kwargs):
        styleDbPath = kwargs['style_db'] if "style_db" in kwargs else None
        self.GLOBAL_DATA = kwargs['data'] if "data" in kwargs else {}

        if styleDbPath: del kwargs['style_db']
        if self.GLOBAL_DATA: del kwargs['data']

        Tk.__init__(self, *args, **kwargs)
        
        if (os.path.exists(styleDbPath or "style.db")):
            self.option_readfile(styleDbPath)
        
        if "CommitLog" in self.GLOBAL_DATA:
            self.commitLog = self.GLOBAL_DATA["CommitLog"]
        self.anonymiser = Anonymiser(self.commitLog)

        
        self.dropdownFrame = Frame(self)
        self.graphFrame = Frame(self)
        self.statisticsFrame = Frame(self)

        # Create checkbox to assert wether user wants to look at anonymous users, or just users
        self.anonymousCheckbox = ttk.Checkbutton(self.dropdownFrame, text="Anonymity", command=self.resetComboboxValue)
        self.anonymousCheckbox.grid(row=0, column=2, padx=10, pady=10)
        self.anonymousCheckbox.state(['!alternate'])
        self.anonymousCheckbox.state(['selected'])
        
        # Create a combobox (dropdown box) for list of users / anonymised users 
        self.authorCombobox = ttk.Combobox(self.dropdownFrame, values=self.anonymiser.getAnonymisedUsers(), postcommand=self.updateAuthorsByState, width=30)
        
        Button(self.dropdownFrame, text="Generate Statistics", command=self.generateStatistics).grid(row=0, column=1, pady=10, padx=10)

        self.updateAuthorsByState()        

        self.authorCombobox.set("Select a user")
        self.authorCombobox.grid(row=0, column=0, pady=10, padx=10)


        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.dropdownFrame.grid_columnconfigure(0, weight=1)

        # Create statistics labels
        self.totalParticipationsLabel = Label(self.statisticsFrame, text=f"Total commits participated in: ")
        self.participationsDriven = Label(self.statisticsFrame, text=f"Commits Driven:")
        self.participationsNavigated = Label(self.statisticsFrame, text=f"Commits Navigated:")
        self.averageCommitScore = Label(self.statisticsFrame, text=f"Average Commit Score:")

        self.totalParticipationsLabel.pack(side=TOP, fill=X, expand=1)
        self.participationsDriven.pack(side=TOP, fill=X, expand=1)
        self.participationsNavigated.pack(side=TOP, fill=X, expand=1)
        self.averageCommitScore.pack(side=TOP, fill=X, expand=1)

        # Create Matplotlib figures and canvases
        self.driverFig, self.driverAx = plt.subplots()
        self.driverCanvas = FigureCanvasTkAgg(self.driverFig, master=self.graphFrame)
        self.driverCanvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=1)
        
        self.navigatorFig, self.navigatorAx = plt.subplots()
        self.navigatorCanvas = FigureCanvasTkAgg(self.navigatorFig, master=self.graphFrame)
        self.navigatorCanvas.get_tk_widget().pack(side=RIGHT, fill=BOTH, expand=1)


        # Pack frames
        self.dropdownFrame.grid(row=0, column=0, sticky=N, padx=10, pady=10)
        self.graphFrame.grid(row=1,column=0, padx=10, pady=10)
        self.statisticsFrame.grid(row=2, column=0, sticky=S, padx=5, pady=5)

    def updateAuthorsByState(self):
        if self.anonymousCheckbox.instate(['selected']):
            self.authorCombobox['values'] = self.anonymiser.getAnonymisedUsers()
        elif self.anonymousCheckbox.instate(['!selected']):
            self.authorCombobox['values'] = self.anonymiser.getUsers()

    def resetComboboxValue(self):
        self.authorCombobox.set("Select a user")

    def generateStatistics(self):
        # Generate graphs
        self.generateGraphs()

        # Generate statistics
        userAnonymous = self.anonymousCheckbox.instate(['selected'])
        if userAnonymous:
            user = self.anonymiser.unanonymiseUser(self.authorCombobox.get())
        else:
            user = self.authorCombobox.get()
        if user == False:
            return

        commitCounter = 0
        commitsDriven = 0
        commitsParticipated = 0
        commitsNavigated = 0
        cumulativeRating = 0
        for commit in self.commitLog.commits:
            commitCounter+=1
            if user == commit.getDriver():
                commitsDriven += 1
            if user in commit.getNavigators():
                commitsNavigated += 1
            if user in commit.participants:
                commitsParticipated += 1
                cumulativeRating += commit.getRating()
            

        # Update labels
        self.totalParticipationsLabel.config(text=f"Total commits participated in: {commitsParticipated} ({round((commitsParticipated/commitCounter) * 100, 2)} %) ")
        self.participationsDriven.config(text=f"Commits Driven: {commitsDriven} ({round((commitsDriven/commitsParticipated) * 100, 2)} %)")
        self.participationsNavigated.config(text=f"Commits Navigated: {commitsNavigated} ({round((commitsNavigated/commitsParticipated) * 100, 2)} %)")
        self.averageCommitScore.config(text=f"Average Commit Score: {round(cumulativeRating/commitsParticipated, 2)}")

    def generateGraphs(self):
        # Clear the graph
        self.driverAx.clear()
        self.navigatorAx.clear()

        # First we get the person selected
        userAnonymous = self.anonymousCheckbox.instate(['selected'])
        if userAnonymous:
            user = self.anonymiser.unanonymiseUser(self.authorCombobox.get())
        else:
            user = self.authorCombobox.get()
        if user == False:
            return

        # get list of revisions driven by that user
        commits = self.commitLog.getCommitsByDriver(user)
        committed_revisions = []
        for commit in commits:
            committed_revisions.append(commit.revision)
        
        # Create an list of tuples containing (<int> additions,<int> deletions)
        additionsDeletionsList = []
        
        for commit in committed_revisions:
            revString = f"{int(commit)-1}:{commit}"
            response, error = runCommand(["svn", "diff", "-r", revString])
            if error != "":
                return
            additionsDeletionsList.append(self.getAdditionsAndDeletions(response))
        
        # Reverse these lists (x,y data) for better display (chronological)
        committed_revisions.reverse()
        additionsDeletionsList.reverse()
        
        additions, deletions = [], []
        if (len(additionsDeletionsList) > 0):
            additions, deletions = zip(*additionsDeletionsList)

        barWidth = 0.35

        barPositionsAdditions = np.arange(len(committed_revisions))     
        barPositionsDeletions = barPositionsAdditions + barWidth

        self.driverAx.bar(barPositionsAdditions, additions, width=barWidth, label="Additions")
        self.driverAx.bar(barPositionsDeletions, deletions, width=barWidth, label="Deletions")
        if userAnonymous:
            self.driverAx.set(xlabel="Revision Number", ylabel="Lines of code", title=f"Code changes by {self.anonymiser.anonymiseUser(user)} as a driver")    
        else:
            self.driverAx.set(xlabel="Revision Number", ylabel="Lines of code", title=f"Code changes by {user} as driver")
        self.driverAx.set_xticks(barPositionsAdditions + barWidth / 2, committed_revisions)
        self.driverAx.legend()

        self.driverCanvas.draw()

        ## NAVIGATORS

        # get list of revisions driven by that user
        commits = self.commitLog.getCommitsByNavigator(user)
        committed_revisions = []
        for commit in commits:
            committed_revisions.append(commit.revision)
        

        additionsDeletionsList = []
        
        for commit in committed_revisions:
            revString = f"{int(commit)-1}:{commit}"
            response, error = runCommand(["svn", "diff", "-r", revString])
            if error != "":
                return
            additionsDeletionsList.append(self.getAdditionsAndDeletions(response))
        
        committed_revisions.reverse()
        additionsDeletionsList.reverse()

        additions, deletions = [], []
        if (len(additionsDeletionsList) > 0):
            additions, deletions = zip(*additionsDeletionsList)

        barWidth = 0.35

        barPositionsAdditions = np.arange(len(committed_revisions))     
        barPositionsDeletions = barPositionsAdditions + barWidth

        self.navigatorAx.bar(barPositionsAdditions, additions, width=barWidth, label="Additions")
        self.navigatorAx.bar(barPositionsDeletions, deletions, width=barWidth, label="Deletions")
        if userAnonymous:
            self.navigatorAx.set(xlabel="Revision Number", ylabel="Lines of code", title=f"Code changes by {self.anonymiser.anonymiseUser(user)} as a navigator")    
        else:
            self.navigatorAx.set(xlabel="Revision Number", ylabel="Lines of code", title=f"Code changes by {user} as a navigator")
        self.navigatorAx.set_xticks(barPositionsAdditions + barWidth / 2, committed_revisions)
        self.navigatorAx.legend()

        self.navigatorCanvas.draw()
    
    def getAdditionsAndDeletions(self, string): # Function to take in a svn diff string and return a counter for additions and deletions
        myList = string.split("\r\n")
        additions = 0
        deletions = 0
        for item in myList:
            if len(item) == 1:
                if item == "+":
                    additions += 1
                elif item == "-":
                    deletions += 1
            elif item == "":
                pass
            else:
                if item[0] == '+' and item[1] != '+':
                    additions += 1
                elif item[0] == '-' and item[1] != '-':
                    deletions += 1
            
        return additions, deletions