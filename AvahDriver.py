# Driver.py
from Body import Planetary_Body, Vector3
from Simulation import Simulation 
from Visualizer import animate_simulation, anim_data

def remove_two_bodies():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Mercury', 'mass_MEarth': 0.0553,   'pos_AU_components': [-0.177, -0.428, -0.046],  'vel_km_s_components': [36.2, -15.8, -4.4]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
        {'name': 'Mars',    'mass_MEarth': 0.107,    'pos_AU_components': [-1.08, -1.04, 0.038],   'vel_km_s_components': [16.4, -18.6, -0.7]},
        {'name': 'Saturn',  'mass_MEarth': 95.16,    'pos_AU_components': [9.32, -2.60, -0.32],   'vel_km_s_components': [2.6, 8.8, -0.2]},
        {'name': 'Uranus',  'mass_MEarth': 14.5,     'pos_AU_components': [15.5, 12.3, -0.19],   'vel_km_s_components': [-4.2, 5.0, 0.06]},
        {'name': 'Neptune', 'mass_MEarth': 17.1,     'pos_AU_components': [29.9, -1.06, -0.58],  'vel_km_s_components': [0.1, 5.4, -0.08]}
    ]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Vector3(*body_data['pos_AU_components'])
        vel_vec_kms = Vector3(*body_data['vel_km_s_components'])
        
        planet = Planetary_Body(
            mass_val=body_data['mass_MEarth'],
            pos_vector=pos_vec,
            vel_vector=vel_vec_kms,
            name_val=body_data['name']
        )
        list_of_bodies.append(planet)

    simulation_instance = Simulation(
        list_of_planetary_bodies=list_of_bodies,
        time_step_months=TIME_STEP_MONTHS
    )

    print(f"Starting simulation: Removing Jupiter and Venus from Solar System (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    remove_jupiter_and_venus = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print("Simulation finished.")

    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)
    
    # Visualization
    
    # print("Attempting to animate simulation...")
    # body_names = [body.name for body in simulation_instance.bodies]
    # body_masses = [body.mass for body in simulation_instance.bodies]
    # data = anim_data("Placeholder")
    # #animate_simulation(position_history_array, body_names, body_masses)
    # animate_simulation(data[0], data[1], data[2])

def remove_one_body():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Mercury', 'mass_MEarth': 0.0553,   'pos_AU_components': [-0.177, -0.428, -0.046],  'vel_km_s_components': [36.2, -15.8, -4.4]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
        {'name': 'Mars',    'mass_MEarth': 0.107,    'pos_AU_components': [-1.08, -1.04, 0.038],   'vel_km_s_components': [16.4, -18.6, -0.7]},
        {'name': 'Saturn',  'mass_MEarth': 95.16,    'pos_AU_components': [9.32, -2.60, -0.32],   'vel_km_s_components': [2.6, 8.8, -0.2]},
        {'name': 'Uranus',  'mass_MEarth': 14.5,     'pos_AU_components': [15.5, 12.3, -0.19],   'vel_km_s_components': [-4.2, 5.0, 0.06]},
        {'name': 'Neptune', 'mass_MEarth': 17.1,     'pos_AU_components': [29.9, -1.06, -0.58],  'vel_km_s_components': [0.1, 5.4, -0.08]}
    ]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Vector3(*body_data['pos_AU_components'])
        vel_vec_kms = Vector3(*body_data['vel_km_s_components'])
        
        planet = Planetary_Body(
            mass_val=body_data['mass_MEarth'],
            pos_vector=pos_vec,
            vel_vector=vel_vec_kms,
            name_val=body_data['name']
        )
        list_of_bodies.append(planet)

    simulation_instance = Simulation(
        list_of_planetary_bodies=list_of_bodies,
        time_step_months=TIME_STEP_MONTHS,
        sim_name = "remove_jupiter_and_venus"
    )

    print(f"Starting simulation: Removing Jupiter from Solar System (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    position_history_array = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print("Simulation finished.")

    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)
    
    # Visualization
    # print("Attempting to animate simulation...")
    # body_names = [body.name for body in simulation_instance.bodies]
    # body_masses = [body.mass for body in simulation_instance.bodies]
    # data = anim_data("Placeholder")
    # #animate_simulation(position_history_array, body_names, body_masses)
    # animate_simulation(data[0], data[1], data[2])

def main():
# Initial Conditions: Mass in Earth Masses, Position in AU, Velocity in km/s

# For this simulation, Jupiter will be removed
    #remove_one_body()

# For this simulation, Jupiter and Venus are removed
    remove_two_bodies()

if __name__ == '__main__':
    main()