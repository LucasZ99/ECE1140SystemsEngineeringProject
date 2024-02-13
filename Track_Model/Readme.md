Define excel input format:
-
Right now, Blue Line.xlsx is our ideal input file, 
we may want to add a direction of travel column
once our layouts are multi-directional

Inputs:
-
Commanded Speed (no action)

Vital authority (no action)

Switch positions (change value in tables and map)

Signal activation (change value in tables and map)

RR crossing activation (change value in tables and map)

Track presence (change block occupancy in tables and map, and send to track controller)

Disembarking passengers (to keep track of train occupancy so we can generate embarking passengers)

Broken rail failure (block occupancy)

Track circuit failure (block occupancy)

Power failure (block occupancy)

Track layout (to partially send to track controllers and for viewing table/map info)

Outputs:
-
Commanded Speed (unchanged)

Vital authority (unchanged)

Beacon (from excel input)

Ticket sales (randomly generated based off time)

Block occupancy (from track presence from train model)

{Embarking passengers}

{Track information}

Use cases:
-
1. Loading Track Layouts
2. Viewing Track Information (dynamic table)
3. Testing Failure Modes
4. Changing Track Temperature
5. Viewing Track Information (dynamic map)
