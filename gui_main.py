import tkinter
import gpiozero

NUMBER_OF_CHANNELS = 8
OPTIONS_FRAME_OFFSET_X = 15
OPTIONS_FRAME_OFFSET_Y = 15
OPTIONS_TO_STATUS_FRAME_OFFSET = 420
LABEL_OFFSET = 25
LABEL_TO_ELEMENT_OFFSET = 25
RELAY[0] = gpiozero.LED(2)  # j8p3
RELAY[1] = gpiozero.LED(3)  # j8p5
RELAY[2] = gpiozero.LED(4)  # j8p7
RELAY[3] = gpiozero.LED(17) # j8p11
RELAY[4] = gpiozero.LED(27) # j8p13
RELAY[5] = gpiozero.LED(22) # j8p15
RELAY[6] = gpiozero.LED(10) # j8p19
RELAY[7] = gpiozero.LED(9)  # j8p21


class RelayArrayGUI:

    def __init__(self, master):

        self.master = master
        self.master.title("Power Cycling Test UI")
        self.master.geometry("675x420")

        # set up the options pane
        self.testOptionFrame = tkinter.LabelFrame(self.master,
                                                  text="Test Options").place(x=OPTIONS_FRAME_OFFSET_X,
                                                                             y=OPTIONS_FRAME_OFFSET_Y,
                                                                             width=420,
                                                                             height=380)
        # set up enable label
        self.enableLabel = tkinter.StringVar()
        tkinter.Label(self.testOptionFrame,
                      textvariable=self.enableLabel).place(x=OPTIONS_FRAME_OFFSET_X + 15,
                                                           y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.enableLabel.set("Enable")

        # set up period label
        self.periodLabel = tkinter.StringVar()
        tkinter.Label(self.testOptionFrame,
                      textvariable=self.periodLabel).place(x=OPTIONS_FRAME_OFFSET_X + 75,
                                                           y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.periodLabel.set("Period(s)")

        # set up duty cycle label
        self.dutyCycleLabel = tkinter.StringVar()
        tkinter.Label(self.testOptionFrame,
                      textvariable=self.dutyCycleLabel).place(x=OPTIONS_FRAME_OFFSET_X + 130,
                                                              y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.dutyCycleLabel.set("Duty Cycle(%)")

        # set up number of cycles label
        self.noOfCyclesLabel = tkinter.StringVar()
        tkinter.Label(self.testOptionFrame,
                      textvariable=self.noOfCyclesLabel).place(x=OPTIONS_FRAME_OFFSET_X + 215,
                                                               y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.noOfCyclesLabel.set("No. of Cycles")

        # set up the status pane
        self.statusFrame = tkinter.LabelFrame(self.master,
                                              text="Test Status").place(x=OPTIONS_FRAME_OFFSET_X
                                                                          + OPTIONS_TO_STATUS_FRAME_OFFSET,
                                                                        y=OPTIONS_FRAME_OFFSET_Y,
                                                                        width=220,
                                                                        height=380)

        # set up on/off label
        self.onOffLabel = tkinter.StringVar()
        tkinter.Label(self.statusFrame,
                      textvariable=self.onOffLabel).place(x=OPTIONS_FRAME_OFFSET_X
                                                            + OPTIONS_TO_STATUS_FRAME_OFFSET + 15,
                                                          y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.onOffLabel.set("On/Off")

        # set up cycle count label
        self.cycleCountLabel = tkinter.StringVar()
        tkinter.Label(self.statusFrame,
                      textvariable=self.cycleCountLabel).place(x=OPTIONS_FRAME_OFFSET_X
                                                                 + OPTIONS_TO_STATUS_FRAME_OFFSET + 70,
                                                               y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.cycleCountLabel.set("Cycle Count")

        # set up test time label
        self.testTimeLabel = tkinter.StringVar()
        tkinter.Label(self.statusFrame,
                      textvariable=self.testTimeLabel).place(x=OPTIONS_FRAME_OFFSET_X
                                                               + OPTIONS_TO_STATUS_FRAME_OFFSET + 150,
                                                             y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.testTimeLabel.set("Test Time")

        self.enableChButtonVars = []
        self.periodEntries = []
        self.dutyCycleEntries = []
        self.numOfCycleEntries = []
        self.chStartButtons = []
        self.chStopButtons = []
        self.chStateEntries = []
        self.chCycleCountEntries = []
        self.chTestTimeEntries = []

        for i in range(0, NUMBER_OF_CHANNELS):

            # set up enable checkboxes with labels
            self.enableChButtonVars.append(tkinter.IntVar())
            self.enableChButtonVars[i].set(i+1)

            tkinter.Label(self.testOptionFrame,
                          text="Ch "+str(i)).place(y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y
                                                     + LABEL_TO_ELEMENT_OFFSET+i*30,
                                                   x=OPTIONS_FRAME_OFFSET_X+15)
            tkinter.Checkbutton(self.testOptionFrame,
                                variable=self.enableChButtonVars[i],
                                onvalue=i+1,
                                offvalue=-(i+1),
                                command=(lambda j=self.enableChButtonVars[i]: self.enable_ch_button_press(j))
                                ).place(y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y+25+i*30,
                                        x=OPTIONS_FRAME_OFFSET_X+45)

            # set up period entry boxes
            self.periodEntries.append(tkinter.StringVar())
            tkinter.Entry(self.testOptionFrame,
                          textvariable=self.periodEntries[i]).place(y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y
                                                                      + LABEL_TO_ELEMENT_OFFSET+i*30,
                                                                    x=OPTIONS_FRAME_OFFSET_X+80,
                                                                    width=45)

            # set up duty cycle entry boxes
            self.dutyCycleEntries.append(tkinter.StringVar())
            tkinter.Entry(self.testOptionFrame,
                          textvariable=self.dutyCycleEntries[i]).place(y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y
                                                                         + LABEL_TO_ELEMENT_OFFSET+i*30,
                                                                       x=OPTIONS_FRAME_OFFSET_X+150,
                                                                       width=45)

            # set up number of cycles entry boxes
            self.numOfCycleEntries.append(tkinter.StringVar())
            tkinter.Entry(self.testOptionFrame,
                          textvariable=self.numOfCycleEntries).place(y=LABEL_OFFSET +
                                                                       OPTIONS_FRAME_OFFSET_Y
                                                                       + LABEL_TO_ELEMENT_OFFSET+i*30,
                                                                     x=OPTIONS_FRAME_OFFSET_X+220,
                                                                     width=45)

            # set up the channel start buttons

            self.chStartButtons.append(tkinter.Button(self.testOptionFrame,
                                                      text="start",
                                                      command=(lambda j=self.enableChButtonVars[i]: self.start(j))))
            self.chStartButtons[i].place(y=OPTIONS_FRAME_OFFSET_Y+LABEL_OFFSET
                                           + LABEL_TO_ELEMENT_OFFSET+i*30,
                                         x=OPTIONS_FRAME_OFFSET_X+290)

            # set up the channel start buttons
            self.chStopButtons.append(tkinter.Button(self.testOptionFrame,
                                                     text="stop",
                                                     command=(lambda j=self.enableChButtonVars[i]: self.stop(j))))
            self.chStopButtons[i].place(y=OPTIONS_FRAME_OFFSET_Y+LABEL_OFFSET
                                          + LABEL_TO_ELEMENT_OFFSET+i*30,
                                        x=OPTIONS_FRAME_OFFSET_X+350)

            # set up on/off entry boxes
            self.chStateEntries.append(tkinter.StringVar())
            tkinter.Entry(self.statusFrame,
                          textvariable=self.chStateEntries[i],
                          bg="gray90").place(y=LABEL_OFFSET + OPTIONS_FRAME_OFFSET_Y
                                               + LABEL_TO_ELEMENT_OFFSET + i * 30,
                                             x=OPTIONS_FRAME_OFFSET_X
                                               + OPTIONS_TO_STATUS_FRAME_OFFSET + 15,
                                             width=45)

            self.chStateEntries[i].set("Off")

            # set cycle count entry boxes
            self.chCycleCountEntries.append(tkinter.StringVar())
            tkinter.Entry(self.statusFrame,
                          textvariable=self.chCycleCountEntries[i],
                          bg="gray90").place(y=LABEL_OFFSET + OPTIONS_FRAME_OFFSET_Y
                                               + LABEL_TO_ELEMENT_OFFSET + i * 30,
                                             x=OPTIONS_FRAME_OFFSET_X
                                               + OPTIONS_TO_STATUS_FRAME_OFFSET + 85,
                                             width=45)

            self.chCycleCountEntries[i].set("0")

            # set test time entry boxes
            self.chTestTimeEntries.append(tkinter.StringVar())
            tkinter.Entry(self.statusFrame,
                          textvariable=self.chTestTimeEntries[i],
                          bg="gray90").place(y=LABEL_OFFSET + OPTIONS_FRAME_OFFSET_Y
                                               + LABEL_TO_ELEMENT_OFFSET + i * 30,
                                             x=OPTIONS_FRAME_OFFSET_X
                                               + OPTIONS_TO_STATUS_FRAME_OFFSET + 155,
                                             width=45)

            self.chTestTimeEntries[i].set("0")

        self.allStartButton = tkinter.Button(self.testOptionFrame,
                                             text="Start All Channels",
                                             command=lambda: self.start_all())
        self.allStartButton.place(y=OPTIONS_FRAME_OFFSET_Y+LABEL_OFFSET+LABEL_TO_ELEMENT_OFFSET
                                    + NUMBER_OF_CHANNELS*30,
                                  x=OPTIONS_FRAME_OFFSET_X+15,
                                  width=390)

        self.allStopButton = tkinter.Button(self.testOptionFrame,
                                            text="Stop All Channels",
                                            command=lambda: self.stop_all())
        self.allStopButton.place(y=OPTIONS_FRAME_OFFSET_Y+LABEL_OFFSET+LABEL_TO_ELEMENT_OFFSET
                                   + NUMBER_OF_CHANNELS*30+30,
                                 x=OPTIONS_FRAME_OFFSET_X+15,
                                 width=390)

    def enable_ch_button_press(self, channel):
        ch = abs(channel.get())-1
        if channel.get() <= 0:
            self.stop(channel)
            print("Disabling channel %d"%ch)
            self.chStartButtons[ch].configure(state=tkinter.DISABLED)
            self.chStopButtons[ch].configure(state=tkinter.DISABLED)
        else:
            print("Enabling channel %d"%ch)
            self.chStartButtons[ch].configure(state=tkinter.NORMAL)
            self.chStopButtons[ch].configure(state=tkinter.NORMAL)

    def set_text(self, textHandle, text):
        textHandle.delete(0, tkinter.END)
        textHandle.insert(0, text)
        return

    def start(self, channel):
        ch = abs(channel.get()) - 1
        print("Starting channel %d" % ch)

    def start_all(self):
        startText = 'Starting channels: '
        for ch in range(NUMBER_OF_CHANNELS):
            if self.enableChButtonVars[ch].get() > 0:
                startText += "%d, " % (self.enableChButtonVars[ch].get()-1)
        print(startText[0:len(startText)-2])

    def stop(self, channel):
        ch = abs(channel.get()) - 1
        print("Stopping channel %d" % ch)

    def stop_all(self):
        stopText = 'Stopping channels: '
        for ch in range(NUMBER_OF_CHANNELS):
            if self.enableChButtonVars[ch].get() > 0:
                stopText += "%d, " % (self.enableChButtonVars[ch].get() - 1)
        print(stopText[0:len(stopText) - 2])


def main():
    gui_root = tkinter.Tk()
    gui_main = RelayArrayGUI(gui_root)
    gui_main.master.mainloop()


if __name__ == "__main__":
    main()
