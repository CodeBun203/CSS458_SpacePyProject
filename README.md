# CSS458_SpacePyProject

## Prerequisites
* VSCode (Updated to the latest version)
* Python 3 Interpreter

## How to Run
We recommend using VS Code for this project, as our visualization is an interactable 3D figure that IDEs like Spyder are unable to handle. When you do "plot.show()" in Spyder, the figure is interpreted as a 2D non-interactable image. 

## Driver Files
There are two different versions of the driver file. One version requires a CSV file with your data to be read into the driver, while the other version has your data hard-coded into the file. To visualize your simulation, these are the steps you need to take to have it run based on the version of driver you wish to use:

**CSV Read In:** Change the visualization variable from 'False' to 'True'. 

**Hard-Code:** 
* In the section of the function below, change the name to something meaningful to what you're using this simulation for. 
```
simulation_instance = Simulation(
    list_of_planetary_bodies=list_of_bodies,
    time_step_months=TIME_STEP_MONTHS,
    name = "NameofYourSimulation" # You will change the name here inside the quotations
)
```
* Uncomment out the code under 'Visualization' and change the name of the file to the same name you used in the other section. 
```
#Visualization
    print("Attempting to animate simulation...")
    body_names = [body.name for body in simulation_instance.bodies]
    body_masses = [body.mass for body in simulation_instance.bodies]
    data = anim_data("NameofYourSimulation") # This should be the exact same as what you used up top, including the quotations
    animate_simulation(data[0], data[1], data[2])
```
* Run your driver like normal.
