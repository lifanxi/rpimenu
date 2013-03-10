rpimenu
==================

Modified from https://github.com/aufder/RaspberryPiLcdMenu

The difference between the two projects: RaspberryPiLcdMenu uses the buttons on Adafruit LCD Plates, rpimenu uses IR Remote control with LIRC.

A menu driven application template for on a Raspberry Pi.

It provides a simple way to navigate a nested set of menus, and run various
functions, by pressing the buttons on your IR Remote control.  
Included is a way to determine the IP address of the Pi when running
headless.  Also, allows the user to select from a large list of choices (using List
Selector), by cycling through letters vertically and horizontally.
It uses an XML file to configure the menu structure, and processes tags to enable
different options.  XML element support includes:
- folders, for organizing menus.
- widgets, which are really just functions to call in the code.
- run, which allows you to run any command and see the output on the LCD.

It assumes the user has the LCD 1602 with LIRC compatible infrared receiver.
You can also launch the Python based application from /etc/init.d.  In that mode, you can launch right into the application without
keyboard or monitor, yet still determine the IP address, change networks if you
like, or any other capability you build in. Also note that once you put it in init.d, if
you don't actually connect the LCD, you may find lots of error messages.  You may
want to test for presence of the LCD before running it.
Included also is an approach to switch networks from the UI, in case you want to
switch between different network layouts if you travel with it.

Some of the canned menu items are functional, but other are place holders to spawn
ideas.  Such as using gphoto2 to trigger camera operations.  Or using the ephem
library to do astronomy calculations.

BTW, the ListSelector relies on using the LCD plate's blink cursor capability.  As
of this writing, it had a bug, where you need to modify the LCD code to define a
blink method, similar to the other cursor methods.  Notice there are two noBlinks,
so change one to blink and change the code to do the right thing.

Written by Alan Aufderheide, modified by Li Fanxi

GPL v3 license, kindly include text above in any redistribution.
