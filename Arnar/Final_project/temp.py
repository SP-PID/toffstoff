import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
import numpy as np
import rotaryio

clk = 17
dt = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
time = 0
clkLastState = GPIO.input(clk)

class enc_val:
    def __init__(self) -> None:
        GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.encA = rotaryio.IncrementalEncoder(board.D9,board.D8)


class GUI:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        enc_val = get_enc_value(counter, clkLastState, time )
        global depth    #kallar á global breytuna depth svo hægt sé að nota hana í þræðinum 
        
        fig = plt.figure(facecolor='#7d7d7d')   #Stillir lit á glugganum sem kemur upp með punktaritið 
        win = fig.canvas.manager.window  # skilgreinir gluggan sem kemur upp
        screen_res = win.wm_maxsize()   #Notað til þess að stilla gluggan
        dpi = 150.0  # Upplausn myndarinnar
        fig.set_dpi(dpi)    #setur upplausn myndarinnar


        ax = fig.add_subplot(111, facecolor='k')    #Áhvarðar hvaða litur er á bakgrunninum á punktaritinu
        r_max = 2   #Breita sem segir til um efri mörk punktaritsins
        ax.set_ylim([0.2, r_max])   #Skilgreinir neðri og efri mörk á y-ás
        ax.set_xlim([0.0, 640])  #Skilgreinir neðri og efri mörk á x-ás
        ax.tick_params(axis='both', colors='w') #Stillingar fyrir ása
        ax.tick_params(axis='both', colors='w') #Stillingar fyrir ása
        ax.grid(color='w', alpha=0.5)  #Stillir lit á hnitaneti 
        angles = np.arange(0, 640, 1)   #Skilgreinri fylkjabreitu sem notuð er fyrir x-ás.

        ##################################################################################
        #Skilgreinir punktana í punkta ritinu. Þessu tilfelli er um við með 5 punkta línur
        pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='w',
                        markeredgecolor='#EFEFEF', markeredgewidth=1.0,
                        markersize=1.0, alpha=0.9)  # dots for radar points
        ###################################################################################
        
        plt.show(block=False)

        fig.set_size_inches(0.95*(screen_res[0]/dpi), 0.95*(screen_res[1]/dpi)) #Áhvarðar stæðr gluggans sem keumur upp útfrá uplausn skjás
        plot_res = fig.get_window_extent().bounds  #Stilling til þess að miðja ritið í glugganum
        win.wm_geometry('+{0:1.0f}+{1:1.0f}'.
                        format((screen_res[0]/2.0)-(plot_res[2]/2.0),
                               (screen_res[1]/2.0)-(plot_res[3]/2.0)))  # Miðjar ritið í glugganum
        fig.canvas.toolbar.pack_forget()  #Fjarlægir toolbar
        fig.canvas.set_window_title('IVAN Vision')   #Setur titil á glugan

        fig.canvas.draw()  #Teiknar upp ritið
        axbackground = fig.canvas.copy_from_bbox(ax.bbox)
       
        fig.show()  #sýnir myndina

        #Lykkja sem keyrir á meðan forritið keyrir og uppfærir punktaritið 
        while True:

           
            try:
                enc_val, time = get_enc_value()
                enc_val  #Tekur eina lágrétta línu og setur inn í breytu
                pols.set_data(angles, depth1)   #græjar gögn til þess að hægt sé að teikna þau
                fig.canvas.restore_region(axbackground) #Heldur bakgrunninum
                ax.draw_artist(pols)    #Teikar nýtt punktarit út frá nýjumm uplýsingum
                fig.canvas.flush_events()   #Fjarlægir punktaritin sem voru á undan
                fig.canvas.blit(ax.bbox)    #Sýnir uppfærð punktarit


            except KeyboardInterrupt:
                plt.close('all')
                print('Keyboard Interrupt')
                break


