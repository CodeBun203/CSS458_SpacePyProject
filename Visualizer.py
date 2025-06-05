# Visualizer.py
# This version is already compatible with SimIO.reconstruct_history_pickle

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
import os # For path joining if needed

# Try to import SimIO to get DEFAULT_DUMPS_DIR, otherwise use a fallback
try:
    import SimIO
    # Your SimIO.py uses DEFAULT_DUMP_PATH, let's adapt or assume it's available
    DEFAULT_DUMPS_DIR_FROM_SIMIO = getattr(SimIO, 'DEFAULT_DUMPS_DIR', getattr(SimIO, 'DEFAULT_DUMP_PATH', "Dumps"))
except (ImportError, AttributeError):
    DEFAULT_DUMPS_DIR_FROM_SIMIO = "Dumps"
    print(f"Visualizer Warning: Could not get DEFAULT_DUMPS_DIR from SimIO. Using fallback: '{DEFAULT_DUMPS_DIR_FROM_SIMIO}'")


def anim_data(sim_name, dumps_dir=DEFAULT_DUMPS_DIR_FROM_SIMIO):
    """
    Takes a simulation name, loads its history using SimIO.reconstruct_history_pickle,
    and formats the data for the animate_simulation method.
    """
    # Ensure SimIO is available
    if 'SimIO' not in globals() or not hasattr(SimIO, 'reconstruct_history_pickle'):
        print("Visualizer Error: SimIO module or reconstruct_history_pickle function not available.")
        return None, None, None

    print(f"Visualizer: Loading pickled data for simulation '{sim_name}' from dumps in '{dumps_dir}'...")
    # SimIO.reconstruct_history_pickle takes sim_name (for subdirectory) and assumes DEFAULT_DUMPS_DIR
    # If your SimIO needs dumps_dir passed, you'd adjust its call.
    # Your uploaded SimIO.reconstruct_history_pickle uses os.path.join(DEFAULT_DUMP_PATH, sim_name)
    # So, we just need to ensure DEFAULT_DUMP_PATH (or DEFAULT_DUMPS_DIR) in SimIO points correctly.
    
    sim_hist = SimIO.reconstruct_history_pickle(sim_name) # This should use SimIO's DEFAULT_DUMPS_DIR
    
    if sim_hist is None or sim_hist.size == 0:
        print(f"Visualizer Error: No history data reconstructed for '{sim_name}'.")
        return None, None, None

    try:
        # sim_hist is expected to be a NumPy array of shape (num_steps, num_bodies)
        # where each element is a Planetary_Body object.
        num_steps, num_bodies = sim_hist.shape
        
        if num_steps == 0 or num_bodies == 0:
            print("Visualizer Error: Reconstructed history has no steps or no bodies.")
            return None, None, None

        pos_data = np.zeros((num_steps, num_bodies, 3))
        name_data = []
        mass_data = []

        # Extract names and masses from the first time step
        # (assuming names and masses are constant for each body throughout the simulation)
        for body_idx in range(num_bodies):
            first_step_body = sim_hist[0, body_idx]
            if not hasattr(first_step_body, 'name') or \
               not hasattr(first_step_body, 'mass') or \
               not hasattr(first_step_body, 'pos') or \
               not hasattr(first_step_body.pos, 'x'):
                print(f"Visualizer Error: Reconstructed body object at [0,{body_idx}] is missing attributes.")
                return None, None, None
            name_data.append(first_step_body.name)
            mass_data.append(first_step_body.mass)
        
        # Extract position data for all steps
        for step_idx in range(num_steps):
            for body_idx in range(num_bodies):
                body_object = sim_hist[step_idx, body_idx]
                pos_data[step_idx, body_idx, 0] = body_object.pos.x
                pos_data[step_idx, body_idx, 1] = body_object.pos.y
                pos_data[step_idx, body_idx, 2] = body_object.pos.z
                
        print(f"Visualizer: Successfully processed pickled data. Position history shape: {pos_data.shape}")
        return pos_data, name_data, mass_data

    except AttributeError as ae:
        print(f"Visualizer Error: Attribute error while processing reconstructed history. "
              f"Ensure Planetary_Body objects in pickle files are complete. Error: {ae}")
        import traceback
        traceback.print_exc()
    except IndexError as ie:
        print(f"Visualizer Error: Index error, likely issue with sim_hist shape. "
              f"Expected (num_steps, num_bodies). Got shape: {getattr(sim_hist, 'shape', 'N/A')}. Error: {ie}")
    except Exception as e:
        print(f"Visualizer Error: Failed to process reconstructed history for '{sim_name}'. Error: {e}")
        import traceback
        traceback.print_exc()
    return None, None, None


