# openfoam_residuals_monitor

## Description
This Python script, referred to as **"residuals_monitor.py"**, allows the user to monitor the residuals of their simulation in real-time while it is running, through a dashboard in their browser. It reads the log file to retrieve the data and plots the residuals of some variables as well as the continuity. Additionally, this program analyzes the variables I generally use in my simulations due to the solvers and turbulence models I work with, but feel free to modify it according to your needs.

Furthermore, there is another script named **"residuals_plot.py"** that has been created to save the residual graphs as .png images.


## Example of Use **residuals_monitor.py**
1. Make sure that the log file already exists (either by running the simulation before the script or creating the file using `touch` in the Linux terminal).
2. In the script, set the `log_file` variable to your log file.
3. Run the script and open the server started by the script (typically at `http://127.0.0.1:8080/`).
   
* An example log file can be found in the files.

## Example of Use **residuals_plot.py**
1. After the simulation is complete, copy the script to the simulation folder.
2. In the script, set the `log_file` variable to your log file.
3. Run the code. A "figures" folder will be created containing two .png files related to the simulation residuals.

* An example log file can be found in the files.