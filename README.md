# CSS458_SpacePyProject User Manual

## Prerequisites
* VSCode (Updated to the latest version)
* Python 3 Interpreter

## How to Run
1. Please make sure you have the prerequisites installed.
2. We recommend using VS Code for this project as other IDEs, such as Spyder, behave strangely when displaying animations.
3. Open the UserDriver.py file in VSCode.
4. Specify the filename of a file in the 'StartingData' folder that you would like to run like so:
```
def main():

    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10.0
    TIME_STEP_MONTHS = .1
    STARTING_DATA_FOLDER = "StartingData"
    FILE_NAME = "Solar_System_Full_Initial.csv" <---------------
```
5. Run UserDriver to run the simulation. You will see an animation once it has completed.
6. If you would like to animate past simulations using the binary data in the 'dumps' folder, open Visualizer.py and specify the name of the binary file like so:
```
if __name__ == '__main__':
    run_anim("Moons")     <------------
```

## Driver Files
There are two different versions of the driver file; UserDriver, and [MemberName]Driver. UserDriver requires a CSV file with your data to be read into the driver, while the other versions hardcode the Planetary_Body data into the file. To visualize your simulation, these are the steps you need to take to have it run based on the version of driver you wish to use:

**UserDriver:** 
Change the visualization variable from 'False' to 'True'. 

**Hard-Code (AvahDriver):** 
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
