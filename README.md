# openfoam_residuals_monitor

## Description
This Python script allows the user to monitor the residuals of their simulation in real-time while it is running, through a dashboard in their browser. It reads the log file to retrieve the data and plots the residuals of some variables as well as the continuity. Additionally, this program analyzes the variables I generally use in my simulations due to the solvers and turbulence models I work with, but feel free to modify it according to your needs.

## Example of Use
1. Make sure that the log file already exists (either by running the simulation before the script or creating the file using `touch` in the Linux terminal).
2. In the script, set the `log_file` variable to your log file.
3. Run the script and open the server started by the script (typically at `http://127.0.0.1:8080/`).
   
* An example log file can be found in the files.