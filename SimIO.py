DEFAULT_DUMP_PATH = "dumps"
MIN_DUMP_TIME = 600.0 # in seconds

#==============================================================================
#                                 Package Methods
#==============================================================================

#------------------------------ CSV Write Method ------------------------------
def dump_history_csv(system_hist, sim_name, inital_time, final_time):
    """Create a backup of all the data about the simulation's positions, 
    masses, and name 
    
    Method Arguments:
    * system_hist: A 2D numpy array of all the planets at each timestep being 
      dumped.
    * sim_name: The name of the simulation.
    * inital_time: The time "index" of the simulation for the first time step 
      from system_hist. Used for reconstruction of data.
    * final_time: The time "index" of the simulation for the last time step 
      from system_hist. Used for reconstruction of data.
        
    Output:
    * None 
    """
    import csv
    import os
    import numpy as np
    
    try:
        os.mkdir(DEFAULT_DUMP_PATH)
    except:
        pass
    
    try:
        os.mkdir(DEFAULT_DUMP_PATH + os.sep + sim_name)
    except:
        pass
    
    
    file_path = DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep + \
    str(inital_time)
    
    with open(file_path + ".csv", 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        
        # write the inital and final time:
        writer.writerow([inital_time, final_time])
        
        # write the simulation
        #each time step
        for timesteps in range(0, np.shape(system_hist)[0]):
            #each planet
            for planet in range(0, np.shape(system_hist)[1]):
                writer.writerow(system_hist[timesteps][planet].as_type_list())
            #empty line after each time step
            writer.writerow([])

def dump_history_pickle(system_hist, sim_name, inital_time, final_time):
    """Create a backup of all the data about the simulation's positions, 
    masses, and name 
    
    Method Arguments:
    * system_hist: A 2D numpy array of all the planets at each timestep being 
      dumped.
    * sim_name: The name of the simulation.
    * inital_time: The time "index" of the simulation for the first time step 
      from system_hist. Used for reconstruction of data.
    * final_time: The time "index" of the simulation for the last time step 
      from system_hist. Used for reconstruction of data.
        
    Output:
    * None 
    """
    import os
    import pickle
    
    try:
        os.mkdir(DEFAULT_DUMP_PATH)
    except:
        pass
    
    try:
        os.mkdir(DEFAULT_DUMP_PATH + os.sep + sim_name)
    except:
        pass
    
    
    file_path = DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep + \
    str(inital_time)
    
    with open(file_path + ".pkl", 'wb') as file:
        pickle.dump(system_hist, file)



#------------------------------ CSV Read Method -------------------------------
def reconstruct_history_csv(sim_name):
    """Create an array of all data over time dumped by the simulation
    
    Method Arguments:
    * sim_name: The name of the simulation.
        
    Output:
    * A 2D numpy array of all the planets at each timestep that were dumped.
    """
    import csv
    import os
    import numpy as np
    from Body import Vector3, Planetary_Body
    import copy

    # File management vars
    file_path = DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep
    last_file = False
    
    # System Management vars
    system_hist = []
    cur_time_index = 0
    
    while(not last_file):
        try:
            with open(file_path + str(cur_time_index) + ".csv", newline='') \
            as csvfile:
                reader = csv.reader(csvfile)
                
                # Read the timestep indexes of the file
                next(reader)
                
                # Read the simulation
                temp_system = []
                for row in reader:
                    if(len(row) >= 8):
                        new_name = row[0]
                        new_mass = row[1]
                        new_pos = Vector3(row[2], row[3], row[4])
                        new_vel = Vector3(row[5], row[6], row[7])
                        new_body = Planetary_Body(new_mass, new_pos, new_vel, new_name)
                        temp_system.append(copy.deepcopy(new_body))
                    else:
                        system_hist.append(copy.deepcopy(temp_system))
                        temp_system = []
                        cur_time_index += 1
        # Could not find simulation file
        except:
            print("'" + DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep + \
                  str(cur_time_index) + "' does not exist, end of history.")
            last_file = True

    return np.array(system_hist)

def reconstruct_history_pickle(sim_name):
    """Create an array of all data over time dumped by the simulation
    
    Method Arguments:
    * sim_name: The name of the simulation.
        
    Output:
    * A 2D numpy array of all the planets at each timestep that were dumped.
    """
    import os
    import pickle
    import numpy as np

    # File management vars
    file_path = DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep
    last_file = False
     
    # System Management vars
    system_hist = []
    cur_time_index = 0

    while(not last_file):
        try:
            with open(file_path + str(cur_time_index) + ".pkl", 'rb') as file:
                temp = pickle.load(file)
                system_hist += temp
                cur_time_index = len(system_hist)
                
        # Could not find simulation file
        except:
            print("'" + DEFAULT_DUMP_PATH + os.sep + sim_name + os.sep + \
                  str(cur_time_index) + "'.pkl does not exist, end of history.")
            last_file = True

    return np.array(system_hist)

#==============================================================================
#                                  Test Code
#==============================================================================

def test_dump_and_recon_csv():
    print("Testing CSV dumping")
    import time
    from Body import Vector3, Planetary_Body
    import numpy as np
    import copy
    
    # create a system of bodies
    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, \
         'pos_AU_components': [0.0, 0.0, 0.0], \
         'vel_km_s_components': [0.0, 0.0, 0.0]}, \
        {'name': 'Earth',   'mass_MEarth': 1.0, \
         'pos_AU_components': [0.182, 0.967, 0.0], \
         'vel_km_s_components': [-29.9, 5.6, 0.0]}, \
        {'name': 'Mars',    'mass_MEarth': 0.107, \
         'pos_AU_components': [-1.08, -1.04, 0.038], \
         'vel_km_s_components': [16.4, -18.6, -0.7]}, \
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
    
    # create 1st set of mock data
    system = np.array(list_of_bodies)
    history1 = []
    for i in range(0,10):
        history1.append(copy.deepcopy(system))
        for i in range(0, np.shape(system)[0]):
            system[i].update_pos(100)
    
    # create 2nd set of mock data
    history2 = []
    for i in range(0,10000):
        history2.append(copy.deepcopy(system))
        for i in range(0, np.shape(system)[0]):
            system[i].update_pos(100)
    
    dump_history_csv(history1, "Test_Sim", 0, 9)
    cur_time = time.time()
    dump_history_csv(history2, "Test_Sim", 10, 10009)
    elapesed_time = time.time() - cur_time
    
    # reconstruct data
    full_hist = history1 + history2
    dumped_hist = reconstruct_history_csv("Test_Sim")
    
    # print results
    # Check data shape 
    if (np.shape(full_hist) != np.shape(dumped_hist)):
        print("Data shapes do not match!")
        return
    #Check data contents
    for time_step in range(0, np.shape(full_hist)[0]):
        for planet in range(0, np.shape(full_hist)[1]):
            if not (full_hist[time_step][planet] == \
                    dumped_hist[time_step][planet]):
                print("Data does not match!")
                print(full_hist[i].as_type_list())
                print(dumped_hist[i].as_type_list())
                return
    
    print("Data reconstructed succesfully!")
    print(f"Time to dump 1000 states of 2 objects {elapesed_time}")

