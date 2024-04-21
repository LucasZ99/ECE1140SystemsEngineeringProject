# Track Controller (Software)

## About

Track Controller software controls two sections of the Green Line, sections A and C which contain the
loops and two-way sections of the track

## Running Track Controller Module on its own:

Navigate to Track_Controller_SW/TrackControllerContainer.py and run main()

This will open UI's for both sections A and C, as well as starting the backend processes for all three
track controllers on the green line.

This will also start the testbench for the entire track controller module (both HW and SW)

# How to use the module

1. Configuration: Upload PLC Programs: A default PLC program for each module is included on startup
   for ease of use.
   
   - To upload a file directly, select Upload File. A file browser is shown. The file that _must_ be
     used for proper operation is
     
       /Track_Controller_SW/PLCProgramSectionA.py for Track Controller A
       /Track_Controller_SW/PLCProgramSectionC.py for Track Controller C
     
    - The current filename is indicated above the Upload File button

_**You MUST upload files (or use the preuploaded files) to both Track Controller UI's before continuing**_

## Background Information

1. Switch Position, Block Occupancy, and Light / Railroad status indicators are all read only fields that
   reflect the state of the system.
   
   - Track Controller A controls blocks 1-32 for green line, which includes switches at blocks 13 and 28,
     and a railroad crossing at block 19
   - Track Controller C controls blocks 77 - 104 for green line, which includes switches at blocks 77 and 86

2. The PLC programs for the track controllers control the state of switches, lights, and railroad crossings
   as well as safe travel speed for the trains
   
   - The plc program updates the safe system state whenever there is a new block occupancy detected
     in the system.

## Integrated Operation

1. In the fully integrated system, inputs to the Track Controllers are sent directly from the CTC
   and Track Model
2. The only operation aside from Uploading a PLC file on program startup is a Maintenance Mode switch toggle.
   
   - Click Maintenance Mode in either UI
   - select a switch to toggle. If it's safe, the switch will toggle and the new switch and light statuses
     will be reflected in the UI.
   - If it's not safe, nothing will update.

## Using the Testbench to Simulate Inputs

1. To observe the results of the PLC program's execution on the track state:
   
   - toggle the desired block occupancies in the Track Model to Wayside Section of the testbench, and
     click _Send Input_.
   - The track controller UI's will reflect the new state of the system
     
2. To observe the Track Controller's handling / modification of CTC to Wayside inputs:
   
   - first make sure there is some occupancy on the track, even if it's none by clicking _Send Input_
     from above
   - This generates a PLC result that is used to process a CTC Track Signal and maintenance mode operations
     
3. To send a track signal (authority and speed update):
   
   - select a block
   - assign an authority
   - enter a non-negative speed.
   - Press _Send Input_.
     
4. To simulate the switch toggle and close/open block functionality:
   
   - select a switch to toggle or a block to close/open
   - press _Send Input_
     
5. The track controller will output to console messages that are sent to either the CTC or Track Model after inputs