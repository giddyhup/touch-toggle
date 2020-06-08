# Touch Screen Toggle

Python 3 scripts to turn an official Raspberry Pi touchscreen off and on.

The scripts are extensively documented and, alternatively, work with the official Raspberry Pi touch screen. The Python module _evdev_ must be installed (globally or specifically for root). To change the screen's state sudo/root rights are required.

`simpletouch.py` can be used to toggle the screen off and on by touch. There is no specific region where the screen must be touched. All events are passed on to whatever is displayed on the screen.

`specialtouch.py` can be used to toggle the screen off by touching it in a specified rectangle (the source code needs to be edited). While the screen is off touch events in any area turn it back on. Since the user may not know what's on the screen while it is off all touch events are grabbed/discarded.
