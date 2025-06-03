
def dump_history(system_hist, sim_name, inital_time, final_time):
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
        os.mkdir("dumps")
        os.mkdir("dumps" + os.sep + sim_name)
    except:
        pass
    
    
    filepath = "dumps" + os.sep + sim_name + os.sep + str(inital_time) + "_" + \
    str(final_time)
    
    with open(filepath, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        
        # write the inital and final time:
        writer.writerow([inital_time, final_time])
        
        # write the simulation
        for timesteps in range(0, np.shape(system_hist)[0]):
            for planet in range(0, np.shape(system_hist)[1]):
                writer.writerow([str(system_hist[timesteps, planet])])
            writer.writerow([])



import numpy as np
temp = np.array([[2,3], [1,4], [9,6]])
dump_history(temp, "Hi", 0, 3)