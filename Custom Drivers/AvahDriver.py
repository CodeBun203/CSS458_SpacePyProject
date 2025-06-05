# Driver.py
import random # for the random tests
import os
import Body
import time
from Simulation import Simulation 
from Visualizer import run_anim

def two_suns():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "TwoSuns.csv"               # The file in the sub folder to read the planets from
    SIMULATION_NAME = "TwoSuns"             # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def lagrange_large():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "LagrangeLarge.csv"         # The file in the sub folder to read the planets from
    SIMULATION_NAME = "LagrangeLarge"       # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def perpendicular_planes():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10000.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "PerpendicularPlanes.csv"         # The file in the sub folder to read the planets from
    SIMULATION_NAME = "PerpendicularPlanes"       # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def lagrange_stable():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "LagrangeStable.csv"         # The file in the sub folder to read the planets from
    SIMULATION_NAME = "LagrangeStable"       # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)


def random_velocities():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "RandomVelocities.csv"         # The file in the sub folder to read the planets from
    SIMULATION_NAME = "RandomVelocities"       # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def swap_body_pos():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "SwapBodyPos.csv"         # The file in the sub folder to read the planets from
    SIMULATION_NAME = "SwapBodyPos"       # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def random_masses():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "RandomMasses.csv"           # The file in the sub folder to read the planets from
    SIMULATION_NAME = "RandomMasses"         # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def distribute_sun_mass():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 100.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "DistributeSunMass.csv"           # The file in the sub folder to read the planets from
    SIMULATION_NAME = "DistributeSunMass"         # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = True               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def remove_two_bodies():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10000.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "RemoveTwoBodies.csv"           # The file in the sub folder to read the planets from
    SIMULATION_NAME = "RemoveTwoBodies"         # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def remove_one_body():
    # Adjust these variables to adjust simulation
    SIMULATION_DURATION_YEARS = 10000.0        # Total duration in years
    TIME_STEP_MONTHS = .1                   # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                            # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months
    STARTING_DATA_FOLDER = "StartingData"   # The sub folder holding starting data
    FILE_NAME = "RemoveOneBody.csv"           # The file in the sub folder to read the planets from
    SIMULATION_NAME = "RemoveOneBody"         # The name of the simulation. Used to save simulation data to dsik.
    DISPLAY_ANIMATION = False               # Set to true if you want the simulation to display an animation. Does not work on Spyder.

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
    
    # Visualization
    if (DISPLAY_ANIMATION):
        print("Animating simulation...")
        run_anim(SIMULATION_NAME)

def main():
# Initial Conditions: 
# Mass in Earth Masses, Position in AU, Velocity in km/s 
# For each test, values are changed

#For these tests: the duration is 10,000 years
# Jupiter is removed
    remove_one_body()
#Jupiter and Venus are removed
    remove_two_bodies()
# Perpendicular Planes
    perpendicular_planes()

# For these tests: the duration is 100 years
# Sun's Mass is distributed to the other planets
    distribute_sun_mass()
# Randomizing masses
    random_masses()
#Swapping placing of planets
    swap_body_pos()
# Random Velocities
    random_velocities()
# Lagrange Stability
# How does the distance from both bodies change over time?
    lagrange_stable()
# Lagrange points with a larger mass (using Jupiter's Mass)
    lagrange_large()
# Two Suns
    two_suns()

if __name__ == '__main__':
    main()
    
