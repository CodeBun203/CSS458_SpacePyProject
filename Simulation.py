# simulation.py
import numpy as np
from Body import Planetary_Body, Vector3, KM_PER_S_TO_AU_PER_MONTH, CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH

class Simulation:
    """
    Manages and runs an N-body gravitational simulation using RK4 integration.
    Time step is in months. Positions are AU, Velocities are km/s.
    """
    def __init__(self, list_of_planetary_bodies, time_step_months=0.1, name="Placeholder"): # Default to 0.1 months
        if not all(isinstance(pb, Planetary_Body) for pb in list_of_planetary_bodies):
            raise TypeError("All items must be Planetary_Body instances.")
            
        self.bodies = list_of_planetary_bodies
        self.dt_months = float(time_step_months) # Time step for RK4 in months
        self.body_names = [body.name for body in self.bodies]
        self.position_history = []
        self.sim_name = name

    def _get_system_state_derivatives(self, temp_system_state):
        """
        Calculates derivatives for the RK4 method.
        Args:
            temp_system_state (list[Planetary_Body]): List of bodies representing the current state
                                                     (pos in AU, vel in km/s).
        Returns:
            tuple(list[Vector3], list[Vector3]):
                - pos_derivatives (list of velocities in AU/month)
                - vel_derivatives (list of accelerations in km/(s*month))
        """
        num_bodies = len(temp_system_state)
        
        # 1. Calculate raw gravitational accelerations in AU/month^2
        raw_accels_AU_month_sq = [Vector3(0,0,0) for _ in range(num_bodies)]
        for i in range(num_bodies):
            target_body = temp_system_state[i]
            total_force_on_target_AU_MEarth_month_sq = Vector3(0,0,0)
            for j in range(num_bodies):
                if i == j:
                    continue
                acting_body = temp_system_state[j]
                # force is in MEarth * AU / month^2
                force_vector = Planetary_Body.calculate_gravitational_force_exerted_by_on(
                    acting_body=acting_body,
                    target_body=target_body
                )
                total_force_on_target_AU_MEarth_month_sq += force_vector
            
            if target_body.mass != 0:
                # accel_AU_month_sq = Force / mass
                raw_accels_AU_month_sq[i] = total_force_on_target_AU_MEarth_month_sq / target_body.mass
        
        # 2. Calculate position derivatives (dx/dt in AU/month)
        # vel_kms * (AU/month)/(km/s) = AU/month
        pos_derivatives_AU_month = [body.velocity * KM_PER_S_TO_AU_PER_MONTH for body in temp_system_state]

        # 3. Convert accelerations from AU/month^2 to km/(s*month) for velocity derivatives
        # accel_AU_month_sq * (km/(s*month))/(AU/month^2) = km/(s*month)
        vel_derivatives_kms_month = [acc * CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH for acc in raw_accels_AU_month_sq]
        
        return pos_derivatives_AU_month, vel_derivatives_kms_month


    def run_simulation(self, total_duration_years):
        # Data dump timer
        import time
        import SimIO
        import copy
        prev_time = time.time()
        prev_step = -1
        
        
        if not isinstance(total_duration_years, (int, float)) or total_duration_years <= 0:
            raise ValueError("total_duration_years must be a positive number.")

        total_duration_months = total_duration_years * 12.0
        num_simulation_steps = int(total_duration_months / self.dt_months)
        dt = self.dt_months # RK4 time step in months
        num_bodies = len(self.bodies)
        
        print(f"Running N-body simulation for {total_duration_years:.2f} years ({total_duration_months:.2f} months) "
              f"with a {self.dt_months:.3f}-month time step ({num_simulation_steps} steps) using RK4...")
        
        initial_positions_snapshot = [body.pos.to_list() for body in self.bodies]
        self.position_history.append(initial_positions_snapshot)
        sim_hist = [copy.deepcopy(self.bodies)]
        
        for step_num in range(num_simulation_steps):
            if num_simulation_steps > 100 and step_num > 0 and step_num % (num_simulation_steps // 20) == 0:
                 print(f"  Processed step {step_num}/{num_simulation_steps} ({(step_num/num_simulation_steps*100):.0f}%)")
            
            y0_pos_AU = [body.pos.copy() for body in self.bodies]       # AU
            y0_vel_kms = [body.velocity.copy() for body in self.bodies] # km/s

            # --- RK4 Stage k1 ---
            # Derivatives at current state (self.bodies)
            k1_pos_deriv_AU_month, k1_vel_deriv_kms_month = self._get_system_state_derivatives(self.bodies)

            # --- RK4 Stage k2 ---
            temp_bodies_k2 = []
            for i in range(num_bodies):
                pos_k2_intermediate_AU = y0_pos_AU[i] + (k1_pos_deriv_AU_month[i] * (dt / 2.0))
                vel_k2_intermediate_kms = y0_vel_kms[i] + (k1_vel_deriv_kms_month[i] * (dt / 2.0))
                temp_bodies_k2.append(Planetary_Body(name_val=self.bodies[i].name, 
                                                     mass_val=self.bodies[i].mass, 
                                                     pos_vector=pos_k2_intermediate_AU, 
                                                     vel_vector=vel_k2_intermediate_kms))
            k2_pos_deriv_AU_month, k2_vel_deriv_kms_month = self._get_system_state_derivatives(temp_bodies_k2)

            # --- RK4 Stage k3 ---
            temp_bodies_k3 = []
            for i in range(num_bodies):
                pos_k3_intermediate_AU = y0_pos_AU[i] + (k2_pos_deriv_AU_month[i] * (dt / 2.0))
                vel_k3_intermediate_kms = y0_vel_kms[i] + (k2_vel_deriv_kms_month[i] * (dt / 2.0))
                temp_bodies_k3.append(Planetary_Body(name_val=self.bodies[i].name,
                                                     mass_val=self.bodies[i].mass,
                                                     pos_vector=pos_k3_intermediate_AU,
                                                     vel_vector=vel_k3_intermediate_kms))
            k3_pos_deriv_AU_month, k3_vel_deriv_kms_month = self._get_system_state_derivatives(temp_bodies_k3)

            # --- RK4 Stage k4 ---
            temp_bodies_k4 = []
            for i in range(num_bodies):
                pos_k4_intermediate_AU = y0_pos_AU[i] + (k3_pos_deriv_AU_month[i] * dt)
                vel_k4_intermediate_kms = y0_vel_kms[i] + (k3_vel_deriv_kms_month[i] * dt)
                temp_bodies_k4.append(Planetary_Body(name_val=self.bodies[i].name,
                                                     mass_val=self.bodies[i].mass,
                                                     pos_vector=pos_k4_intermediate_AU,
                                                     vel_vector=vel_k4_intermediate_kms))
            k4_pos_deriv_AU_month, k4_vel_deriv_kms_month = self._get_system_state_derivatives(temp_bodies_k4)

            # --- Update final positions (AU) and velocities (km/s) ---
            for i in range(num_bodies):
                # Weighted average of position derivatives (AU/month)
                avg_pos_deriv_AU_month = (k1_pos_deriv_AU_month[i] + 
                                         (k2_pos_deriv_AU_month[i] * 2.0) + 
                                         (k3_pos_deriv_AU_month[i] * 2.0) + 
                                         k4_pos_deriv_AU_month[i]) / 6.0
                self.bodies[i].pos = y0_pos_AU[i] + (avg_pos_deriv_AU_month * dt)

                # Weighted average of velocity derivatives (km/(s*month))
                avg_vel_deriv_kms_month = (k1_vel_deriv_kms_month[i] + 
                                          (k2_vel_deriv_kms_month[i] * 2.0) + 
                                          (k3_vel_deriv_kms_month[i] * 2.0) + 
                                          k4_vel_deriv_kms_month[i]) / 6.0
                self.bodies[i].velocity = y0_vel_kms[i] + (avg_vel_deriv_kms_month * dt)
            
            current_positions_snapshot = [body.pos.to_list() for body in self.bodies]
            self.position_history.append(current_positions_snapshot)
            sim_hist.append(copy.deepcopy(self.bodies))
            
            # Check if dump timer has been met
            if (time.time() - prev_time >= SimIO.MIN_DUMP_TIME):
                print("Dumping Data")
                SimIO.dump_history_pickle(sim_hist, self.sim_name, prev_step +1, step_num)
                prev_step = step_num
                prev_time = time.time()
                sim_hist = []
        
        print("Dumping Data")
        print("Simulation complete.")
        SimIO.dump_history_pickle(sim_hist, self.sim_name, prev_step +1, num_simulation_steps-1)
        return np.array(self.position_history)

if __name__ == "__main__":
    print("Simulation.py example using months and km/s:")
    try:
        sun = Planetary_Body(333000.0, Vector3(0,0,0), Vector3(0,0,0), "Sun")
        # Earth's average orbital speed is ~29.78 km/s
        earth = Planetary_Body("Earth", 1.0, Vector3(1.0,0,0), Vector3(0,29.78,0))

        # Time step: e.g., 0.1 months (approx 3 days)
        # For a stable Earth orbit, smaller time steps are better.
        # 1 day = 1 / (365.25/12) months approx 1/30.4375 months
        one_day_in_months = 1.0 / (365.25 / 12.0)
        sim = Simulation([sun, earth], time_step_months=one_day_in_months * 3) # Simulating with ~3 day steps

        # Simulate for a short period, e.g., 2 months (approx 1/6th of an orbit)
        duration_years = 2.0 / 12.0 
        
        print(f"\nInitial Earth: {earth}")
        history = sim.run_simulation(duration_years)
        print(f"Simulation finished. {len(history)} steps recorded.")
        print(f"Final Earth: {earth}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
