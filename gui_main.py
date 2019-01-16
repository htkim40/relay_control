import Tkinter


NUMBER_OF_CHANNELS = 8
class relayArrayGUI:
    def __init__(self,master):


        self.master = master
        self.master.title("Power Cycling Test UI")
        self.label = Tkinter.Label(master,text="Power cycling test UI")
        #self.label.pack()

        self.leftFrame = Tkinter.Frame(master)
        #self.leftFrame.pack(side = Tkinter.LEFT)

        self.bottomFrame = Tkinter.Frame(master)
        #self.bottomFrame.pack(side = Tkinter.BOTTOM)

        self.startChButton_1 = Tkinter.Button(self.leftFrame,text="CH1 Start")
        #self.startChButton_1.pack(side = Tkinter.LEFT)

        self.startAllChButton = Tkinter.Button(self.bottomFrame,text="Start All Channels")
        #self.startAllChButton.pack(side = Tkinter.BOTTOM)

        self.enableChButtonStates = [True,True,True,True,True,True,True,True]
        self.enableChButtonVars = []
        for i in range (0,NUMBER_OF_CHANNELS):
            self.enableChButtonVars.append(Tkinter.IntVar())
            self.enableChButtonVars[i].set(i+1)

            print "Initializing ch " + str(i+1)

            Tkinter.Label(self.master,text = "Ch " + str(i+1)).place(y = 10+i*30, x = 15)

            Tkinter.Checkbutton(self.master, \
                                      #text="Ch " + str(i+1),\
                                      variable=self.enableChButtonVars[i],\
                                      onvalue = i+1,\
                                      offvalue = -(i+1),\
                                      command = (lambda i = self.enableChButtonVars[i]: self.enableChButtonPress(i))\
                                      ).place(y = 10+i*30, x = 45)

    def enableChButtonPress(self,i):
        if i.get() <=0 :
            print "Disabling channel " + str(abs(i.get()))
        else:
            print "Enabling channel " + str(i.get())

    def start(self):
        print("Starting")





gui_root = Tkinter.Tk()
gui_main = relayArrayGUI(gui_root)
gui_root.mainloop()
