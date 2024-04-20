# Installation Guide For Train Model Test Bench :)

##### Pre Requisite Instalations
1. Python 3.11 or later
2. pyqt6

   pip install PyQt6

##### Required Files From Our GitHub
1. the entire contents of the Train_Model directory
2. the entire contents of the Train_Controller_HW directory
3. the entire contents of the Train_Controller_SW directory

##### Using the Train Model Test Bench
In the Train_Model directory launch the file train_model_container_testbench.py.
you will be faced with this UI:

![UI for container test bench](/test_bench_ui.png)

Using this UI is largely strait forward. first by pressing Add train you can add a train 
to the container, all trains in the container can be selected using the Train select combo 
box. Each button is associated to the text box above that, above that text box is the format 
of the data that needs to be input. So as an example with Train 1 selected and "12, 13" in the 
Track Model Inputs text box if you press the Track Model Inputs button it will update Train 1's
incoming commanded speed and authority to Train 1 to 12 and 13 respectively.


