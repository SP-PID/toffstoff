class stepper():
    def __init__(self):
        self.pulse = dg.DigitalInOut(board.D17)
        self.pulse.direction = dg.Direction.OUTPUT
        self.direc = dg.DigitalInOut(board.D15)
        self.direc.direction = dg.Direction.OUTPUT
        self.enable = dg.DigitalInOut(board.D18)
        self.enable.direction = dg.Direction.OUTPUT
        self.ms1 = dg.DigitalInOut(board.D20)
        self.ms1.direction = dg.Direction.OUTPUT
        self.ms2 = dg.DigitalInOut(board.D21)
        self.ms2.direction = dg.Direction.OUTPUT
        self.ms1.value = False
        self.ms2.value = False
        self.stop = dg.DigitalInOut(board.D9)
        self.stop.direction = dg.Direction.INPUT

        self.step_time = 0.0007

        self.direction = "up"
        self.current_pos = 0

        self.Set_stepping("Quarter")
        
    def Set_stepping(self, stepp):
        if stepp == "Full":
            self.ms1.value = False
            self.ms2.value = False

        if stepp == "Half":
            self.ms1.value = True
            self.ms2.value = False
            
        if stepp == "Quarter":
            self.ms1.value = False
            self.ms2.value = True

        if stepp == "Eigth"
            self.ms1.value = True
            self.ms2.value = True

    def driver_on(self):        
    ''' Function that enables Easydriver for use '''
        enable.value = False

    def driver_off(self):        
    ''' Function that disables Easydriver after use '''
        enable.value = True 
    
    
    def drive(self,sp):
        if sp == self.current_pos:
            self.driver_off()
            return
        if sp != self.current_pos:
            self.driver_on()

        if sp < self.current_pos:
            self.direc.value = True
            self.current_pos --0.25
            self.step()

        if sp > self.current_pos:
            self.direc.value = False
            self.current_pos ++0.25
            self.step()

        return

    def step(self):
        pulse.value = True
        time.sleep(self.step_time)      # wait
        pulse.value = False
        time.sleep(self.step_time)      # wait
        return