class Drive:
    def __init__(self) -> None:
        self.disp = screen()
        self.motor_Ain1 = pwmio.PWMOut(board.D12,frequency = 50)
        self.motor_Ain2 = pwmio.PWMOut(board.D13,frequency = 50)
        self.motor_Bin1 = pwmio.PWMOut(board.D10,frequency = 50)
        self.motor_Bin2 = pwmio.PWMOut(board.D11,frequency = 50)
        self.motor_a = Motor.DCMotor(self.motor_Ain1,self.motor_Ain2)
        self.motor_b = Motor.DCMotor(self.motor_Bin1,self.motor_Bin2)
        self.encA = rotaryio.IncrementalEncoder(board.D9,board.D8)
        self.encB = rotaryio.IncrementalEncoder(board.D6,board.D7) 
        #self.config = Conf()  


    
    def velocity(self):
        motor_radius = config.wheel_dia
        motor_rad = motor_radius/1000
        delta_time = 0
        angular_velocity1 = 0
        angular_velocity2 = 0
        delta_angle = 0
        now = time.monotonic()
        ticks1 = self.encA.position
        ticks2 = self.encB.position
        angle1 = ticks1 * (2 * math.pi / 700)
        angle2 = ticks2 * (2 * math.pi / 700)
        time.sleep(0.1)
        ticks1 = self.encA.position
        ticks2 = self.encB.position
        delta_time = time.monotonic() - now
        delta_angle1 = angle1 - (ticks1 * (2 * math.pi / 700))
        delta_angle2 = angle2 - (ticks2 * (2 * math.pi / 700))
        if delta_time > 0:
            angular_velocity1 = delta_angle1 / delta_time
            angular_velocity2 = delta_angle2 / delta_time
        linear_velocity1 = motor_rad * angular_velocity1
        linear_velocity2 = motor_rad * angular_velocity2
        return angular_velocity1, linear_velocity1,angular_velocity2, linear_velocity2

    def rpm(self):
        delta_time = 0
        start = time.monotonic()
        start_ticks1 = self.encA.position
        start_ticks2 = self.encB.position
        time.sleep(0.1)
        
        delta_time = time.monotonic() - start
        delta_ticks1 = self.encA.position - start_ticks1
        delta_ticks2 = self.encB.position - start_ticks2

        rpm1 = ((delta_ticks1 / 7) / delta_time) * 60
        rpm2 = ((delta_ticks2 / 7) / delta_time) * 60

        return rpm1, rpm2

    
    def get_enc_value(self,A_or_B):
        if A_or_B == "A":
            enc = self.encA.position
        elif A_or_B == "B":
            enc = self.encB.position
        return enc
    
    def DRV_OL_FW(self):
        dist1 = 0
        dist2 = 0
        self.encA.position = 0
        self.encB.position = 0
        
        while dist1 < config.FW_test_dist and dist2 < config.FW_test_dist:
            if ESTOP.Read_Lock() == True:
                break
            if ir.Get_dist() > config.follow:
                dist1 = self.encA.position * (config.wheel_dia/100)
                dist2 = self.encB.position * (config.wheel_dia/100)
                self.throttle(255,255,"FWD")
            
            if ir.Get_dist() < config.break_dist:
                self.throttle(0,0,0)            
            
            self.disp.text_to_disp("Distance: {0}mm".format(dist1), 0, 6, 1)
            self.disp.show()
            self.disp.clear()

        self.throttle(0,0,0)

        

    def Motor_A2D_PWM(self):
                duration = config.test_dur
                timestamp = time.monotonic()
                while time.monotonic() - timestamp < duration:
                    if ESTOP.Read_Lock() == True:
                        break
                    self.motor_a.throttle = self.pwm_sense("A") / 255
                    self.motor_b.throttle = self.pwm_sense("B") / 255
                    a1,l1,a2,l2 =self.velocity()
                    self.disp.text_to_display_4("Ang.Vel.L:{0:0.2f} rad/s".format(a1),"Lin.Vel.L:{0:0.2f} m/s".format(l1),"Ang.Vel.R:{0:0.2f} rad/s".format(a2),"Lin.Vel.R:{0:0.2f} m/s".format(l2))
                self.disp.clear()
                self.disp.show()
                self.throttle(0,0,0)