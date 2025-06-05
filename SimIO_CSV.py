# SimIO.py
# Phase 3: Module for saving simulation progress to a single CSV per run.

import csv
import os
# Body.py is needed if we reconstruct Planetary_Body objects for any reason here,
# or if type hinting is used. For writing, we primarily need body.as_type_list()
# and body.name, body.mass.
from Body import Planetary_Body 

# Define the header for the dump CSV file.
# This format includes time information in each row for clarity.
DUMP_FILE_HEADER = [
    "TimeStep_Index", "Time_Months", 
    "BodyName", "Mass_MEarth", 
    "PosX_AU", "PosY_AU", "PosZ_AU", 
    "VelX_kms", "VelY_kms", "VelZ_kms"
]

def initialize_dump_file(dump_filepath, system_bodies_initial_state):
    """
    Creates and initializes a new dump CSV file for a simulation run.
    Writes the header and the initial state (time step 0) of the system.

    Args:
        dump_filepath (str): The full path to the CSV file to be created.
        system_bodies_initial_state (list[Planetary_Body]): A list of Planetary_Body objects
                                                             representing the initial state of the system.
    """
    # Ensure the directory for the dump file exists
    dump_dir = os.path.dirname(dump_filepath)
    if dump_dir: # Check if dump_dir is not an empty string (e.g. if filename is in current dir)
        os.makedirs(dump_dir, exist_ok=True)

    try:
        with open(dump_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(DUMP_FILE_HEADER)
            
            # Write the initial state (time step 0, time 0.0 months)
            time_step_index = 0
            time_months = 0.0
            for body in system_bodies_initial_state:
                # body.as_type_list() returns:
                # [Name, Mass_MEarth, PosX_AU, PosY_AU, PosZ_AU, VelX_kms, VelY_kms, VelZ_kms]
                # We need to prepend time_step_index and time_months.
                # Note: body.name and body.mass are already part of as_type_list() if it's structured correctly.
                # Let's assume as_type_list() gives: [Name, Mass, Px, Py, Pz, Vx, Vy, Vz]
                # The header expects: TimeStep, Time, Name, Mass, Px, Py, Pz, Vx, Vy, Vz
                
                # Robustly get data from body attributes to match DUMP_FILE_HEADER
                row_data = [
                    time_step_index, time_months,
                    body.name, float(body.mass), # Ensure mass is float
                    float(body.pos.x), float(body.pos.y), float(body.pos.z), # Ensure pos components are float
                    float(body.velocity.x), float(body.velocity.y), float(body.velocity.z) # Ensure vel components are float
                ]
                writer.writerow(row_data)
        print(f"SimIO: Initialized dump file: {dump_filepath}")
    except IOError as e:
        print(f"SimIO Error: Could not initialize dump file {dump_filepath}. Error: {e}")
    except Exception as e:
        print(f"SimIO Error: An unexpected error occurred during dump file initialization. Error: {e}")


def append_to_dump_file(dump_filepath, current_time_step_index, current_time_months, current_system_bodies_state):
    """
    Appends the current state of all bodies in the system to the dump CSV file.

    Args:
        dump_filepath (str): The full path to the CSV file.
        current_time_step_index (int): The current simulation time step index.
        current_time_months (float): The current simulation time in months.
        current_system_bodies_state (list[Planetary_Body]): A list of Planetary_Body objects
                                                             representing the current state.
    """
    try:
        with open(dump_filepath, 'a', newline='') as csvfile: # Open in append mode
            writer = csv.writer(csvfile)
            for body in current_system_bodies_state:
                # Prepare row data matching DUMP_FILE_HEADER
                row_data = [
                    current_time_step_index, current_time_months,
                    body.name, float(body.mass),
                    float(body.pos.x), float(body.pos.y), float(body.pos.z),
                    float(body.velocity.x), float(body.velocity.y), float(body.velocity.z)
                ]
                writer.writerow(row_data)
        # print(f"SimIO: Appended state for time step {current_time_step_index} to {dump_filepath}") # Optional: for verbose logging
    except IOError as e:
        print(f"SimIO Error: Could not append to dump file {dump_filepath}. Error: {e}")
    except Exception as e:
        print(f"SimIO Error: An unexpected error occurred while appending to dump file. Error: {e}")


# --- Optional: Functions for loading/reconstructing (can be developed further in Phase 6/7) ---
def load_history_from_dump_csv(dump_filepath):
    """
    (Optional - for later development or for Visualizer.py)
    Loads and reconstructs simulation history from a SimIO dump CSV file.
    This can be complex to parse into the (num_steps, num_bodies, 3) position array
    and separate name/mass lists needed by the current visualizer.
    Using pandas would simplify this significantly.

    Returns:
        A structured representation of the history (e.g., a list of dictionaries,
        or a pandas DataFrame).
    """
    history_data = []
    if not os.path.exists(dump_filepath):
        print(f"SimIO Error: Dump file not found: {dump_filepath}")
        return history_data # Or None, or raise error

    try:
        with open(dump_filepath, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile) # Use DictReader for easier access by column name
            for row in reader:
                # Convert numeric fields from string to float/int
                try:
                    processed_row = {
                        "TimeStep_Index": int(row["TimeStep_Index"]),
                        "Time_Months": float(row["Time_Months"]),
                        "BodyName": row["BodyName"],
                        "Mass_MEarth": float(row["Mass_MEarth"]),
                        "PosX_AU": float(row["PosX_AU"]),
                        "PosY_AU": float(row["PosY_AU"]),
                        "PosZ_AU": float(row["PosZ_AU"]),
                        "VelX_kms": float(row["VelX_kms"]),
                        "VelY_kms": float(row["VelY_kms"]),
                        "VelZ_kms": float(row["VelZ_kms"]),
                    }
                    history_data.append(processed_row)
                except ValueError as ve:
                    print(f"SimIO Warning: Skipping row due to data conversion error in {dump_filepath}: {row}. Error: {ve}")
                except KeyError as ke:
                    print(f"SimIO Warning: Skipping row due to missing key in {dump_filepath}: {row}. Missing key: {ke}")

        print(f"SimIO: Successfully loaded {len(history_data)} records from {dump_filepath}")
    except IOError as e:
        print(f"SimIO Error: Could not read dump file {dump_filepath}. Error: {e}")
    except Exception as e:
        print(f"SimIO Error: An unexpected error occurred while reading dump file. Error: {e}")
    return history_data


if __name__ == "__main__":
    print("SimIO.py testing ground...")
    # Example Usage:
    # Create some dummy body data (normally from Body.py instances)
    # Note: For this test to run standalone, you'd need a minimal Planetary_Body and Vector3
    # or mock them. Assuming Body.py is accessible for a proper test.
    try:
        # Create a dummy Vector3 and Planetary_Body for testing if Body.py is not fully set up
        # This is just for allowing SimIO.py to be tested in isolation.
        # In the actual project, these come from the real Body.py.
        if 'Vector3' not in globals():
            class Vector3:
                def __init__(self, x, y, z): self.x=x; self.y=y; self.z=z
        if 'Planetary_Body' not in globals():
            class Planetary_Body:
                def __init__(self, name, mass, pos, vel):
                    self.name=name; self.mass=mass; self.pos=pos; self.velocity=vel

        body1_initial = Planetary_Body("Earth", 1.0, Vector3(1,0,0), Vector3(0,29.78,0))
        body2_initial = Planetary_Body("Mars", 0.1, Vector3(1.5,0,0), Vector3(0,24.0,0))
        initial_system = [body1_initial, body2_initial]

        test_dump_dir = "Test_Dumps"
        test_sim_name = "MyTestSim"
        test_dump_filename = os.path.join(test_dump_dir, f"{test_sim_name}_History.csv")

        # Test initialization
        initialize_dump_file(test_dump_filename, initial_system)

        # Test appending
        body1_step1 = Planetary_Body("Earth", 1.0, Vector3(0.9,0.1,0), Vector3(-2.0,28.0,0))
        body2_step1 = Planetary_Body("Mars", 0.1, Vector3(1.4,0.05,0), Vector3(-1.0,23.5,0))
        system_step1 = [body1_step1, body2_step1]
        append_to_dump_file(test_dump_filename, 1, 0.1, system_step1)

        body1_step2 = Planetary_Body("Earth", 1.0, Vector3(0.8,0.2,0), Vector3(-4.0,26.0,0))
        body2_step2 = Planetary_Body("Mars", 0.1, Vector3(1.3,0.09,0), Vector3(-2.0,23.0,0))
        system_step2 = [body1_step2, body2_step2]
        append_to_dump_file(test_dump_filename, 2, 0.2, system_step2)

        print(f"\nTest dump file created at: {os.path.abspath(test_dump_filename)}")

        # Test loading
        print("\nLoading history from dump file...")
        loaded_history = load_history_from_dump_csv(test_dump_filename)
        if loaded_history:
            print(f"Loaded {len(loaded_history)} records.")
            # Print first few records for verification
            for i in range(min(5, len(loaded_history))):
                print(loaded_history[i])
        
        # Clean up test file and directory if empty
        # if os.path.exists(test_dump_filename):
        #     os.remove(test_dump_filename)
        # if os.path.exists(test_dump_dir) and not os.listdir(test_dump_dir):
        #     os.rmdir(test_dump_dir)

    except NameError as ne:
        print(f"SimIO Test Error: A class is not defined (likely Vector3 or Planetary_Body from Body.py). {ne}")
        print("Please ensure Body.py is in the same directory or accessible in PYTHONPATH for full testing.")
    except Exception as e:
        print(f"SimIO Test Error: {e}")
        import traceback
        traceback.print_exc()