***COMPENG 2DX4 Final Project***

The microcontroller source code can be found under /src with the main file called 2dx4_ds90-1.c

The Python script that captures the data and plots the output can be found in visualization/2DX4Project-DA-Visualizaton-hassaa73.py 

Feel free to read through the project report for a more detailed description of the project, and the theory behind it.

***General Description***

The embedded spatial measurement system generates a 3-Dimensional render of the surrounding area using the VL53L1X Time-of-Flight sensor. By attaching the sensor to the 28BYJ-48 Stepper Motor we are able to capture 32 points on the Y-Z plane, and by moving the system on the X axis and taking multiple scans, a 3D render can be created. The system consists of the VL53L1X Time-of-Flight sensor, the 28BYJ-48 Stepper Motor, the MSP432E401Y microcontroller and a laptop. 

The Time-of-Flight sensor captures distance data using LIDAR technology. It uses infrared light as a pulsated laser to measure the distances, this is done by calculating the amount of time required for the emitted light to return to the sensor. The sensor's internal Analog-to-Digital converter converts the analog data to digital data to be sent to the microcontroller.  The 28BYJ-48 Stepper Motor rotates 11.25 degrees between scans, allowing the sensor to capture 32 data points.
The MSP432E401Y microcontroller powers and controls the stepper motor as well as the ToF sensor. The distance data is communicated to the microcontroller using 12C from the ToF sensor; This is then communicated to the computer using UART and a baud rate of 115200.

The distance data is read byte by byte and collected together until a newline/enter character is received, the distance data is then parsed and converted from cylindrical coordinates to xyz coordinates, this data is then written to a .xyz file.  The xyz file is then read in by the script, and a mesh is created by connecting points within an individual plane together then connecting the following planes together. A 3D render is then created using Open3D for visualization.
