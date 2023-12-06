# pygeiger
A python script which plots bytes on the serial port, intended to be used with a geiger counter which dumps one byte per count.  Developed on Images Co. DTG-01 and Raspberry Pi for museum exhibit but should work with other makes and models.

pygeiger
version 0.9
2023-08-24
Brian P. d'Entremont

This is the code behind the radiation exhibit at the SRS Musuem (https://www.srsheritagemuseum.org/).

Files:
geiger_read.py
Produces a rolling full-screen plot of the count rate.  Installed source activity levels are displayed on screen which will diminish with calculated rate of decay.

geiger_source_set.py
Produce the source activity levels and time stamps by counting each source for 30s.  Run from a command line and follow instructions.  Will overwrite source_list.txt.

lib_geiger_plot.py lib_geiger_util.py
Functions related to the plot and the serial interface respectively.

source_tmpl.txt
A template for the source information on screen.

Tested hardware:
Geiger Counter:
	DTG-01 Professional Desktop Geiger Counter (unit,wand,power supply)
	https://www.imagesco.com/geiger/desktop-digital-geiger-counter.html
USB serial port to 1/8 conversion cable
	configured Pin 2 RxD: tip, Pin 3 TxD: ring, Pin 5: shield
This cable uses a PC210x chipset which is supported by default on the Linux kernel currently on the Pi (6.1.21-v8)
	https://www.imagesco.com/semiconductors/usb-3.5mm.html
Computer:
	Raspberry Pi 4 with power supply, case, and HDMI adapter
	https://www.amazon.com/Vilros-Raspberry-RAM-Basic-Heavy-Duty-Self-Cooling/dp/B0854Q9WX2
Monitor:
	24” HP V24i FHD 
	Note: program is configured for monitor configured to Full HD (1920 x 1080) resolution.
	https://www.amazon.com/HP-V24i-23-8-inch-Diagonal-Computer/dp/B08G5R5LM3
Wireless USB keyboard and mouse (for maintenance)
	https://www.amazon.com/Logitech-MK270-Wireless-Keyboard-Mouse/dp/B079JLY5M5

Configuration:
Connect USB serial cable from TTL port on the Geiger counter to any USB port on the Pi.  Connect wand.  Set random number generator to switch to “1-2”.  Turn everything on.  The computer is configured for auto login.

To exit the plot and return to the Linux desktop, press alt-tab as many times as needed to switch to the terminal window and ctrl-C in the terminal window to kill the python script.  To restart the plot or start it if it does not start automatically, double click the geiger_read.py and press the “execute in terminal” option at the prompt.

After installing new sources, exit to the desktop, and double click geiger_source_set.py and at the prompt press “execute in terminal”.  Follow instructions in the terminal window to get a baseline count for each source.  Type “yes” at the final prompt to overwrite existing source values.

Note: In random 1-2 mode the Geiger counter generates a random byte at every event, of which we can ignore the value and count the events.  Serial configuration, as set in serial_util.py should be baudrate=9600, parity=None, stopbits=one, byte size=eight bits for this device.
