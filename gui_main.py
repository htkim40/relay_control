import tkinter
import gpiozero
import time
import threading


# gui offsets
NUMBER_OF_CHANNELS = 8
OPTIONS_FRAME_OFFSET_X = 15
OPTIONS_FRAME_OFFSET_Y = 15
OPTIONS_TO_STATUS_FRAME_OFFSET = 420
LABEL_OFFSET = 25
LABEL_TO_ELEMENT_OFFSET = 25

# GPIO to relay map
RELAY = [0 for i in range(NUMBER_OF_CHANNELS)]
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

        self.relayTaskHandle = [None for i in range(NUMBER_OF_CHANNELS)]
        self.timerTaskHandle = [None for i in range(NUMBER_OF_CHANNELS)]
        self.stopEventHandle = [1 for i in range(NUMBER_OF_CHANNELS)]
        self.master = master
        self.master.title("Power Cycling Test UI")
        self.master.geometry("740x420")

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
                      textvariable=self.dutyCycleLabel).place(x=OPTIONS_FRAME_OFFSET_X + 133,
                                                              y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.dutyCycleLabel.set("Duty Cycle(%)")

        # set up number of cycles label
        self.noOfCyclesLabel = tkinter.StringVar()
        tkinter.Label(self.testOptionFrame,
                      textvariable=self.noOfCyclesLabel).place(x=OPTIONS_FRAME_OFFSET_X + 220,
                                                               y=LABEL_OFFSET+OPTIONS_FRAME_OFFSET_Y)
        self.noOfCyclesLabel.set("No. of Cycles")

        # set up the status pane
        self.statusFrame = tkinter.LabelFrame(self.master,
                                              text="Test Status").place(x=OPTIONS_FRAME_OFFSET_X
                                                                          + OPTIONS_TO_STATUS_FRAME_OFFSET,
                                                                        y=OPTIONS_FRAME_OFFSET_Y,
                                                                        width=290,
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
        self.testTimeLabel.set("Test Time(HH:MM:SS)")
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
                          textvariable=self.numOfCycleEntries[i]).place(y=LABEL_OFFSET +
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
                                             width=115)

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

    def start(self, chEnableHndl):
        ch = abs(chEnableHndl.get()) - 1
        print("Starting channel %d" % ch)
        print("Generating test thread")
        requestedPeriod = self.periodEntries[ch].get()
        requestedDutyCycle = self.dutyCycleEntries[ch].get()
        requestedNumOfCycles = self.numOfCycleEntries[ch].get()

        if requestedPeriod == "" or requestedDutyCycle == "" or requestedNumOfCycles == "":
            print("Error: One or more empty fields")
        else:
            print("Period: %f \nDuty Cycle: %f \nRequested Cycles: %d" % 
                   (float(requestedPeriod),
                    float(requestedDutyCycle),
                    int(requestedNumOfCycles)))
            self.stopEventHandle[ch] = 0
            self.timerTaskHandle[ch] = threading.Thread(target=relay_test_timer,
                                                        args=(ch,
                                                              self.chTestTimeEntries,
                                                              self.stopEventHandle))
            self.relayTaskHandle[ch] = threading.Thread(target=toggle_relay_test,
                                                        args=(ch,
                                                              RELAY[ch],
                                                              float(requestedPeriod),
                                                              float(requestedDutyCycle),
                                                              int(requestedNumOfCycles),
                                                              self.stopEventHandle,
                                                              self.chStateEntries,
                                                              self.chCycleCountEntries))
            self.timerTaskHandle[ch].start()
            self.relayTaskHandle[ch].start()



    def start_all(self):
        startText = 'Starting channels: '
        for ch in range(NUMBER_OF_CHANNELS):
            if self.enableChButtonVars[ch].get() > 0:
                self.start(self.enableChButtonVars[ch])
                startText += "%d, " % (self.enableChButtonVars[ch].get()-1)
        print(startText[0:len(startText)-2])

    def stop(self, channel):
        ch = abs(channel.get()) - 1
        print("Stopping channel %d" % ch)
        self.stopEventHandle[ch] = 1

    def stop_all(self):
        stopText = 'Stopping channels: '
        for ch in range(NUMBER_OF_CHANNELS):
            if self.enableChButtonVars[ch].get() > 0:
                self.stop(self.enableChButtonVars[ch])
                stopText += "%d, " % (self.enableChButtonVars[ch].get() - 1)
        print(stopText[0:len(stopText) - 2])


def init_relay(relayArray=RELAY, state=0):
    for relay in relayArray:
        relay.value = state


def toggle_relay_test(channel, relay, period, dutyCycle, requestdCycles, stopEventHandle, stateTextHandle, cycleTextHandle):
    cycle = 0
    cycleTextHandle[channel].set(str(cycle))
    while cycle < requestdCycles and stopEventHandle[channel] == 0:
        relay.value = 1
        stateTextHandle[channel].set("On")
        polling_wait(float(period)*(float(dutyCycle)/100),stopEventHandle,channel)
        relay.value = 0
        stateTextHandle[channel].set("Off")
        polling_wait(float(period)*(1-(float(dutyCycle)/100)),stopEventHandle,channel)

        # if the number of cycles is greater than 0, count cycles, otherwise infinite cycles
        if int(requestdCycles) >= 0 and stopEventHandle[channel] == 0:
            cycle += 1
            print("Cycle: %d" % cycle)
            cycleTextHandle[channel].set(str(cycle))
    stopEventHandle[channel] = 1

def relay_test_timer(channel, timeEntryHandle, stopEventHandle):
    startTime = time.time()
    while stopEventHandle[channel] == 0:
        endTime = time.time()
        hours, rem = divmod(endTime - startTime, 3600)
        minutes, seconds = divmod(rem, 60)
        timeEntryHandle[channel].set("{:0>5}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
        time.sleep(0.1)

def polling_wait(seconds,stopEventHandle,stopIndex):
    tStart = time.time()
    while time.time()-tStart < seconds and stopEventHandle[stopIndex] == 0:
        time.sleep(0.1) 

def main():

    #tasks = [toggle_relay_test for i in range(NUMBER_OF_CHANNELS)]
    #for task in tasks:

    #init_relay()
    #toggle_relay_test(RELAY[0])
    gui_root = tkinter.Tk()
    gui_main = RelayArrayGUI(gui_root)
    gui_main.master.mainloop()


if __name__ == "__main__":
    main()
