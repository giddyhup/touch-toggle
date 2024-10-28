#!/usr/bin/python3
# package evdev must be installed

from evdev import InputDevice, ecodes, categorize
import subprocess
import time

# debug flag, no script output when False
debug = False
if debug: print('debug is on')

# touch screen device 
dev = InputDevice('/dev/input/event3')


def screenstate():
    r = subprocess.check_output('xset q | grep -q "Monitor is On" && echo -n on || echo -n off', shell=True, universal_newlines=True)
    return r

scrstate = screenstate()


# init vars
BTNstate = 0

# function to toggle screen state
def screentoggle(wantedstate):
    s = subprocess.check_output(f'xset dpms force {wantedstate}', shell=True)

# read events and categorize
for event in dev.read_loop():
    absevent = categorize(event)
    try:
        if ecodes.bytype[absevent.event.type][absevent.event.code] == 'BTN_TOUCH':
            BTNstate = absevent.event.value
            # read screen state when touch is detected
            if BTNstate == 1:
                scrstate = screenstate()
                if debug: print(f'Touch detected and screen state = {scrstate}')
                # act on touch events within the defined region when the screen is on
                if scrstate == 'on':
                    # turn screen off
                    screentoggle('off')
                    # reset variable
                    BTNstate = "0"
                    # debounce
                    time.sleep(.5)
                # act on touch events anywhere when the screen is off
                if (scrstate == 'off'):
                    # turn screen on and let events pass
                    screentoggle('on')
                    # reset variables
                    BTNstate = "0"
                    # debounce
                    time.sleep(.5)
    except:
        BTNstate = "0"
    # debounce
    time.sleep(.5)
