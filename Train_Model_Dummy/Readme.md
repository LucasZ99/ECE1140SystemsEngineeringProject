## Train Model Dummy

Since we had issues integrating with the train model and train controller, we made a train model dummy to show
functionality of the CTC, Track Controllers, and Track Model for Green Line. This module has no UI, and it is started
automatically when ece1140-tovarish/CTCWaysideTrackModelUI.py is run. 

### Functionality

The train model dummy calculates a change in position for each train when it receives a non-zero authority and speed 
based on a simple d = vt calculation for each train. It communicates with the track model to show trains moving 
through the system. Additionally, trains are automatically spawned when a non-zero speed and authority are sent to 
block 62 (the yard block), and they are de-spawned when it returns to the yard (after block 57).

