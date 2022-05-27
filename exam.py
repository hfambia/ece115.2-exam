from tkinter import *
from tkinter import ttk
import time

class StopWatch(Frame):                                                           
    def __init__(self, parent=None):        
        Frame.__init__(self, parent)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.laps = []
        self.timestr = StringVar()
        self.makeWidgets()
        self.prevLapHolder = 0
        self.lapcounter = 1
        self.avglap = []
        self.fastestlap = 99999999
        self.slowestlap = 0
        
    def makeWidgets(self):                         
        self.e = Entry(self)
        timerframe = LabelFrame(self)
        timerframe.pack(fill="both", pady=(25,0))
        timer = Label(timerframe, textvariable=self.timestr,font=('arial', 38, 'bold'))
        self._setTime(self._elapsedtime)
        timer.pack(anchor = N,pady=(0,0),side=TOP)
        extraframe = LabelFrame(self)
        extraframe.pack(fill="both")
        avgLap = Label(extraframe, text='Average lap time:')
        avgLap.grid(column=0,row=0,sticky=W)
        self.avgLapvalue = Label(extraframe, text="00:00:00")
        self.avgLapvalue.grid(column=1,row=0,sticky=E)
        fastLap = Label(extraframe, text='Fastest lap time:')
        fastLap.grid(column=0,row=1,sticky=W)
        self.fastLapvalue = Label(extraframe, text="00:00:00")
        self.fastLapvalue.grid(column=1,row=1,sticky=E)
        self.fastLapcount = Label(extraframe, text="(#0)")
        self.fastLapcount.grid(column=2,row=1,sticky=W)
        slowLap = Label(extraframe, text='Slowest lap time:')
        slowLap.grid(column=0,row=2,sticky=W)
        self.slowLapvalue = Label(extraframe, text="00:00:00")
        self.slowLapvalue.grid(column=1,row=2,sticky=E)
        self.slowLapcount = Label(extraframe, text="(#0)")
        self.slowLapcount.grid(column=2,row=2,sticky=W)      
        tree = ttk.Treeview(self)
        tree.pack(pady=(5,0))
        tree_scroll = Scrollbar(tree)
        tree_scroll.pack(side=RIGHT, fill=Y)
        self.treeall = ttk.Treeview(tree,yscrollcommand=tree_scroll.set, height=6)
        self.treeall.pack() 
        self.treeall['columns'] = ("#", "Lap Time", "Split Time")
        self.treeall.column("#0", width=0, stretch=NO)
        self.treeall.column("#", anchor=CENTER, width=30)
        self.treeall.column("Lap Time", anchor=CENTER, width=100)
        self.treeall.column("Split Time", anchor=CENTER, width=100)
        self.treeall.heading("0", text="", anchor=W)
        self.treeall.heading("#", text="#", anchor=CENTER)
        self.treeall.heading("Lap Time", text="Lap Time", anchor=CENTER)
        self.treeall.heading("Split Time", text="Split Time", anchor=CENTER)
        self.treeall.pack()
        
    def _update(self): 
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def _setLapTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d:%02d' % (minutes, seconds, hseconds)
    
    def Start(self):                                          
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1 

    def Stop(self):                                    
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self._setTime(self._elapsedtime)
            self._running = 0
         
    def Reset(self):
        self._start = time.time()         
        self._elapsedtime = 0.0
        self.prevLapHolder = 0
        self.lapcounter = 1
        self.avglap = []
        self.fastestlap = 99999999
        self.slowestlap = 0
        self.laps = []   
        self._setTime(self._elapsedtime)
        self.after_cancel(self._timer)            
        self._elapsedtime = 0.0
        self.treeall.delete(*self.treeall.get_children())
        self.avgLapvalue.config(text="00:00:00")
        self.fastLapvalue.config(text="00:00:00")
        self.fastLapcount.config(text="(#0)")
        self.slowLapvalue.config(text="00:00:00")
        self.slowLapcount.config(text="(#0)")
        self._running = 0
    
    def Lap(self):
       tempo = self._elapsedtime - self.prevLapHolder
       if self._running:
           self.avglap.append(tempo)
           self.avgLapvalue.config(text=(self._setLapTime((sum(self.avglap))/self.lapcounter)))
           if tempo < self.fastestlap:
               self.fastestlap = tempo
               self.fastLapvalue.config(text=self._setLapTime(tempo))
               self.fastLapcount.config(text=("(#" + str(self.lapcounter) + ")"))
           if tempo > self.slowestlap:
                self.slowestlap = tempo
                self.slowLapvalue.config(text=self._setLapTime(tempo))
                self.slowLapcount.config(text=("(#" + str(self.lapcounter) + ")"))
           self.laps.append(self._setLapTime(tempo))
           self.treeall.insert(parent='',index=0,text='', values=(self.lapcounter,self._setLapTime(tempo),self._setLapTime(self._elapsedtime)))
           self.lapcounter += 1
           self.prevLapHolder = self._elapsedtime
        
def main():
    root = Tk()
    root.title('Exam')
    root.geometry("300x380")
    root.resizable(False, False)
    root.wm_attributes("-topmost", 1)
    sw = StopWatch(root)
    sw.pack(side=TOP)
    Button(root, text='Lap',command=sw.Lap).pack(side=LEFT,fill=BOTH, expand=YES, anchor=S,padx=(25,2),pady=(5,25))
    Button(root, text='Stop',command=sw.Stop).pack(side=LEFT,fill=BOTH, expand=YES, anchor=S,padx=2,pady=(5,25))
    Button(root, text='Start',command=sw.Start).pack(side=LEFT,fill=BOTH, expand=YES, anchor=S,padx=2,pady=(5,25))
    Button(root, text='Reset', command=sw.Reset).pack(side=LEFT,fill=BOTH, expand=YES, anchor=S,padx=2,pady=(5,25))
    Button(root, text='Quit',command=root.destroy).pack(side=LEFT,fill=BOTH, expand=YES, anchor=S,padx=(2,25),pady=(5,25))
    root.mainloop()
    
if __name__ == '__main__':
    main()
