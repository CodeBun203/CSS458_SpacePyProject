# Driver.py
import Body
import time
from Simulation import Simulation 
from Visualizer import animate_simulation, anim_data, run_anim

def run_sim_with_G(G, sim_name, display_anim = False, overide_max_range = -1, block=False):
    Body._G_ASTRO_DAYS_REF = G
    Body.G_ASTRO_MONTHS = Body._G_ASTRO_DAYS_REF * (Body.DAYS_PER_MONTH**2)
    SIMULATION_DURATION_YEARS = 5.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    # Initial Conditions: Mass in Earth Masses, Position in AU, Velocity in km/s
    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
    ]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Body.Vector3(*body_data['pos_AU_components'])
        vel_vec_kms = Body.Vector3(*body_data['vel_km_s_components'])
        
        planet = Body.Planetary_Body(
            mass_val=body_data['mass_MEarth'],
            pos_vector=pos_vec,
            vel_vector=vel_vec_kms,
            name_val=body_data['name']
        )
        list_of_bodies.append(planet)
    simulation_instance = Simulation(
        list_of_planetary_bodies=list_of_bodies,
        time_step_months=TIME_STEP_MONTHS, name=sim_name
    )
    temp_time = time.time()
    print(f"Starting simulation from Driver.py (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    position_history_array = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print(f"Simulation finished. Elapsed time: {time.time() - temp_time}")


    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)
    
    # Visualization
    if (display_anim):
        print("Attempting to animate simulation...")
        body_names = [body.name for body in simulation_instance.bodies]
        body_masses = [body.mass for body in simulation_instance.bodies]
        data = anim_data(sim_name)
        #animate_simulation(position_history_array, body_names, body_masses)
        animate_simulation(data[0], data[1], data[2], overide_max_range, block)


def get_data():
    import numpy as np

    # Control Variables
    default_G = Body._G_ASTRO_DAYS_REF
    min_perc = 0.5
    max_perc = 1.5
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
    max_perc = 1.5
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
        run_anim(sim_name + str(scaled_steps[i]), 3)

def view_sim(folder_name):
    run_anim(folder_name)

if __name__ == '__main__':
    #get_data()
    play_animations()
    


    