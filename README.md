# espresso-arm: PID Espresso Controller + Siri

## A Project for Odroid C2 / Raspberry Pi 3

This is an embedded ARM modification for home espresso machines to add:

* Accurate PID temperature control
* A pretty touch interface
* Control over the local network via a unified GUI
* Siri and HomeKit support for voice-activated heating

I use an [Odroid C2](http://ameridroid.com/products/odroid-c2) for this project. A Raspberry Pi 3 will work just as well.

The Odroid C2 (or Raspberry Pi) hosts the control application on a local webserver. Attach a touchscreen and control your espresso machine there, or use the local web interface with any phone, tablet, or computer.

![Interface](http://i.imgur.com/gbyqMFy.png)

The app logic, GPIO pin control (PWM), a PID controller, and the thermocouple driver are all implemented in Python. Even the GUI and local web server are generated with Python ([Remi](https://github.com/dddomodossola/remi)).

Siri support (via [HomeBridge](https://github.com/nfarina/homebridge)) requires Node.js, which causes a big dependency mess. If you don't want Siri support, everything else will work fine, and installation will be much easier for you.

### Parts List

Price | Supplier (US) | Name + Link
----- | ------------- | ----
$49 | Ameridroid | [Odroid C2 + USB to 2.5mm Power Adapter](http://ameridroid.com/products/odroid-c2)
$15 | Adafruit   | [Thermocouple Amplifier](https://www.adafruit.com/products/269)
$10 | Adafruit   | [Thermocouple](https://www.adafruit.com/products/270)
$5  | Adafruit   | [Thermal Tape](https://www.adafruit.com/products/1468)
$7  | Amazon     | [Solid State Relay](https://smile.amazon.com/gp/product/B00E1LC1VK/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$5  | Amazon     | [14 AWG Wire, Marine Grade](https://smile.amazon.com/gp/product/B000NV2E6O/ref=od_aui_detailpages00?ie=UTF8&psc=1)
$6  | Amazon     | [Weatherproof Connectors](https://smile.amazon.com/gp/product/B00GMO98NI/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$10 | Amazon     | [Breadboard Wires](https://smile.amazon.com/gp/product/B00M5WLZDW/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$9  | Amazon     | [USB Wifi Adapter](https://smile.amazon.com/gp/product/B003MTTJOY/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$4  | Amazon     | [USB Extension Cable](https://smile.amazon.com/Tripp-Lite-Universal-Reversible-UR024-18N-RA/dp/B00ESZJEEG/ref=sr_1_29?s=electronics&ie=UTF8&qid=1465866122&sr=1-29&keywords=usb+extension)
$**120**    |            |  

### Tools

Price | Supplier (US) | Name + Link
----- | ------------- | ----
$19 | Amazon     | [Soldering Iron](https://smile.amazon.com/gp/product/B0192PZD1Y/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$5  | Amazon     | [Solder Remover](https://smile.amazon.com/gp/product/B00L2HRW92/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$18  | Amazon     | [Wire Strippers](https://smile.amazon.com/gp/product/B000OQ21CA/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1)

## Installation

### Installing Linux

If you're starting from scratch, I recommend Arch Linux ARM. This guide assumes you're running Arch. If you already have a Linux distribution on your Odroid/Pi, and you're comfortable with Linux, you should be able to figure out how this translates to your platform. If you're not comfortable with Linux, flash your SD card with Arch and follow my instructions.

Arch Linux ARM provides a great installation guide for each platform:

 * [Odroid C2](https://archlinuxarm.org/platforms/armv8/amlogic/odroid-c2)
 * [Raspberry Pi 3](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)

 Follow the guide for your platform to get up-and-running with Arch Linux.

### Prerequisites

* `python` + `python2` (Yes, both Python 2 and 3.)
* `WiringPi-Python`: Get it [here](https://github.com/hardkernel/WiringPi2-Python) for the Odroid C2, and [here](https://github.com/WiringPi/WiringPi-Python) for the Raspberry Pi.
* `nodejs` + `npm`
* `avahi`

### Installing espresso-arm

> Just give me the damn commands to enter!

Okay:

        pacman -S python python2 nodejs npm avahi

        systemctl start avahi-daemon
        systemctl enable avahi-daemon
        sudo npm install -g homebridge --unsafe-perm
