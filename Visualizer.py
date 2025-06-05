# visualizer.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import random

def run_anim(sim_name):
    """takes a folder name containg a set of pickled data representing a system
    over time and turns it into an animation
    
    Method Arguments:
    * sim_name: The name of a simulation to load data from
        
    Output:
    * None
    """
    data = anim_data(sim_name)
    animate_simulation(data[0], data[1], data[2])


def anim_data(sim_name):
    """takes a folder name containg a set of pickled data representing a system
    over time and turns it into the data for an anuimation
    
    Method Arguments:
    * sim_name: The name of a simulation to load data from
        
    Output:
    * A 2D array of planets formated for the animate_simulation method
    """
    import SimIO

    sim_hist = SimIO.reconstruct_history_pickle(sim_name)
    
    # Get position data
    temp = np.shape(sim_hist)
    if len(temp) < 2: # Basic check for sim_hist structure
        print("Error: sim_hist does not have the expected dimensions.")
        return (np.array([]), [], []) 
        
    num_steps = temp[0]
    num_planets = temp[1]
    pos_data = np.zeros((num_steps, num_planets, 3))
    
    for step in range(0, num_steps):
        for planet in range(0, num_planets):
            pos_data[step, planet, 0] = sim_hist[step, planet].pos.x
            pos_data[step, planet, 1] = sim_hist[step, planet].pos.y
            pos_data[step, planet, 2] = sim_hist[step, planet].pos.z
            
    # Get name data
    name_data = []
    for planet in range(0, num_planets):
        name_data.append(sim_hist[0, planet].name)

    # Get mass data
    mass_data = []
    for planet in range(0, num_planets):
        mass_data.append(sim_hist[0, planet].mass)
    
    print(pos_data)
    return (pos_data, name_data, mass_data)

def animate_simulation(position_history, names, masses):
    """
    Creates and displays a 3D animation of the simulation.

    Args:
        position_history (np.ndarray): A NumPy array of shape (num_steps, num_bodies, 3)
                                     containing the position of each body at each step.
        names (list[str]): A list of names for each body for labeling.
        masses (list[float]): A list of masses for each body. (Currently used for size validation, not color)
    """
    if not position_history.size: # Check if position_history is empty
        print("No position data to animate.")
        return

    num_steps, num_bodies, _ = position_history.shape

    if len(masses) != num_bodies:
        raise ValueError("The length of 'masses' list must match the number of bodies.")
    if len(names) != num_bodies:
        raise ValueError("The length of 'names' list must match the number of bodies.")

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    # --- Define colors ---
    plot_colors = []
    for name in names:
        if 'sun' in name.lower(): # Case-insensitive check for "sun"
            plot_colors.append('yellow')
        else:
            # Generate a random RGB color tuple (values between 0 and 1)
            plot_colors.append(np.random.rand(3,)) 


    # Create scatter plot objects for each body
    sizes = [100 if 'sun' in name.lower() else 20 for name in names] 
    
    scatter_plots = [ax.scatter([], [], [], s=size, color=plot_colors[i], label=name) 
                     for i, (name, size) in enumerate(zip(names, sizes))]
    
    # Create line plot objects for the orbital trails, using the same assigned colors
    trails = [ax.plot([], [], [], '-', color=plot_colors[i], linewidth=0.5)[0] 
              for i in range(num_bodies)]

    def init():
        """Initializes the plot elements."""
        ax.set_title('Pylanetary Simulator')
        ax.set_xlabel('X (AU)')
        ax.set_ylabel('Y (AU)')
        ax.set_zlabel('Z (AU)')
        ax.legend(loc='upper right')
        
        # Determine plot limits based on the maximum extent of positions
        if position_history.size > 0:
            max_range = np.max(np.abs(position_history)) * 1.2 # Increased padding slightly
            if max_range == 0: # Handle case where all positions are zero
                max_range = 1 
        else:
            max_range = 10 # Default range if no data

        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])


            
        return scatter_plots + trails

    def update(frame):
        """Updates the plot for each animation frame."""
        for i in range(num_bodies):
            pos = position_history[frame, i]
            scatter_plots[i]._offsets3d = ([pos[0]], [pos[1]], [pos[2]])

            # Update trail data up to the current frame
            trail_data = position_history[:frame+1, i]
            trails[i].set_data(trail_data[:, 0], trail_data[:, 1]) # X, Y data
            trails[i].set_3d_properties(trail_data[:, 2]) # Z data

        return scatter_plots + trails

    frame_skip = max(1, num_steps // 1000 if num_steps > 1000 else 1) 

    # Create the animation
    # interval: Delay between frames in milliseconds. 
    # blit=True can improve performance but can be tricky with 3D plots and legends.
    # Setting blit=False is often more robust for 3D.
    anim = FuncAnimation(fig, update, frames=range(0, num_steps, frame_skip), 
                         init_func=init, blit=False, interval=30) # interval can be adjusted
    
    #plt.tight_layout() # Adjust layout to prevent labels from overlapping
    plt.show()


if __name__ == '__main__':
    run_anim("Moons")