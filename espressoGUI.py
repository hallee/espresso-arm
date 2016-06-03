"""
GUI Comment
"""

import remi.gui as gui
from remi import start, App
from threading import Timer


class Espresso(App):
    def __init__(self, *args):
        super(Espresso, self).__init__(*args)

    def main(self):
        verticalContainer = gui.Widget(width=400)
        verticalContainer.style['display'] = 'block'
        verticalContainer.style['overflow'] = 'hidden'
        verticalContainer.style['text-align'] = 'center'
        verticalContainer.style['margin'] = '0 auto'


        horizontalContainer = gui.Widget(width='100%', layout_orientation=gui.Widget.LAYOUT_HORIZONTAL, margin='0 auto')
        # horizontalContainer.style['display'] = 'block'
        horizontalContainer.style['overflow'] = 'auto'
        horizontalContainer.style['text-align'] = 'center'
        horizontalContainer.style['margin'] = '0 auto'



        # the arguments are	width - height - layoutOrientationOrizontal
        subContainer = gui.Widget()
        # subContainer.style['width'] = '380px'
        subContainer.style['display'] = 'block'
        subContainer.style['overflow'] = 'auto'
        subContainer.style['text-align'] = 'center'
        
        self.powerSwitch = gui.CheckBox(False)
        surround = gui.Widget()
        surround.attributes['class'] = 'surround'
        switchClass = gui.Widget()
        switchClass.attributes['class'] = 'switch'
        buttonClass = gui.Widget()
        buttonClass.attributes['class'] = 'button'
        buttonFaceClass = gui.Widget()
        buttonFaceClass.attributes['class'] = 'button-face'
        shadowClass = gui.Widget()
        shadowClass.attributes['class'] = 'shadow'
        buttonFaceClass.append(shadowClass)
        switchClass.append(buttonClass)
        switchClass.append(buttonFaceClass)
        surround.append(switchClass)
        
        self.count = 0
        self.counter = gui.Label('', width=200, height=30, margin='10px')
        self.lbl = gui.Label('This is a LABEL!', width=200, height=30, margin='10px')
        
        self.bt = gui.Button('Press me!', width=200, height=30, margin='10px')
        self.bt.set_on_click_listener(self, 'on_button_pressed')

        self.spin = gui.SpinBox('96', 92, 102, 1, width=200, height=30, margin='10px')
        self.spin.set_on_change_listener(self, 'on_spin_change')

        self.slider = gui.Slider('96', 92, 102, 1, width=200, height=20, margin='10px')
        self.slider.set_on_change_listener(self, 'slider_changed')

        subContainer.append(self.powerSwitch)
        subContainer.append(surround)
        subContainer.append(self.counter)
        subContainer.append(self.lbl)
        subContainer.append(self.bt)
        subContainer.append(self.spin)
        subContainer.append(self.slider)
        self.subContainer = subContainer
        horizontalContainer.append(subContainer)
        verticalContainer.append(horizontalContainer)

        # kick of regular display of counter
        self.display_counter()

        # returning the root widget
        return verticalContainer

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