def test_dump_and_recon_pkl():
    print("Testing Pickle dumping")
    import time
    from Body import Vector3, Planetary_Body
    import numpy as np
    import copy
    
    # create a system of bodies
    solar_system_initial_data = [
        {'name': 'Sun',     'mass_MEarth': 333000.0, \
         'pos_AU_components': [0.0, 0.0, 0.0], \
         'vel_km_s_components': [0.0, 0.0, 0.0]}, \
        {'name': 'Earth',   'mass_MEarth': 1.0, \
         'pos_AU_components': [0.182, 0.967, 0.0], \
         'vel_km_s_components': [-29.9, 5.6, 0.0]}, \
        {'name': 'Mars',    'mass_MEarth': 0.107, \
         'pos_AU_components': [-1.08, -1.04, 0.038], \
         'vel_km_s_components': [16.4, -18.6, -0.7]}, \
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
    
    # create 1st set of mock data
    system = np.array(list_of_bodies)
    history1 = []
    for i in range(0,10):
        history1.append(copy.deepcopy(system))
        for i in range(0, np.shape(system)[0]):
            system[i].update_pos(100)
    
    # create 2nd set of mock data
    history2 = []
    for i in range(0,10000):
        history2.append(copy.deepcopy(system))
        for i in range(0, np.shape(system)[0]):
            system[i].update_pos(100)
    dump_history_pickle(history1, "Test_Sim", 0, 9)
    cur_time = time.time()
    dump_history_pickle(history2, "Test_Sim", 10, 10009)
    elapesed_time = time.time() - cur_time
    
    # reconstruct data
    full_hist = history1 + history2
    dumped_hist = reconstruct_history_pickle("Test_Sim")
    
    # print results
    # Check data shape 
    if (np.shape(full_hist) != np.shape(dumped_hist)):
        print("Data shapes do not match!")
        return
    #Check data contents
    for time_step in range(0, np.shape(full_hist)[0]):
        for planet in range(0, np.shape(full_hist)[1]):
            if not (full_hist[time_step][planet] == \
                    dumped_hist[time_step][planet]):
                print("Data does not match!")
                print(full_hist[i].as_type_list())
                print(dumped_hist[i].as_type_list())
                return
    
    print("Data reconstructed succesfully!")
    print(f"Time to dump 1000 states of 2 objects {elapesed_time}")


if __name__ == "__main__": 
    test_dump_and_recon_csv()
    print()
    test_dump_and_recon_pkl()
    