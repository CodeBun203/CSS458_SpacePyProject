# Driver.py
import os
import sys 
from Body import Planetary_Body, Vector3, read_system 
from Simulation import Simulation
from Visualizer import animate_simulation, anim_data 
import SimIO

def main():
    try:
        project_root_dir = os.path.dirname(os.path.abspath(__file__))
    except NameError: 
        project_root_dir = os.getcwd()
        print(f"Warning: __file__ not defined, using CWD as project root: {project_root_dir}")

    initial_systems_dir = os.path.join(project_root_dir, "Initial_Systems")
    dumps_base_dir = os.path.join(project_root_dir, getattr(SimIO, 'DEFAULT_DUMP_PATH', getattr(SimIO, 'DEFAULT_DUMPS_DIR', "Dumps")))

    if not os.path.isdir(initial_systems_dir):
        print(f"Error: 'Initial_Systems' directory not found at {initial_systems_dir}")
        print("Please create it and populate it with _Initial.csv files.")
        return
    os.makedirs(dumps_base_dir, exist_ok=True) 

    print(f"Looking for initial system CSVs in: {initial_systems_dir}")
    print(f"Simulation history (pickle) dumps will be saved in subdirectories of: {dumps_base_dir}")
    print("-" * 40)

    DEFAULT_SIMULATION_DURATION_YEARS = 10000 # Shorter for quick testing
    DEFAULT_TIME_STEP_MONTHS = 0.0075
    DEFAULT_DUMP_INTERVAL_SECONDS = getattr(SimIO, 'MIN_DUMP_TIME', 600.0) 

    try:
        initial_csv_files = [f for f in os.listdir(initial_systems_dir) if f.endswith("Moons_Initial.csv")]
    except FileNotFoundError:
        print(f"Error: 'Initial_Systems' directory not found at {initial_systems_dir}.")
        initial_csv_files = []

    if not initial_csv_files:
        print(f"No '*_Initial.csv' files found in '{initial_systems_dir}'.")
        return

    sim_names_completed_for_final_viz = []
    #initial_csv_files = ["Binary_Suns_Close_Initial.csv"] # Override to test a single system

    for csv_filename in initial_csv_files:
        initial_csv_path = os.path.join(initial_systems_dir, csv_filename)
        system_name_from_file = csv_filename.replace("_Initial.csv", "")
        # SimIO.py will create a subdirectory named system_name_from_file inside dumps_base_dir

        print(f"\n>>> Processing System: {system_name_from_file} <<<")
        print(f"  Loading initial state from: {initial_csv_path}")

        list_of_bodies = read_system(initial_csv_path) 

        if not list_of_bodies:
            print(f"  Warning: No bodies loaded from {initial_csv_path}. Skipping.")
            continue
        
        print(f"  Successfully loaded {len(list_of_bodies)} bodies for {system_name_from_file}.")

        current_sim_duration_years = DEFAULT_SIMULATION_DURATION_YEARS
        current_time_step_months = DEFAULT_TIME_STEP_MONTHS
        current_dump_interval_seconds = DEFAULT_DUMP_INTERVAL_SECONDS

        total_steps_for_this_run = 0
        if current_time_step_months > 0:
             total_steps_for_this_run = int((current_sim_duration_years * 12.0) / current_time_step_months)
        
        if total_steps_for_this_run <= 0:
            print(f"  Warning: Calculated total steps for {system_name_from_file} is {total_steps_for_this_run}. Skipping.")
            continue
            
        print(f"  Simulation Parameters for {system_name_from_file}:")
        print(f"    Duration: {current_sim_duration_years:.3f} years")
        print(f"    Time Step: {current_time_step_months:.4f} months")
        print(f"    Total Steps: {total_steps_for_this_run}")
        print(f"    SimIO Dump Interval: ~{current_dump_interval_seconds} seconds (wall clock)")
        print(f"    SimIO Dump Subdirectory: {os.path.join(dumps_base_dir, system_name_from_file)}")


        simulation_instance = Simulation(
            list_of_planetary_bodies=list_of_bodies,
            time_step_months=current_time_step_months,
            simulation_name=system_name_from_file, # For SimIO subdirectory and file naming
            dump_interval_seconds=current_dump_interval_seconds
        )

        print(f"  Starting simulation for: {system_name_from_file}...")
        try:
            position_history_array_in_memory = simulation_instance.run_simulation(
                total_duration_years=current_sim_duration_years
            )
            print(f"  Simulation for {system_name_from_file} complete.")
            sim_names_completed_for_final_viz.append(system_name_from_file) 
            print(f"  Pickle history chunks saved in Dumps/{system_name_from_file}/")

        except Exception as e:
            print(f"  ERROR during simulation for {system_name_from_file}: {e}")
            import traceback; traceback.print_exc()
        print("-" * 30) 

    print("\nAll initial systems processed.")

    # Visualization from Pickle Dumps
    if sim_names_completed_for_final_viz: 
        print("\n--- Visualizing from Pickle Dump Example (First Completed Sim) ---")
        sim_to_visualize_from_dump = sim_names_completed_for_final_viz[0] 
        print(f"Attempting to load and animate: '{sim_to_visualize_from_dump}' from its pickle dump files...")
        
        # Visualizer.anim_data is already set up to use SimIO.reconstruct_history_pickle
        pos_hist_d, names_d, masses_d = anim_data(sim_to_visualize_from_dump) # Pass only sim_name
        
        if pos_hist_d is not None:
            print(f"Data loaded from pickle dump for {sim_to_visualize_from_dump}. Launching animation...")
            animate_simulation(pos_hist_d, names_d, masses_d, trail_length_percent=0.5)
        else:
            print(f"Could not load data from pickle dump for {sim_to_visualize_from_dump}.")
    else:
        print("\nNo simulations were completed, skipping visualization from dump file example.")

if __name__ == '__main__':
    main()
