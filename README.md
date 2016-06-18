# espresso-arm: PID Espresso Controller + Siri

## A Project for Odroid C2 / Raspberry Pi 3

This is an embedded ARM modification for home espresso machines to add:

* Accurate PID temperature control
* A pretty touch interface
* Control over the local network via a unified GUI
* Siri and HomeKit support for voice-activated heating

I use an [Odroid C2](http://ameridroid.com/products/odroid-c2) for this project. A Raspberry Pi 3 will work just as well. I also show installation in a rather uncommon Lelit espresso machine. This will work fine in your Rancilio Silvia and most other single-boiler machines, but you'll need to be comfortable figuring out the wiring. If you want specific build instructions for the Silvia, send me one!

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
$10  | Amazon    | [SD Card](https://smile.amazon.com/Samsung-Class-Adapter-MB-MG16EA-AM/dp/B014W1ZL3S/ref=sr_1_1?ie=UTF8&qid=1466254153&sr=8-1)
$7  | Amazon     | [Solid State Relay](https://smile.amazon.com/gp/product/B00E1LC1VK/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$5  | Amazon     | [14 AWG Wire, Marine Grade](https://smile.amazon.com/gp/product/B000NV2E6O/ref=od_aui_detailpages00?ie=UTF8&psc=1)
$6  | Amazon     | [Weatherproof Connectors](https://smile.amazon.com/gp/product/B00GMO98NI/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$10 | Amazon     | [Breadboard Wires](https://smile.amazon.com/gp/product/B00M5WLZDW/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$9  | Amazon     | [USB Wifi Adapter](https://smile.amazon.com/gp/product/B003MTTJOY/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$4  | Amazon     | [USB Extension Cable](https://smile.amazon.com/Tripp-Lite-Universal-Reversible-UR024-18N-RA/dp/B00ESZJEEG/ref=sr_1_29?s=electronics&ie=UTF8&qid=1465866122&sr=1-29&keywords=usb+extension)
$**130**    |            |  

### Tools

Price | Supplier (US) | Name + Link
----- | ------------- | ----
$19 | Amazon     | [Soldering Iron](https://smile.amazon.com/gp/product/B0192PZD1Y/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$5  | Amazon     | [Solder Remover](https://smile.amazon.com/gp/product/B00L2HRW92/ref=od_aui_detailpages01?ie=UTF8&psc=1)
$18  | Amazon     | [Wire Strippers](https://smile.amazon.com/gp/product/B000OQ21CA/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1)

## Installation

If you're starting from scratch, I recommend Arch Linux ARM. This guide assumes you're running Arch. If you already have a Linux distribution on your Odroid/Pi, and you're comfortable with Linux, you should be able to figure out how this translates to your platform.

### Installing Linux

Arch Linux ARM provides a great installation guide for each platform:

 * [Odroid C2](https://archlinuxarm.org/platforms/armv8/amlogic/odroid-c2)
 * [Raspberry Pi 3](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)

 Follow the guide for your platform to get up-and-running with Arch Linux. You'll need another Linux machine to flash the SD card with Arch Linux, so hopefully you already run Linux somewhere.

Once you have bootable media with Arch Linux, you'll need to set up Wifi and get everything working while you have access to a keyboard & monitor. I strongly suggest reading the Arch Linux Wiki's [general recommentations](https://wiki.archlinux.org/index.php/General_recommendations) page.

### Prerequisites

* `python`
* `WiringPi` + `WiringPi-Python`

If you want Siri support, you'll also need:
* `python2`
* `avahi`
* `nodejs` + `npm`
* [`HomeBridge`](https://github.com/nfarina/homebridge)
* [`homebridge-http`](https://github.com/rudders/homebridge-http)

### Installing espresso-arm

As root:

    pacman -S git python python-pip base-devel

* On the Odroid:

      pacman -S wiringc1
      git clone https://github.com/hardkernel/WiringPi2-Python.git
      pip install WiringPi2-Python/

* On the Raspberry Pi:

      pacman -S wiringpi
      git clone --recursive https://github.com/WiringPi/WiringPi-Python.git
      pip install WiringPi2-Python/


    cd ~
    git clone https://github.com/hallee/espresso-arm.git
    cd espresso-arm/
    cp espresso.service /etc/systemd/system
    systemctl start espresso
    systemctl enable espresso
    cd remi/
    python setup.py install

For automatic login to root (make sure you've changed your root password at least):

    systemctl edit getty@tty1
    [Service]
    ExecStart=
    ExecStart=-/usr/bin/agetty --autologin root --noclear %I $TERM




#### Extra Steps for Siri Support

For Siri support, as root:

    pacman -S python2 nodejs npm avahi

    systemctl start avahi-daemon
    systemctl enable avahi-daemon
    npm install -g homebridge --unsafe-perm
    npm install -g homebridge-http
