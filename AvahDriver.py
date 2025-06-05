# Driver.py
import random # for the random tests
from Body import Planetary_Body, Vector3
from Simulation import Simulation 
from Visualizer import animate_simulation, anim_data

def two_suns():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    # Initial Conditions: Mass in Earth Masses, Position in AU, Velocity in km/s
    solar_system_initial_data = [
        {'name': 'Sun A',     'mass_MEarth': 333000.0, 'pos_AU_components': [-5.0, 0.0, 0.0],       'vel_km_s_components': [0.0, -2.0, 0.0]},
        {'name': 'Sun B',     'mass_MEarth': 333000.0, 'pos_AU_components': [5.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 2.0, 0.0]},
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
        time_step_months=TIME_STEP_MONTHS,
        name = "TwoSuns"
    )

    print(f"Starting Two Suns (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
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
    # data = anim_data("TwoSuns")
    # animate_simulation(data[0], data[1], data[2])

def lagrange_large():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
        
        #Using Jupiter's Mass
        {'name': 'Large Astroid',   'mass_MEarth': 317.8,    'pos_AU_components': [0.5, 0.866, 0.0],   'vel_km_s_components': [-25.8, 14.9, 0.0]},
      ]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Vector3(*body_data['pos_AU_components'])
        vel_vec_kms = Vector3(*body_data['vel_km_s_components'])
        2
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
        name = "LagrangeLargeMass"
    )

    print(f"Starting simulation: Lagrange Stability with a Larger mass (Jupiter's Mass) (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("LagrangeLargeMass")
    # animate_simulation(data[0], data[1], data[2])

def perpendicular_planes():
    SIMULATION_DURATION_YEARS = 10000.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (half a month)

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0,     0.0,    0.0],    'vel_km_s_components': [0.0,    0.0,    0.0]},
        {'name': 'Mercury', 'mass_MEarth': 0.0553,   'pos_AU_components': [-0.177, -0.428,  0.0],    'vel_km_s_components': [36.2,  -15.8,   0.0]},
        {'name': 'Venus',   'mass_MEarth': 0.815,    'pos_AU_components': [-0.720,  0.0,    0.065],  'vel_km_s_components': [-3.4,   0.0,  -34.8]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.0,     0.182,  0.967],  'vel_km_s_components': [0.0,  -29.9,    5.6]},
        {'name': 'Mars',    'mass_MEarth': 0.107,    'pos_AU_components': [-0.76,  -0.76,   0.038],  'vel_km_s_components': [13.0, -21.0,  -0.7]},
        {'name': 'Jupiter', 'mass_MEarth': 317.8,    'pos_AU_components': [4.58,    0.0,    2.11],   'vel_km_s_components': [-5.4,   0.0,   11.8]},
        {'name': 'Saturn',  'mass_MEarth': 95.16,    'pos_AU_components': [0.0,     9.32,  -2.60],   'vel_km_s_components': [0.0,    2.6,    8.8]},
        {'name': 'Uranus',  'mass_MEarth': 14.5,     'pos_AU_components': [10.0,   10.0,   10.0],    'vel_km_s_components': [-4.2,   5.0,    0.06]},
        {'name': 'Neptune', 'mass_MEarth': 17.1,     'pos_AU_components': [29.9,  -1.06,  -0.58],   'vel_km_s_components': [0.1,    5.4,   -0.08]}
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
        name = "PerpendicularPlanes"
    )

    print(f"Starting Perpendicular planes of planets to each other (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
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
    # data = anim_data("PerpendicularPlanes")
    # animate_simulation(data[0], data[1], data[2])

def lagrange_stable():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, 'pos_AU_components': [0.0, 0.0, 0.0],       'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Earth',   'mass_MEarth': 1.0,      'pos_AU_components': [0.182, 0.967, 0.0],     'vel_km_s_components': [-29.9, 5.6, 0.0]},
        
        #Small Astroid is starting at L2
        {'name': 'Small Astroid',   'mass_MEarth': 0.001,    'pos_AU_components': [0.5, 0.866, 0.0],   'vel_km_s_components': [-25.8, 14.9, 0.0]},
      ]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Vector3(*body_data['pos_AU_components'])
        vel_vec_kms = Vector3(*body_data['vel_km_s_components'])
        2
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
        name = "LagrangeStability"
    )

    print(f"Starting simulation: Lagrange Stability (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("LagrangeStability")
    # animate_simulation(data[0], data[1], data[2])


def random_velocities():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

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

    planet_velocities = [body['vel_km_s_components'] for body in solar_system_initial_data[1:]]
    random.shuffle(planet_velocities)

    for i, body in enumerate(solar_system_initial_data[1:]):
        body['vel_km_s_components'] = planet_velocities[i]

    list_of_bodies = []
    for body_data in solar_system_initial_data:
        pos_vec = Vector3(*body_data['vel_km_s_components'])
        vel_vec_kms = Vector3(*body_data['vel_km_s_components'])
        2
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
        name = "RandomVelocities"
    )

    print(f"Starting simulation: Random Velocities (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("RandomVelocities")
    # animate_simulation(data[0], data[1], data[2])

def swap_body_pos():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

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

    planet_positions = [body['pos_AU_components'] for body in solar_system_initial_data[1:]]
    random.shuffle(planet_positions)

    for i, body in enumerate(solar_system_initial_data[1:]):
        body['pos_AU_components'] = planet_positions[i]

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
        name = "SwapBodyPositions"
    )

    print(f"Starting simulation: Swapping positions of some planets (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("SwapBodyPositions")
    # animate_simulation(data[0], data[1], data[2])

def random_masses():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 306937.2919, 'pos_AU_components': [0.0, 0.0, 0.0],         'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Mercury', 'mass_MEarth': 230764.9023, 'pos_AU_components': [-0.177, -0.428, -0.046], 'vel_km_s_components': [36.2, -15.8, -4.4]},
        {'name': 'Venus',   'mass_MEarth': 235339.9342, 'pos_AU_components': [-0.720, 0.065, 0.041],   'vel_km_s_components': [-3.4, -34.8, 1.8]},
        {'name': 'Earth',   'mass_MEarth': 303867.2151, 'pos_AU_components': [0.182, 0.967, 0.0],      'vel_km_s_components': [-29.9, 5.6, 0.0]},
        {'name': 'Mars',    'mass_MEarth': 133286.7796, 'pos_AU_components': [-1.08, -1.04, 0.038],    'vel_km_s_components': [16.4, -18.6, -0.7]},
        {'name': 'Jupiter', 'mass_MEarth': 151296.3372, 'pos_AU_components': [4.58, 2.11, -0.09],      'vel_km_s_components': [-5.4, 11.8, 0.1]},
        {'name': 'Saturn',  'mass_MEarth': 85125.6718, 'pos_AU_components': [9.32, -2.60, -0.32],     'vel_km_s_components': [2.6, 8.8, -0.2]},
        {'name': 'Uranus',  'mass_MEarth': 230582.5226, 'pos_AU_components': [15.5, 12.3, -0.19],      'vel_km_s_components': [-4.2, 5.0, 0.06]},
        {'name': 'Neptune', 'mass_MEarth': 272800.4739, 'pos_AU_components': [29.9, -1.06, -0.58],     'vel_km_s_components': [0.1, 5.4, -0.08]}
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
        name = "RandomMasses"
    )

    print(f"Starting simulation: All Planets have Random Masses (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("RandomMasses")
    # animate_simulation(data[0], data[1], data[2])

def distribute_sun_mass():
    SIMULATION_DURATION_YEARS = 100.0  # Total duration in years
    TIME_STEP_MONTHS = .1           # Simulation time step in months (e.g., 0.1 months ~ 3 days)
                                     # Or use daily steps: (1.0 / (365.25 / 12.0)) for 1 day in months

    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 37049.6153, 'pos_AU_components': [0.0, 0.0, 0.0],         'vel_km_s_components': [0.0, 0.0, 0.0]},
        {'name': 'Mercury', 'mass_MEarth': 37049.6153, 'pos_AU_components': [-0.177, -0.428, -0.046], 'vel_km_s_components': [36.2, -15.8, -4.4]},
        {'name': 'Venus',   'mass_MEarth': 37049.6153, 'pos_AU_components': [-0.720, 0.065, 0.041],   'vel_km_s_components': [-3.4, -34.8, 1.8]},
        {'name': 'Earth',   'mass_MEarth': 37049.6153, 'pos_AU_components': [0.182, 0.967, 0.0],      'vel_km_s_components': [-29.9, 5.6, 0.0]},
        {'name': 'Mars',    'mass_MEarth': 37049.6153, 'pos_AU_components': [-1.08, -1.04, 0.038],    'vel_km_s_components': [16.4, -18.6, -0.7]},
        {'name': 'Jupiter', 'mass_MEarth': 37049.6153, 'pos_AU_components': [4.58, 2.11, -0.09],      'vel_km_s_components': [-5.4, 11.8, 0.1]},
        {'name': 'Saturn',  'mass_MEarth': 37049.6153, 'pos_AU_components': [9.32, -2.60, -0.32],     'vel_km_s_components': [2.6, 8.8, -0.2]},
        {'name': 'Uranus',  'mass_MEarth': 37049.6153, 'pos_AU_components': [15.5, 12.3, -0.19],      'vel_km_s_components': [-4.2, 5.0, 0.06]},
        {'name': 'Neptune', 'mass_MEarth': 37049.6153, 'pos_AU_components': [29.9, -1.06, -0.58],     'vel_km_s_components': [0.1, 5.4, -0.08]}
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
        name = "EvenDistributeSunMass"
    )

    print(f"Starting simulation: Sun's Mass evenly distributed to the other planets (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
        total_duration_years=SIMULATION_DURATION_YEARS
    )
    print("Simulation finished.")

    print("\nFinal states of bodies (Pos in AU, Vel in km/s):")
    for body in simulation_instance.bodies:
        print(body)

    #Visualization
    # print("Attempting to animate simulation...")
    # body_names = [body.name for body in simulation_instance.bodies]
    # body_masses = [body.mass for body in simulation_instance.bodies]
    # data = anim_data("EvenDistributeSunMass")
    # animate_simulation(data[0], data[1], data[2])

def remove_two_bodies():
    SIMULATION_DURATION_YEARS = 10000.0  # Total duration in years
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
        name = "RemoveTwobodies"
    )

    print(f"Starting simulation: Removing Jupiter and Venus from Solar System (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("RemoveTwobodies")
    # animate_simulation(data[0], data[1], data[2])

def remove_one_body():
    SIMULATION_DURATION_YEARS = 10000.0  # Total duration in years
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
        name = "RemoveOneBody"
    )

    print(f"Starting simulation: Removing Jupiter from Solar System (duration: {SIMULATION_DURATION_YEARS} years, step: {TIME_STEP_MONTHS:.4f} months)...")
    sim = simulation_instance.run_simulation(
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
    # data = anim_data("RemoveOneBody")
    # animate_simulation(data[0], data[1], data[2])

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
    
