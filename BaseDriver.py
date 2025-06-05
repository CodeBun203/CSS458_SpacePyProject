# Driver.py
from Body import Planetary_Body, Vector3
from Simulation import Simulation 
from Visualizer import animate_simulation, anim_data

def main():
    SIMULATION_DURATION_YEARS = 10.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    # Initial Conditions: Mass in Earth Masses, Position in AU, Velocity in km/s
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

    print(f"Starting simulation from Driver.py (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    position_history_array = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print("Simulation finished.")

    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)
    
    # Visualization
    print("Attempting to animate simulation...")
    body_names = [body.name for body in simulation_instance.bodies]
    body_masses = [body.mass for body in simulation_instance.bodies]
    data = anim_data("Placeholder")
    animate_simulation(data[0], data[1], data[2])

if __name__ == '__main__':
    main()