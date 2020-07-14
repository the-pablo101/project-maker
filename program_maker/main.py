from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as filedialog
import pathlib
from os import walk
from os import path as osPath

class program(Tk):
    def __init__(self,*args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("500x500")
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        self.tabs = {}
        self.fileDict = {}
        self.renderDirectoryFiles()
        self.tabEntities = {}
        self._createMenu()
    def _createMenu(self):
        self.menu = Menu(self)
        self.config(menu=self.menu)

        fileMenu = Menu(self.menu)
        fileMenu.add_command(label="open folder", command=self.renderDirectoryFiles)
        fileMenu.add_command(label="Exit", command=self.quit)
        self.menu.add_cascade(label="File", menu=fileMenu)

        editMenu = Menu(self.menu)
        editMenu.add_command(label="Undo")
        editMenu.add_command(label="Redo")
        self.menu.add_cascade(label="Edit", menu=editMenu)
    def renderDirectoryFiles(self):
        self.tabParent.destroy()
        self.fileFrame.destroy()
        
        self.tabParent = Notebook(self)
        self.fileFrame = Frame(self)
        self.fileFrame.pack(side=LEFT, anchor=NE)
        self.tabParent.pack(side=LEFT, fill=BOTH, expand=1)
        self.tabEntities = {}
        self.dirPath = self.openFileDialog()
        folderTabData = self.breakPaths(self.dirPath)
        self.fileDict = folderTabData
        self.fileFrameEntities = self.renderBlock(self.fileFrame, self.fileDict)
    def renderBlock(self, parent, fileDict):
        index = 0
        output = {}
        keys = list(fileDict.keys())
        for key in keys:
            if key == 'files':
                output[key] = list()
                for file in fileDict['files']:
                    tempButton = Button(parent, text= file, command=lambda path=fileDict['dir'], f=file: self.addTab(path, f))
                    output[key].append(tempButton)
                    index+=1
                    tempButton.grid(row=index+1, sticky=W, padx=(10,))
            elif key == 'dir':
                pass  
            else:
                temp =  {}
                temp['frameParent'] = Frame(parent)
                temp['self'] = Button(parent, text=key, command=lambda frame=temp['frameParent'], i=index: self.activate(frame, i))
                if parent != self.fileFrame:
                    temp['self'].grid(row=index, sticky=W, padx=(10,))
                else:
                    temp['self'].grid(row=index, sticky=W)

                index+=2
                temp.update(self.renderBlock(temp['frameParent'], fileDict[key]))
                
                output = temp

        return output
    def activate(self, frame, index):
        if frame.winfo_ismapped() == 0:
            frame.grid(row=index+1)
        else:
            frame.grid_forget()

    
    def breakPaths(self, path):
        output = {}
        for (p, dirs, files) in walk(path):
            for e in dirs:
                output[e] = self.breakPaths(str(path) + '/' + e)
            output['dir'] = p
            output['files'] = files
            break
        return output
    def addTab(self,path, name):
        filePath = osPath.join(path, name)
        self.tabEntities[filePath] = {}
        tabFrame = Frame(self.tabParent)
        self.tabEntities[filePath]['self'] = tabFrame
        self.tabParent.add(tabFrame, text=name)
        self.tabEntities[filePath]['text'] = Text(tabFrame, tabs=('8m',))
        self.tabEntities[filePath]['text'].pack(fill=BOTH, expand=1)
        self.tabEntities[filePath]['save'] = Button(tabFrame, text="save", command=lambda p=filePath: self.saveFile(p))
        self.tabEntities[filePath]['save'].pack()
        with open(filePath, "r") as func:
            try:
                text = func.readlines()
                for line in text:
                    self.tabEntities[filePath]['text'].insert(END, line)
            except UnicodeDecodeError:
                self.tabEntities[name]['text'].insert(END, "can't open this file")
    def saveFile(self, filePath):
        #wText is the text widget
        text = self.tabEntities[filePath]['text'].get('1.0', END)
        with open(filePath, "w+") as f:
            f.write(text)
            f.close()
    def createTkinterProject(self):
        print("jello world")
    def openFileDialog(self):
        folderPath = filedialog.askdirectory(title="open folder")
        return folderPath

test = program()




test.mainloop()