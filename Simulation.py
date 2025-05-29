# simulation.py
# Designed to work with the "Body.py"

import numpy as np
from Body import Planetary_Body, Vector3 

class Simulation:
    """
    Manages and runs an N-body gravitational simulation using object-oriented
    methods from the Planetary_Body class.
    """

    def __init__(self, list_of_planetary_bodies, time_step_days=1.0):
        """
        Initializes the simulation.

        Args:
            list_of_planetary_bodies (list[Planetary_Body]): A list of pre-initialized 
                                                             Planetary_Body objects.
            time_step_days (float): The duration of each simulation step in days.
                                    This must be consistent with the units used
                                    within Planetary_Body (AU, MEarth, days).
        """
        if not all(isinstance(pb, Planetary_Body) for pb in list_of_planetary_bodies):
            raise TypeError("All items in list_of_planetary_bodies must be instances of Planetary_Body.")
            
        self.bodies = list_of_planetary_bodies  # Store the list of Planetary_Body objects
        self.dt_days = float(time_step_days)    # Time step for the simulation in days
        
        self.body_names = [body.name for body in self.bodies] # For visualization/logging
        
        # This list will store a snapshot of all body positions at each time step
        self.position_history = []

    def run_simulation(self, total_duration_years):
        """
        Runs the N-body simulation for a specified total duration.

        The simulation loop follows these steps for each time increment (dt):
        1. Calculate Net Forces: For each body, calculate the sum of gravitational
           forces exerted on it by all other bodies.
        2. Update Velocities: Using the net force and mass (F=ma), update each
           body's velocity over the time step (dv = a*dt).
        3. Update Positions: Using the new velocity, update each body's position
           over the time step (dx = v*dt).
        4. Record State: Store the positions for later animation/analysis.

        Args:
            total_duration_years (float): The total duration for which to run the simulation, in years.

        Returns:
            numpy.ndarray: An array containing the history of positions for all bodies.
                           Shape: (num_steps, num_bodies, 3)
        """
        if not isinstance(total_duration_years, (int, float)) or total_duration_years <= 0:
            raise ValueError("total_duration_years must be a positive number.")

        num_simulation_steps = int(total_duration_years * 365.25 / self.dt_days)
        
        print(f"Running N-body simulation for {total_duration_years:.2f} years "
              f"with a {self.dt_days:.2f}-day time step ({num_simulation_steps} steps)...")
        
        # --- Main Simulation Loop ---
        for step_num in range(num_simulation_steps):
            
            # Print progress every N steps if desired
            if num_simulation_steps > 100 and step_num % (num_simulation_steps // 20) == 0 and step_num > 0:
                 print(f"  Processed step {step_num}/{num_simulation_steps} ({(step_num/num_simulation_steps*100):.0f}%)")
            
            # --- Calculate Net Gravitational Forces on Each Body ---
            net_forces_on_bodies = [Vector3(0, 0, 0) for _ in self.bodies] # Create vector for each body

            # Loop through all pairs of bodies to calculate forces
            for i, target_body in enumerate(self.bodies):
                for j, acting_body in enumerate(self.bodies):
                    if i == j:
                        continue
                    
                    force_vector = Planetary_Body.calculate_gravitational_force_exerted_by_on(
                        acting_body=acting_body,
                        target_body=target_body
                    )
                    net_forces_on_bodies[i] = net_forces_on_bodies[i] + force_vector
            
            # --- 2. Update Velocities of All Bodies ---
            for i, body in enumerate(self.bodies):
                body.update_velocity_from_net_force(
                    net_forces_on_bodies[i],
                    self.dt_days
                )

            # --- 3. Update Positions of All Bodies ---
            for body in self.bodies:
                body.update_position(self.dt_days)
            
            # --- 4. Record the Positions for this Time Step ---
            current_positions_snapshot = [body.pos.to_list() for body in self.bodies]
            self.position_history.append(current_positions_snapshot)
            
        print("Simulation complete.")
        
        return np.array(self.position_history)

#==============================================================================
# Example Usage (similar to how run_simulation.py would use it)
#==============================================================================
if __name__ == "__main__":
    print("This is the Simulation class definition. To run a simulation, "
          "create instances of Planetary_Body, then an instance of Simulation, "
          "and call its run_simulation() method in Driver.py.")

    try:
        sun = Planetary_Body(name_val="Sun", mass_val=333000.0, 
                             pos_vector=Vector3(0,0,0), vel_vector=Vector3(0,0,0))
        earth = Planetary_Body(name_val="Earth", mass_val=1.0, 
                               pos_vector=Vector3(1.0,0,0), vel_vector=Vector3(0,0.0172,0))

        simple_sim = Simulation(list_of_planetary_bodies=[sun, earth], time_step_days=1.0)

        print("\nRunning a simple 2-body test simulation (Sun and Earth for 10 days):")
        position_history = simple_sim.run_simulation(total_duration_years=(10/365.25))
        
        print(f"\nSimulation finished. {len(position_history)} time steps recorded.")
        print(f"Initial position of Earth: {position_history[1][0]}")
        print(f"Initial position of Sun: {position_history[1][1]}")
        print(f"Final position of Earth: {simple_sim.bodies[1].pos}")
        print(f"Final position of Sun: {simple_sim.bodies[0].pos}")

    except ImportError:
        print("Could not import Planetary_Body or Vector3 from Body.py. "
              "Make sure Body.py (corrected version) is in the same directory.")
    except Exception as e:
        print(f"An error occurred during the example: {e}")