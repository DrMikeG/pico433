

Let's just think about the logical connections from the pi:



5v
40* - To pin of TX board
40* - To pin of RX board

3v3
36* - To resistor (10k) then input to invertor diode
36* - To input of touch sensor

Gnd
3 - To pin of TX board
8 - To pin of touch sensor
13 - To pin of RX board
18 - To leg of Blue LED
33 - To leg of invertor diode

GPIO
19 - Touch
16 - pin TX 
18 - resistor (1k) then Blue LED leg
17 - invertor diode leg (RX)

RX
Receiver Pin - resistor (1k) then invertor diode leg