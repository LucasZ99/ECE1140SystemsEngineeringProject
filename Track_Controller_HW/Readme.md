ECE 1140 Track Controller Hardware Module Help Documentation
Devin James

Compatibility:
	By design, the Track Controller HW module is able to operate without the accompanying Raspberry Pi 4 attached. This will ensure that the PLC for this portion of the track will always be ran and the critical safety operations to avoid train collisions will always be performed. The use of the Raspberry Pi 4 is the user interface; after new track data is received and the PLC logic is run, the data is sent through Wi-Fi signal to the Raspberry Pi. The data being sent through the Wi-Fi signal also enables the system to run without the Pi with no issues; the HardwareUi.py file will simply send out the data, whether or not the data is then received will cause no issues in the system’s overall functionality.  

Hardware UI:
	Running the user interface functionality requires a Raspberry Pi 4, a Wi-Fi connection, and an AdaFruit “Neopixel” library compatible LED strip (look for WS2812, WS2811, or SK6812 LED driver strips). To connect the strip to the Pi, connect the strip’s 5V connection to a 5V pin on the Pi, the strip’s ground to a ground pin on the Pi, and the strip’s D0/Din connection to pin 12 of the Pi.
 ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/9c633e13-130c-4674-9df7-265788fc434c)

 
Once the strip is connected, the Pi must run a program called RPiServer.py to establish a server that can receive the current state of the occupancies over Wi-Fi connection. Running this program may require the editing of the ServerIp variable. To determine the current IP address of the Pi, input ifconfig into the terminal and edit the value in the code of the RPiServer.py file:
![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/b65d2646-cd3d-463f-8443-771f4351d949)
![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/eb552c3b-8f23-4c3f-843f-12354f6d30f5)

 
 
Once that all is set up, use the cd command so the terminal is in the current directory of the RPiServer.py file (in my case I use “cd Desktop”) and type the following command to begin the server. If everything is properly set up, then the terminal will output “Server is up”.
 ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/7bf82057-1935-430b-88c2-98720ac2cc5c)


	The last step to setting up the wireless UI connection is to connect the computer that the system is on to the same Wi-Fi as the Raspberry Pi. Once again you may have to edit the IP variable in the HardwareUi.py file:
  ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/55018db0-1bf0-4994-a4e1-d5c43cd815c0)


Module Demo:
To get a demonstration of the track controller iterating through each occupancy, run the TrackControllerHW.py file. This will run the system as a standalone simulation, which has two modes; If the mode flag is set to False, then the LEDs will simply display occupancies as a single LED moving down the track: 
![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/ba73562b-768d-440e-9af2-a1a9b3380600)

 
The only proof of the PLC executing in this case comes when the blocks 107,108, or 109 are occupied; in which case the LED will change color to indicate that the PLC has determined that the railroad crossing signal should be activated. Running the program with the mode flag set to true will cause the output to show PLC execution much more obviously:
 ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/988d8f54-e10f-4ee8-9898-b48b46003311)

This simulation will show the normal occupancy being trailed by 4 other red LEDs. The red LEDs indicate the zero speed flags, which the PLC assigns each time a new occupancy is detected and are passed along throughout the rest of the system to indicate that any train running into one of these should stop. Due to the single-direction portion of the track that this controller is responsible for, rear-end collisions will eliminate any chance of collision. The PLC also considers any incontiguity in the track (ie. the train is going into the yard or a portion of track that track controller B does not have the ability to see). Here is an example:
 ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/d3dda503-67d6-4161-9eae-227dadc0ba0d)

This is the kind of situation that the PLC is able to avoid. The train enters the yard, effectively no longer posing any risk of being collided with afterwards. In this situation these zero speed flags are only an obstacle to the efficiency of the system; stopping any subsequent trains unnecessarily. With the PLC’s ability to avoid this, the situation plays out more like this:

 ![image](https://github.com/fletch2001/ece1140-tovarish/assets/45702781/ed8ba10d-ca59-4ba4-ad1e-df26d92ba60b)

Once the train is no longer on a spot of track that the track controller is responsible for, any zero speed flags are removed, avoiding any unneeded stops of trains whil
