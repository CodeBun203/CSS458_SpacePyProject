# Driver.py
import Body
import time
import os
from Simulation import Simulation 
from Visualizer import run_anim

def run_sim_with_G(G, sim_name, display_anim = False, overide_max_range = -1):
    Body._G_ASTRO_DAYS_REF = G
    Body.G_ASTRO_MONTHS = Body._G_ASTRO_DAYS_REF * (Body.DAYS_PER_MONTH**2)

    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "Grav_Constant_Test.csv"    # The file in the sub folder to read the planets from
    SIMULATION_NAME = sim_name              # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = display_anim        # Set to true if you want the simulation to display an animation. Does not work on Spyder.

    # Load Planets from the starting conditions file
    system = Body.read_system(STARTING_DATA_FOLDER + os.sep + FILE_NAME)

    # Create the simulation object
    simulation_instance = Simulation(
        list_of_planetary_bodies=system,
        time_step_months=TIME_STEP_MONTHS,
        name = SIMULATION_NAME
    )

    # Run the simulation and display elapsed time
    start_time = time.time()
    print("Starting " + SIMULATION_NAME + f" simulation from Driver.py (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print(f"Simulation finished. Elapsed time: {time.time() - start_time}")


    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME, overide_max_range)


def get_data():
    import numpy as np

    # Control Variables
    default_G = Body._G_ASTRO_DAYS_REF
    min_perc = 0.5
    max_perc = 2
    num_runs = 11
    center_bias = 0.75
    sim_name = "GravConstant_"

    # Get a set of values with a concentration near the default value
    start = min_perc * default_G
    end = max_perc * default_G
    even_steps = np.linspace(-1, 1, num_runs)
    concentrated_steps = np.sign(even_steps) * np.abs(even_steps)**(1 / center_bias)
    scaled_steps = (concentrated_steps + 1) / 2 * (end - start) + start
    
    for i in range(0, num_runs): 
        run_sim_with_G(scaled_steps[i], sim_name + str(scaled_steps[i]), True, 3)
    
def play_animations():
    import numpy as np

    # Control Variables
    default_G = Body._G_ASTRO_DAYS_REF
    min_perc = 0.5
    max_perc = 2
    num_runs = 11
    center_bias = 0.75
    sim_name = "GravConstant_"

    # Get a set of values with a concentration near the default value
    start = min_perc * default_G
    end = max_perc * default_G
    even_steps = np.linspace(-1, 1, num_runs)
    concentrated_steps = np.sign(even_steps) * np.abs(even_steps)**(1 / center_bias)
    scaled_steps = (concentrated_steps + 1) / 2 * (end - start) + start
    
    for i in range(0, num_runs):
        #run_anim(sim_name + str(scaled_steps[i]), 3)
        pass
    run_anim(sim_name + str(scaled_steps[0]), 3)
    run_anim(sim_name + str(scaled_steps[-1]), 3)

def view_sim(folder_name):
    run_anim(folder_name)

if __name__ == '__main__':
    #get_data()
    play_animations()
    


    