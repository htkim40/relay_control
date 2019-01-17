import tkinter

NUMBER_OF_CHANNELS = 8
OPTIONS_FRAME_OFFSET_X = 15
OPTIONS_FRAME_OFFSET_Y = 15

class relayArrayGUI:
    def __init__(self,master):

        self.master = master
        self.master.title("Power Cycling Test UI")
        self.label = tkinter.Label(master,text="Power cycling test UI")

        # set up the options pane
        self.testOptionFrame = tkinter.LabelFrame(self.master,text="Test Options").place(x=OPTIONS_FRAME_OFFSET_X,
                                                                                         y=OPTIONS_FRAME_OFFSET_Y,
                                                                                         width=420,
                                                                                         height=400)
        self.enableChButtonVars = []
        self.periodEntries = []
        self.dutyCycleEntries = []
        self.numOfCycleEntries= []
        self.chStartButtons = []
        self.chStopButtons = []

        for i in range(0, NUMBER_OF_CHANNELS):

            # set up enable checkboxes with labels
            self.enableChButtonVars.append(tkinter.IntVar())
            self.enableChButtonVars[i].set(i+1)

            tkinter.Label(self.testOptionFrame, text="Ch " + str(i)).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                                           x=OPTIONS_FRAME_OFFSET_X+15)
            tkinter.Checkbutton(self.testOptionFrame,
                                variable=self.enableChButtonVars[i],
                                onvalue=i+1,
                                offvalue=-(i+1),
                                command=(lambda i = self.enableChButtonVars[i]: self.enableChButtonPress(i))
                                ).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                        x=OPTIONS_FRAME_OFFSET_X+45)

            # set up period entry boxes
            self.periodEntries.append(tkinter.Entry(self.testOptionFrame).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                                                x=OPTIONS_FRAME_OFFSET_X+80,
                                                                                width=45))

            # set up duty cycle entry boxes
            self.dutyCycleEntries.append(tkinter.Entry(self.testOptionFrame).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                                                   x=OPTIONS_FRAME_OFFSET_X+150,
                                                                                   width=45))

            # set up number of cycles entry boxes
            self.numOfCycleEntries.append(tkinter.Entry(self.testOptionFrame).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                                                    x=OPTIONS_FRAME_OFFSET_X+220,
                                                                                    width=45))

            # set up the channel start buttons
            self.chStartButtons.append(tkinter.Button(self.testOptionFrame,
                                                      text="start",
                                                      # command =
                                                      ).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                              x=OPTIONS_FRAME_OFFSET_X+290))

            # set up the channel start buttons
            self.chStopButtons.append(tkinter.Button(self.testOptionFrame,
                                                      text="stop",
                                                      # command =
                                                      ).place(y=OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                                              x=OPTIONS_FRAME_OFFSET_X+350))

        self.allStartButton = tkinter.Button(self.testOptionFrame,
                                             text="Start All Channels",
                                             # command =
                                             ).place(y=OPTIONS_FRAME_OFFSET_Y+25+NUMBER_OF_CHANNELS*30,
                                                     x=OPTIONS_FRAME_OFFSET_X+15,
                                                     width=390)

        self.allStartButton = tkinter.Button(self.testOptionFrame,
                                             text="Stop All Channels",
                                             # command =
                                             ).place(y=OPTIONS_FRAME_OFFSET_Y+25+NUMBER_OF_CHANNELS*30+30,
                                                     x=OPTIONS_FRAME_OFFSET_X+15,
                                                     width=390)

        # set up the status pane
        self.statusFrame = tkinter.LabelFrame(self.master,text="Test Status").place(x=OPTIONS_FRAME_OFFSET_X+420,
                                                                                     y=OPTIONS_FRAME_OFFSET_Y,
                                                                                     width=400,
                                                                                     height=400)

    def enableChButtonPress(self,i):
        if i.get() <=0 :
            print("Disabling channel "+str(abs(i.get())-1))
        else:
            print("Enabling channel " + str(i.get()-1))

    def start(self):
        print("Starting")





gui_root = tkinter.Tk()
gui_main = relayArrayGUI(gui_root)
gui_root.mainloop()
