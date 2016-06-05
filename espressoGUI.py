"""
GUI Comment
"""

import threading
import time
from remi import start, gui, App
from systemcontrol.pinOut import SoftwarePWM
from systemcontrol.max31855 import SoftwareSPI
from systemcontrol.pid import PID
from multiprocessing import Process, Value


class Espresso(App):
    def __init__(self, *args):
        super(Espresso, self).__init__(*args)

    def main(self):
        self.setTemp = 96
        self.calibrationOffset = -4 # +5 degrees to thermocouple output.
        self.boilerTemp = 0
        self.tempStarted = False
        self.heaterPIDStarted = False
        self.tempProbe = SoftwareSPI()
        self.Process = Process
        
        self.pid = PID(3,1,0)
        self.pid.setPoint(self.setTemp)
                
        mainContainer = gui.Widget(width=320)
        verticalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_VERTICAL)
        verticalContainer.style['text-align'] = 'center'
        verticalContainer.style['margin'] = '2em auto'
        
        subContainer = gui.Widget(width='auto', height=160)
        subContainer.style['text-align'] = 'center'
        
        switchContainer = gui.Widget(width='auto', height=160)
        switchContainer.style['text-align'] = 'center'
        
        self.power = False
        self.powerSwitch = gui.PrettySwitch('Power', False)
        self.powerSwitch.attributes['class'] = 'switch'
        self.powerSwitch.style['height'] = '58px'
        self.powerSwitch._label.attributes['for'] = 's1'
        self.powerSwitch._label.attributes['class'] = 'slider-v1'
        self.powerSwitch._checkbox.attributes['id'] = 's1'
        self.powerSwitch._label.set_on_mouseup_listener(self, 'on_power_change')
        
        self.steam = False
        self.steamSwitch = gui.PrettySwitch('Steam', False)
        self.steamSwitch.attributes['class'] = 'switch'
        self.steamSwitch.style['height'] = '58px'
        self.steamSwitch._label.attributes['for'] = 's2'
        self.steamSwitch._label.attributes['class'] = 'slider-v1'
        self.steamSwitch._checkbox.attributes['id'] = 's2'
        self.steamSwitch._label.set_on_mouseup_listener(self, 'on_steam_change')
        
        self.tempLabel = gui.Label(str(self.boilerTemp)+' ')
        self.tempLabel.attributes['class'] = 'tempLabel'
        self.tempLabel.style['display'] = 'inline'

        self.degreeLabel = gui.Label(u'\N{DEGREE SIGN}'+'C')
        self.degreeLabel.attributes['class'] = 'degreeLabel'
        self.degreeLabel.style['display'] = 'inline'
        
        self.count = 0
        self.counter = gui.Label('', width=200, height=30)
        self.lbl = gui.Label('This is a LABEL!', width=200, height=30)
        
        # self.bt = gui.Button('Press me!', width=200, height=30)
        # self.bt.set_on_click_listener(self, 'on_button_pressed')
        # 
        # self.spin = gui.SpinBox('96', 92, 102, 1, width=200, height=30)
        # self.spin.set_on_change_listener(self, 'on_spin_change')
        # 
        # self.slider = gui.Slider('96', 92, 102, 1, width=200, height=20)
        # self.slider.set_on_change_listener(self, 'slider_changed')
        
        self.dummyUpdated = gui.Label('') # Blank widget to add to the page for forcing an update.
        # When a switch changes from a remote GUI, the local GUI doesn't update automagically.
        # So, forcing an update by adding this dummy to the scene. 
        # Replace with something better eventually.
        
        # subContainer.append(self.counter)
        # subContainer.append(self.lbl)
        # subContainer.append(self.bt)
        # subContainer.append(self.spin)
        # subContainer.append(self.slider)
        subContainer.append(self.tempLabel)
        subContainer.append(self.degreeLabel)
        switchContainer.append(self.powerSwitch)
        switchContainer.append(self.dummyUpdated)
        self.switchContainer = switchContainer
        verticalContainer.append(switchContainer)
        verticalContainer.append(subContainer)
        mainContainer.append(verticalContainer)

        self.display_counter()
        if self.tempStarted == False:
            t = threading.Thread(target=self.tempProbe.initiateSPI, args=(50, 100)) # 50% Duty, 50 Hz
            t.daemon = True
            t.start()
            self.tempStarted = True
        self.temperature_display()
        self.startPID()
        # returning the root widget
        return verticalContainer
        
    def startPID(self):
        if self.heaterPIDStarted == False:
            self.heaterController = SoftwarePWM(27)
            self.heaterController.pwmUpdate(0, 0.83333) # 1% steps when controlling 60 Hz mains.
            print('Initiated Heater PWM.')
            self.heaterPIDStarted = True
        if self.power == False:
            self.heaterController.pwmUpdate(0, 0.83333)
        elif (self.power == True and self.steam == False):
            pidOutputReal = self.pid.update(float(self.boilerTemp))
            pidOutput = pidOutputReal / 5
            if pidOutput > 100:
                pidOutput = 100
            elif pidOutput < 0:
                pidOutput = 0
            # pidNormalized = 0.09356112348 * (pidOutput + 548.75)
            # pidOutput = self.pid.update(float(19.25))
            print('Updating PID with: '+str(self.boilerTemp))
            print('PID Output:        '+str(pidOutputReal))
            print('PID Output Fixed: '+str(pidOutput))
            print('PID Setpoint:      '+str(self.pid.set_point))
            self.heaterController.pwmUpdate(int(pidOutput), 0.83333)
        elif (self.power == True and self.steam == True):
            pass
        threading.Timer(0.416666, self.startPID).start() # Repeat twice as fast as the PWM cycle
        
    def on_power_change(self, x, y):
        self.power = not self.power  
        self.powerSwitch._checkbox.set_value(self.power)      
        if self.power:
            self.pid.setPoint(self.setTemp)
            self.lbl.set_text('ON')
            self.steamSwitch._checkbox.set_value(False)
            time.sleep(0.25)
            self.switchContainer.append(self.steamSwitch)
        else:
            self.lbl.set_text('OFF')
            time.sleep(0.25)
            self.switchContainer.remove_child(self.steamSwitch)
            self.steam = False
        
    def on_steam_change(self, x, y):
        self.steam = not self.steam        
        if self.steam:
            self.lbl.set_text('Steam ON')
        else:
            self.lbl.set_text('Steam OFF')
        self.steamSwitch._checkbox.set_value(self.steam)
        time.sleep(0.25)
        self.switchContainer.remove_child(self.dummyUpdated)
        self.switchContainer.append(self.dummyUpdated)

    def display_counter(self):
        self.counter.set_text('Running Time: ' + str(self.count))
        self.count += 1
        threading.Timer(1, self.display_counter).start()
    
    def temperature_display(self):
        currentTemp = self.tempProbe.getTemp()
        self.boilerTemp = "{:.2f}".format(float(currentTemp) + self.calibrationOffset)
        self.tempLabel.set_text(str(self.boilerTemp))
        threading.Timer(0.5, self.temperature_display).start()

    def on_button_pressed(self):
        self.lbl.set_text('Button pressed! ')
        self.bt.set_text('Hi!')

    def on_spin_change(self, newValue):
        self.lbl.set_text('SpinBox changed, new value: ' + str(newValue))

    def slider_changed(self, value):
        self.lbl.set_text('New slider value: ' + str(value))
        

if __name__ == "__main__":
    # optional parameters
    # start(MyApp,address='127.0.0.1', port=8081, multiple_instance=False,enable_file_cache=True, update_interval=0.1, start_browser=True)
    start(Espresso, debug=True, address='0.0.0.0')  