def animate_simulation(position_history, names, masses, trail_length_percent=.1):
    # This function remains largely the same as in 
    # It's already designed to take the processed numpy array for positions.
    if position_history is None or not isinstance(position_history, np.ndarray) or position_history.ndim != 3 or position_history.shape[0] == 0:
        print("Visualizer Error: Invalid or empty position_history for animation."); return
    num_steps, num_bodies, _ = position_history.shape
    if num_bodies == 0: print("Visualizer Error: No bodies to animate."); return
    if len(masses) != num_bodies: masses = [1.0] * num_bodies 
    if len(names) != num_bodies: names = [f"Body{i+1}" for i in range(num_bodies)]

    fig = plt.figure(figsize=(12,12)); ax = fig.add_subplot(111,projection='3d')
    np_masses = np.array(masses)
    norm_masses = (np_masses - np.min(np_masses))/(np.max(np_masses)-np.min(np_masses)) if np.ptp(np_masses)>0 else np.full(num_bodies,0.5)
    cmap = plt.cm.viridis; sizes = [100 if n.lower()=='sun' else 30 for n in names]
    plot_colors = [cmap(nm) for nm in norm_masses]
    sc_plots = [ax.scatter([],[],[],s=s,color=pc,label=n,depthshade=True) for i,(s,pc,n) in enumerate(zip(sizes,plot_colors,names))]
    trails = [ax.plot([],[],[],'-',color=pc,linewidth=0.7)[0] for pc in plot_colors]
    
    norm_val = Normalize(vmin=np.min(np_masses),vmax=np.max(np_masses)) if np.ptp(np_masses)>0 else Normalize(vmin=(np_masses[0]-0.5 if len(np_masses)>0 and np_masses[0]!=0 else -0.5), vmax=(np_masses[0]+0.5 if len(np_masses)>0 and np_masses[0]!=0 else 0.5) )
    if norm_val.vmin == norm_val.vmax : norm_val.vmax +=1.0 
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_val); sm.set_array([])

    def init_anim():
        ax.set_title('Pylanetary Simulator'); ax.set_xlabel('X (AU)'); ax.set_ylabel('Y (AU)'); ax.set_zlabel('Z (AU)')
        ax.legend(loc='upper left',bbox_to_anchor=(1.05,1))
        max_r = np.max(np.abs(position_history))*1.1 if num_steps>0 and np.any(position_history) else 10.0 
        if max_r == 0 : max_r = 10.0 
        ax.set_xlim([-max_r,max_r]); ax.set_ylim([-max_r,max_r]); ax.set_zlim([-max_r,max_r])
        fig.tight_layout(rect=[0,0,0.85,1])
        if not hasattr(init_anim,'cb_added'): fig.colorbar(sm,ax=ax,pad=0.15,shrink=0.6,aspect=15).set_label('Mass (MEarth)'); init_anim.cb_added=True
        return sc_plots + trails
    
    TRAIL_PTS = max(1, int(num_steps * trail_length_percent))
    def update_anim(frame):
        for i in range(num_bodies):
            sc_plots[i]._offsets3d = ([position_history[frame,i,0]],[position_history[frame,i,1]],[position_history[frame,i,2]])
            start = max(0, frame + 1 - TRAIL_PTS)
            trail_d = position_history[start:frame+1, i]
            trails[i].set_data(trail_d[:,0],trail_d[:,1]); trails[i].set_3d_properties(trail_d[:,2])
        return sc_plots + trails
    
    fr_skip = max(1, num_steps//500 if num_steps>500 else 1); anim_int = 30
    global anim_object 
    anim_object = FuncAnimation(fig,update_anim,frames=range(0,num_steps,fr_skip),init_func=init_anim,blit=False,interval=anim_int)
    plt.show()

if __name__ == '__main__':
    print("Visualizer.py testing ground (for Pickle SimIO)...")
    # test_sim_name = "Solar_System_Full"
    # test_sim_name = "Binary_Suns_Close"
    # test_sim_name = "Solar_System_No_Jupiter"
    # test_sim_name = "Sun_Earth_Moon"
    # test_sim_name = "Three_Body_Equal_Mass_Figure8"
    test_sim_name = "Binary_Star_System"
    # test_sim_name = "Lagrange_Point_Test"
    # test_sim_name = "Moons"
    # test_sim_name = "Sensitivity_Test_System1"
    # test_sim_name = "Sensitivity_Test_System2"
    # test_sim_name = "Slingshot_Ejection_Test"
    
    print(f"Attempting to load and animate pickled data for: {test_sim_name}")
    
    # Use the dumps_dir defined at the module level
    pos_h, names_h, masses_h = anim_data(test_sim_name, dumps_dir=DEFAULT_DUMPS_DIR_FROM_SIMIO)
    if pos_h is not None:
        print(f"Data loaded for {test_sim_name}. Launching animation...")
        animate_simulation(pos_h, names_h, masses_h, trail_length_percent=0.5)
    else:
        print(f"Could not load data for {test_sim_name}. "
              "Ensure SimIO.py is accessible and dump files exist in the correct 'Dumps' subdirectory.")