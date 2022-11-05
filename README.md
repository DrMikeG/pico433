# pico433
project to replace esp32 433mhz controller with pi pico



Micropython needs script called main.py to auto-run.




https://forums.raspberrypi.com/viewtopic.php?t=340099

Your method of clearing PIO state has one major drawback in that you're not clearing PIO memory, so inevitably you'll run into ENOMEM error because MicroPython will add instructions to memory instead of overwriting them. You also need to run:

PIO(x).remove_program()

I've tested it a bit and you're absolutely right. It seems that on Pico non-W (haven't tested on W) pressing play or stop (or equivalent keyboard shortcuts) in Thonny clears the PIO memory but keeps the state machines running and pins configured to PIO function, so loading the same program in the same instruction space will make all previously running SMs run again as if nothing happened. I think it's a major oversight and a quick glance at issues on MicroPython's github doesn't show anything similar, so maybe it's worth filing an issue there.