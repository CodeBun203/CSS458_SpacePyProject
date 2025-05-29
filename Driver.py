# Driver.py
# This script sets up and runs the N-body planetary simulation.
from Body import Planetary_Body, Vector3
from Simulation import Simulation 
# visualizer.py is assumed to be the same as the original version that works with NumPy arrays
from Visualizer import animate_simulation 

def get_km_s_to_au_day_conversion_factor():
    """
    Calculates and returns the conversion factor from km/s to AU/day.
    1 km = 1 / 149,597,870.7 AU
    1 s = 1 / (24 * 60 * 60) day
    """
    AU_IN_KM = 149597870.7  # Kilometers in one Astronomical Unit
    SECONDS_IN_DAY = 24.0 * 60.0 * 60.0
    return (1.0 / AU_IN_KM) * SECONDS_IN_DAY

def main():
    """
    Main function to define initial conditions, set up the simulation,
    run it, and then visualize the results.
    """
    # --- Simulation Parameters ---
    SIMULATION_DURATION_YEARS = 2.0  # Total duration of the simulation in years
    TIME_STEP_DAYS = 1.0             # Duration of each simulation step in days

    # --- Initial Conditions for Solar System Bodies ---
    # Date is approximately for January 1, 2025.
    # Units:
    #   Mass: Earth Masses (MEarth)
    #   Position: Astronomical Units (AU) from the Sun (assumed at origin for initial setup)
    #   Velocity: km/s (this will be converted to AU/day for consistency with Body.py)
    
    # Get the conversion factor using the helper function
    KM_PER_SECOND_TO_AU_PER_DAY = get_km_s_to_au_day_conversion_factor()

    # Data for the bodies
    # Note: For a more accurate simulation, initial positions and velocities 
    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Mercury', 'mass_MEarth': 0.0553,   'pos_AU_components': [-0.177, -0.428, -0.046],  'vel_km_s_components': [36.2, -15.8, -4.4]},
        {'name': 'Venus',   'mass_MEarth': 0.815,    'pos_AU_components': [-0.720, 0.065, 0.041],   'vel_km_s_components': [-3.4, -34.8, 1.8]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
        {'name': 'Mars',    'mass_MEarth': 0.107,    'pos_AU_components': [-1.08, -1.04, 0.038],   'vel_km_s_components': [16.4, -18.6, -0.7]},
        {'name': 'Jupiter', 'mass_MEarth': 317.8,    'pos_AU_components': [4.58, 2.11, -0.09],    'vel_km_s_components': [-5.4, 11.8, 0.1]},
        {'name': 'Saturn',  'mass_MEarth': 95.16,    'pos_AU_components': [9.32, -2.60, -0.32],   'vel_km_s_components': [2.6, 8.8, -0.2]},
        {'name': 'Uranus',  'mass_MEarth': 14.5,     'pos_AU_components': [15.5, 12.3, -0.19],   'vel_km_s_components': [-4.2, 5.0, 0.06]},
        {'name': 'Neptune', 'mass_MEarth': 17.1,     'pos_AU_components': [29.9, -1.06, -0.58],  'vel_km_s_components': [0.1, 5.4, -0.08]}
    ]

    # Create a list of Planetary_Body objects from the initial data
    list_of_bodies = []
    for body_data in solar_system_initial_data:

        pos_components = body_data['pos_AU_components']
        position_vector = Vector3(pos_components[0], pos_components[1], pos_components[2])
        
        vel_components_km_s = body_data['vel_km_s_components']
        velocity_vector_AU_day = Vector3(
            vel_components_km_s[0] * KM_PER_SECOND_TO_AU_PER_DAY,
            vel_components_km_s[1] * KM_PER_SECOND_TO_AU_PER_DAY,
            vel_components_km_s[2] * KM_PER_SECOND_TO_AU_PER_DAY
        )
        
        # Create the Planetary_Body instance
        planet = Planetary_Body(
            mass_val=body_data['mass_MEarth'],
            pos_vector=position_vector,
            vel_vector=velocity_vector_AU_day,
            name_val=body_data['name']
        )
        list_of_bodies.append(planet)

    # --- Setup and Run the Simulation ---
    # Instantiate the Simulation class with the list of bodies and the time step
    simulation_instance = Simulation(
        list_of_planetary_bodies=list_of_bodies,
        time_step_days=TIME_STEP_DAYS
    )

    # Run the simulation
    # The run_simulation method returns a NumPy array of position history
    position_history_array = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )

    # --- Visualize the Results ---
    # Complete this section to visualize the simulation results

if __name__ == '__main__':
    main()