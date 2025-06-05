# Driver.py
import time
import os
import Body
from Simulation import Simulation 
from Visualizer import run_anim

def main():

    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "Sun_To_Mars.csv"           # The file in the sub folder to read the planets from
    SIMULATION_NAME = "Sun_To_Mars"         # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = True                # Set to true if you want the simulation to display an animation. Does not work on Spyder.

    # Load Planets from the starting conditions file
    system = Body.read_system(STARTING_DATA_FOLDER + os.sep + FILE_NAME)

    # Create the simulation object
    simulation_instance = Simulation(
        list_of_planetary_bodies=system,
        time_step_months=TIME_STEP_MONTHS,
        name = SIMULATION_NAME
    )

    # Run the simulation and display elapsed tim
    start_time = time.time()
    print("Starting " + SIMULATION_NAME + f" simulation from Driver.py (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print(f"Simulation finished. Elapsed time: {time.time() - start_time}")
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

if __name__ == '__main__':
   main()