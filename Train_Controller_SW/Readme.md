# Train Controller Software, Elizabeth Novikova

The Train Controller software module is used to control a simulated train on the simulated track. The train 
controller takes inputs from the train model (either through integration or through manual test bench) and driver and 
then performs control functions on those inputs in order to provide the train model with an engine power. All actions 
performed by the train controller module are done so to ensure the train system remains in a vital state and avoids failures.
## Installation
### Windows 10
Windows 10 can be installed here: https://www.python.org/downloads/release/python-3110/

### Python 3.11
Python 3.11 can be installed here: https://www.python.org/downloads/release/python-3110/

### Python libraries
The following external libraries are needed for proper functionality of the Train Controller Software module
- PyQt6

PyQt6 is used for both the UI design and for sending signals between the train controller software frontend and backend,
as well as for integration.\
PyQt6 can be installed by using the following command in the Command Prompt:\
```pip install PyQt6```

## Running Standalone Module
To run the module as a standalone component, navigate to the 'TrainControllerSWContainer.py' file within an IDE or code 
editor of choice and run main(). The Train Controller UI will appear for a single train. Due to the vital architecture 
of the Train Controller, the module initializes with the speed and authority values set to the most vital value: 0. To 
simulate train movement and communication between modules when running standalone, the train controller test bench can 
be used. Clicking the 'Open Test Bench' button in the UI will open the test bench.\
Within the test bench, modifying the values for commanded speed and authority will trigger power control of the Train
Controller. These can either be changed in their individual attribute slots or in the joint array denoted 1: 
representing the train model input array for authority and commanded speed. The arrays that mimic the train model input
denoted 2: and 3: take in [polarity, underground] (with appended bacon information) for 2 and [actual speed, passenger 
ebrake]. Hitting the "update" button in the train controller test bench will take all values in these 3 arrays exactly
as they would be sent in integration, and the train controller will perform its responding computations. Power will be 
calculated once authority is set above 4 and commanded speed is set above 0.\
Once power and authority is set and the train has calculated power, the actual speed of the train can be changed in the
test bench and the train controller will update values as if a signal has been received from the train model.

## Running Integrated Module
_To be completed when integration is complete..._