# ARM Espresso Controller

## A Project for Odroid C2 / Raspberry Pi 3

This is an embedded ARM modification for home espresso machines to add:

* Accurate PID temperature control.
* Pretty touch interface.
* Control over the local network via the GUI.
* Siri and HomeKit support for voice-activated heating.

I use an [Odroid C2](http://ameridroid.com/products/odroid-c2) for this project (it's easier to get, faster, and has a heat sink), but a Raspberry Pi 3 should work just as well.

The Odroid C2 (or Raspberry Pi) hosts the control application on a local webserver. This way, you can control it with a connected touch screen if you want to add one, or if not, you can control it from your phone, computer, or anything with a web browser connected to your wifi. 

[Note about Siri Control]

![Interface](http://i.imgur.com/gbyqMFy.png)

The app logic, GPIO pin control (PWM), PID controller, and temperature board driver are all implemented in Python. Even the GUI and local web server are generated with Python ([Remi](https://github.com/dddomodossola/remi)).

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
