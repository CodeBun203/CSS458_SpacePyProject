# Simulation.py
import numpy as np
import time # For time-based dumping
import copy # For deepcopying system states
from Body import Planetary_Body, Vector3, KM_PER_S_TO_AU_PER_MONTH,\
    CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH, AU_PER_MONTH_TO_KM_PER_SECOND
import SimIO # Your friend's SimIO.py that uses pickle

class Simulation:
    """
    Manages and runs an N-body gravitational simulation using RK4 integration.
    Time step is in months. Positions are AU, Velocities are km/s.
    Periodically saves simulation state using SimIO.dump_history_pickle.
    """
    def __init__(self, list_of_planetary_bodies, time_step_months=0.1,
                 simulation_name="DefaultSim", 
                 # dump_interval_seconds allows overriding SimIO.MIN_DUMP_TIME if needed
                 dump_interval_seconds=None): 
        
        if not all(isinstance(pb, Planetary_Body) for pb in list_of_planetary_bodies):
            raise TypeError("All items must be Planetary_Body instances.")
            
        self.bodies = list_of_planetary_bodies
        self.dt_months = float(time_step_months) 
        self.body_names = [body.name for body in self.bodies]
        
        # For in-memory trajectory for immediate visualization of the current run
        self.position_history = [] 
        if self.bodies: # Ensure bodies list is not empty
            try:
                self.position_history.append([body.pos.to_list() for body in self.bodies])
            except AttributeError: # Fallback if .to_list() isn't on Vector3
                self.position_history.append([[body.pos.x, body.pos.y, body.pos.z] for body in self.bodies])


        # SimIO related attributes
        self.simulation_name = simulation_name
        if dump_interval_seconds is not None:
            self.dump_interval_seconds = float(dump_interval_seconds)
        elif hasattr(SimIO, 'MIN_DUMP_TIME'): # Check if MIN_DUMP_TIME is defined in SimIO
            self.dump_interval_seconds = float(SimIO.MIN_DUMP_TIME)
        else:
            self.dump_interval_seconds = 600.0 # Default fallback if not in SimIO
            print(f"Simulation Warning: SimIO.MIN_DUMP_TIME not found. Defaulting dump interval to {self.dump_interval_seconds}s.")


    def _get_system_state_derivatives(self, temp_system_state_bodies):
        # This method should be the same as the one from 
        # It uses Planetary_Body.calculate_gravitational_force_exerted_by_on
        num_bodies = len(temp_system_state_bodies)
        net_accelerations_AU_month_sq = [Vector3(0.0, 0.0, 0.0) for _ in range(num_bodies)]
        for i in range(num_bodies):
            target_body = temp_system_state_bodies[i]
            current_net_force_on_target = Vector3(0.0, 0.0, 0.0)
            for j in range(num_bodies):
                if i == j: continue
                acting_body = temp_system_state_bodies[j]
                force_vector = Planetary_Body.calculate_gravitational_force_exerted_by_on(
                    acting_body=acting_body, target_body=target_body)
                current_net_force_on_target = current_net_force_on_target + force_vector
            if target_body.mass != 0:
                net_accelerations_AU_month_sq[i] = current_net_force_on_target / target_body.mass
        
        pos_derivatives_AU_month = [b.velocity * KM_PER_S_TO_AU_PER_MONTH for b in temp_system_state_bodies]
        vel_derivatives_kms_month = [acc * CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH for acc in net_accelerations_AU_month_sq]
        return pos_derivatives_AU_month, vel_derivatives_kms_month

    def run_simulation(self, total_duration_years):
        total_duration_months = total_duration_years * 12.0
        if self.dt_months <= 0:
            print("Error: time_step_months must be positive.")
            return np.array(self.position_history) if self.position_history else np.empty((0,len(self.bodies) if self.bodies else 0,3))
            
        num_simulation_steps = int(total_duration_months / self.dt_months)
        if num_simulation_steps <= 0:
            print(f"Warning: num_simulation_steps is {num_simulation_steps}. Returning initial history.")
            return np.array(self.position_history) if self.position_history else np.empty((0,len(self.bodies) if self.bodies else 0,3))

        dt = self.dt_months; num_bodies = len(self.bodies)
        
        print(f"Running N-body simulation '{self.simulation_name}' for {total_duration_years:.2f} years "
              f"({total_duration_months:.2f} months) with a {self.dt_months:.4f}-month time step "
              f"({num_simulation_steps} steps) using RK4...")
        
        # --- SimIO Pickle Dumping Logic ---
        # sim_hist_chunk accumulates [ [Body, Body,...], [Body, Body,...], ... ] for one chunk
        sim_hist_chunk = [] 
        if self.bodies: # Add initial state (step 0) to the first chunk
            sim_hist_chunk.append(copy.deepcopy(self.bodies)) 
            
        last_dump_time_wallclock = time.time() # Wall clock time of last dump
        start_step_of_current_chunk = 0 # Simulation step index (0 to num_simulation_steps-1)

        for step_num in range(num_simulation_steps): # step_num from 0 to num_simulation_steps-1
            if num_simulation_steps > 20 and (step_num + 1) % max(1, (num_simulation_steps // 20)) == 0 :
                 print(f"  Processed step {step_num + 1}/{num_simulation_steps} ({( (step_num + 1.0)/num_simulation_steps*100):.0f}%)")
            
            # Use .copy() method from Body.py's Vector3 class
            y0_pos_AU = [b.pos.copy() for b in self.bodies]      
            y0_vel_kms = [b.velocity.copy() for b in self.bodies] 

            k1_pos, k1_vel = self._get_system_state_derivatives(self.bodies)
            
            # Using list comprehensions for creating temp_bodies for brevity and efficiency
            temp_bodies_k2 = [Planetary_Body(mass_val=m.mass, 
                                             pos_vector=p+(k1_p*(dt/2.0)), 
                                             vel_vector=v+(k1_v*(dt/2.0)), 
                                             name_val=m.name)
                              for m,p,v,k1_p,k1_v in zip(self.bodies, y0_pos_AU,y0_vel_kms, k1_pos,k1_vel)]
            k2_pos, k2_vel = self._get_system_state_derivatives(temp_bodies_k2)

            temp_bodies_k3 = [Planetary_Body(mass_val=m.mass, 
                                             pos_vector=p+(k2_p*(dt/2.0)), 
                                             vel_vector=v+(k2_v*(dt/2.0)), 
                                             name_val=m.name)
                              for m,p,v,k2_p,k2_v in zip(self.bodies, y0_pos_AU,y0_vel_kms, k2_pos,k2_vel)]
            k3_pos, k3_vel = self._get_system_state_derivatives(temp_bodies_k3)

            temp_bodies_k4 = [Planetary_Body(mass_val=m.mass, 
                                             pos_vector=p+(k3_p*dt), 
                                             vel_vector=v+(k3_v*dt), 
                                             name_val=m.name)
                              for m,p,v,k3_p,k3_v in zip(self.bodies, y0_pos_AU,y0_vel_kms, k3_pos,k3_vel)]
            k4_pos, k4_vel = self._get_system_state_derivatives(temp_bodies_k4)

            for i in range(num_bodies):
                avg_pos_deriv = (k1_pos[i] + (k2_pos[i]*2.0) + (k3_pos[i]*2.0) + k4_pos[i]) / 6.0
                self.bodies[i].pos = y0_pos_AU[i] + (avg_pos_deriv * dt)
                avg_vel_deriv = (k1_vel[i] + (k2_vel[i]*2.0) + (k3_vel[i]*2.0) + k4_vel[i]) / 6.0
                self.bodies[i].velocity = y0_vel_kms[i] + (avg_vel_deriv * dt)
            
            # Append current state to in-memory history for visualization
            try:
                self.position_history.append([b.pos.to_list() for b in self.bodies])
            except AttributeError: # Fallback if .to_list() isn't on Vector3
                self.position_history.append([[b.pos.x, b.pos.y, b.pos.z] for b in self.bodies])
            
            # Append deepcopy of current bodies state to the chunk for SimIO
            sim_hist_chunk.append(copy.deepcopy(self.bodies))
            
            # --- SimIO Pickle Dumping Check ---
            time_to_dump = (time.time() - last_dump_time_wallclock >= self.dump_interval_seconds)
            is_last_step = (step_num == num_simulation_steps - 1)

            if sim_hist_chunk and (time_to_dump or is_last_step):
                # SimIO.dump_history_pickle expects (system_hist_chunk, sim_name, chunk_start_step_idx, chunk_end_step_idx)
                # step_num is the index of the *last completed step* in this chunk (0 to N-1)
                print(f"  SimIO: Dumping history chunk for '{self.simulation_name}', steps {start_step_of_current_chunk} to {step_num}.")
                SimIO.dump_history_pickle(sim_hist_chunk, 
                                          self.simulation_name, 
                                          start_step_of_current_chunk, # This is the simulation step index
                                          step_num) 
                
                sim_hist_chunk = [] # Clear the chunk for next accumulation
                last_dump_time_wallclock = time.time()
                start_step_of_current_chunk = step_num + 1 # Next chunk starts after this step
        
        # Final check: if any remaining data in sim_hist_chunk (should ideally be empty if last step dumping worked)
        if sim_hist_chunk: 
             print(f"  SimIO: Dumping final remaining history chunk for '{self.simulation_name}', steps {start_step_of_current_chunk} to {num_simulation_steps-1}.")
             SimIO.dump_history_pickle(sim_hist_chunk, self.simulation_name, start_step_of_current_chunk, num_simulation_steps-1)

        print("Simulation complete.")
        return np.array(self.position_history)

if __name__ == "__main__":
    print("Simulation.py example with Pickle SimIO integration:")
    
    if 'SimIO' not in globals() or not hasattr(SimIO, 'dump_history_pickle'):
        class DummySimIO:
            MIN_DUMP_TIME = 600.0 
            def dump_history_pickle(self, hist, name, start_idx, end_idx):
                print(f"DummySimIO: Would dump pickle for '{name}', steps {start_idx}-{end_idx}, {len(hist)} states in chunk.")
        SimIO = DummySimIO()
        print("Warning: Using DummySimIO for Simulation.py standalone test.")

    try:
        # Ensure Body.py's Planetary_Body constructor matches these keywords
        sun = Planetary_Body(mass_val=333000.0, name_val="Sun")
        earth = Planetary_Body(mass_val=1.0, pos_vector=Vector3(1,0,0), vel_vector=Vector3(0,AU_PER_MONTH_TO_KM_PER_SECOND,0), name_val="Earth")
        
        test_sim_name = "SimPyPickleMainTest"
        test_dump_interval_seconds = 2.0 # Dump frequently for testing

        sim = Simulation(
            list_of_planetary_bodies=[sun, earth], 
            time_step_months=0.1, # ~3 day steps
            simulation_name=test_sim_name,
            dump_interval_seconds=test_dump_interval_seconds
        )

        duration_years = 0.05 # Simulate for a short period (0.05 * 12 / 0.1 = 6 steps)
        
        print(f"\nInitial Earth: {earth}")
        history = sim.run_simulation(duration_years)
        print(f"Simulation finished. In-memory history shape: {history.shape if isinstance(history, np.ndarray) else 'N/A'}.")
        print(f"Final Earth: {earth}")
        # Check the Dumps/SimPyPickleMainTest/ directory for files like 0.pkl, etc.
        # The filenames in SimIO.dump_history_pickle are based on the 'inital_time' argument.
        print(f"Check '{getattr(SimIO, 'DEFAULT_DUMPS_DIR', getattr(SimIO, 'DEFAULT_DUMP_PATH', 'Dumps'))}/{test_sim_name}/' directory for pickle files.")

    except Exception as e:
        print(f"Error in Simulation.py __main__: {e}")
        import traceback
        traceback.print_exc()
