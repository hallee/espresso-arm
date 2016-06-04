"""
GUI Comment
"""

import remi.gui as gui
from remi import start, App
from threading import Timer
import time


class Espresso(App):
    def __init__(self, *args):
        super(Espresso, self).__init__(*args)

    def main(self):
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
        self.powerSwitch.style['height'] = '52px'
        self.powerSwitch._label.attributes['for'] = 's1'
        self.powerSwitch._label.attributes['class'] = 'slider-v1'
        self.powerSwitch._checkbox.attributes['id'] = 's1'
        self.powerSwitch._label.set_on_mouseup_listener(self, 'on_power_change')
        
        self.steam = False
        self.steamSwitch = gui.PrettySwitch('Steam', False)
        self.steamSwitch.attributes['class'] = 'switch'
        self.steamSwitch.style['height'] = '52px'
        self.steamSwitch._label.attributes['for'] = 's2'
        self.steamSwitch._label.attributes['class'] = 'slider-v1'
        self.steamSwitch._checkbox.attributes['id'] = 's2'
        self.steamSwitch._label.set_on_mouseup_listener(self, 'on_steam_change')
        
        self.count = 0
        self.counter = gui.Label('', width=200, height=30)
        self.lbl = gui.Label('This is a LABEL!', width=200, height=30)
        
        self.bt = gui.Button('Press me!', width=200, height=30)
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        self.spin = gui.SpinBox('96', 92, 102, 1, width=200, height=30)
        self.spin.set_on_change_listener(self, 'on_spin_change')

        self.slider = gui.Slider('96', 92, 102, 1, width=200, height=20)
        self.slider.set_on_change_listener(self, 'slider_changed')
        
        subContainer.append(self.counter)
        subContainer.append(self.lbl)
        subContainer.append(self.bt)
        subContainer.append(self.spin)
        subContainer.append(self.slider)
        switchContainer.append(self.powerSwitch)
        self.switchContainer = switchContainer
        verticalContainer.append(switchContainer)
        verticalContainer.append(subContainer)
        mainContainer.append(verticalContainer)

        self.display_counter()

        # returning the root widget
        return verticalContainer
        
    def on_power_change(self, x, y):
        self.power = not self.power  
        self.powerSwitch._checkbox.set_value(self.power)      
        if self.power:
            self.lbl.set_text('ON')
            time.sleep(0.25)
            self.switchContainer.append(self.steamSwitch)
        else:
            self.lbl.set_text('OFF')
            time.sleep(0.25)
            self.switchContainer.remove_child(self.steamSwitch)

        
    def on_steam_change(self, x, y):
        self.steam = not self.steam        
        if self.steam:
            self.lbl.set_text('Steam ON')
        else:
            self.lbl.set_text('Steam OFF')
        self.steamSwitch._checkbox.set_value(self.steam)

    def display_counter(self):
        self.counter.set_text('Running Time: ' + str(self.count))
        self.count += 1
        Timer(1, self.display_counter).start()

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
