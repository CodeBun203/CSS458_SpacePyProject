# visualizer.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
# Removed Normalize as it was for the colorbar
import random # Added for random color selection
import SimIO

def anim_data(sim_name):
    """takes a folder name containg a set of pickled data representing a system
    over time and turns it into the data for an anuimation
    

    Method Arguments:
    * sim_name: The name of a simulation to load data from
        
    Output:
    * A 2D array of planets formated for the animate_simulation method
    """
    # import SimIO # Moved to top-level imports
    
    sim_hist = SimIO.reconstruct_history_pickle(sim_name)
    
    # Get position data
    temp = np.shape(sim_hist)
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
    
    print(pos_data) # This print statement is kept as it was in the original
    return (pos_data, name_data, mass_data)

def animate_simulation(position_history, names, masses):
    """
    Creates and displays a 3D animation of the simulation.

    Args:
        position_history (np.ndarray): A NumPy array of shape (num_steps, num_bodies, 3)
                                       containing the position of each body at each step.
        names (list[str]): A list of names for each body for labeling.
        masses (list[float]): A list of masses for each body (currently used for size check).
    """
    num_steps, num_bodies, _ = position_history.shape

    if len(masses) != num_bodies:
        raise ValueError("The length of 'masses' list must match the number of bodies.")
    if len(names) != num_bodies:
        raise ValueError("The length of 'names' list must match the number of bodies.")

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    # --- Define Colors and Sizes ---
    # Sizes: Sun is larger, other bodies have a default smaller size.
    sizes = [200 if name == 'Sun' else 50 for name in names] 
    
    # Colors: Sun is yellow, others are randomly selected from a predefined list.
    plot_colors = []
    # Predefined list of visually distinct colors (excluding yellow)
    distinct_colors = [
        'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'cyan',
        'magenta', 'lime', 'teal', 'lavender', 'turquoise', 'darkgreen',
        'navy', 'maroon', 'gray', 'darkgray', 'lightgray', 'olive', 'sienna',
        'gold', 'indigo', 'violet', 'coral', 'crimson', 'dodgerblue'
    ]
    random.shuffle(distinct_colors) # Shuffle to make assignments appear random

    color_assignment_index = 0
    for name in names:
        if 'sun' in name.lower(): # Case-insensitive check for "Sun"
            plot_colors.append('yellow')
        else:
            if distinct_colors: # Check if the list is not empty
                plot_colors.append(distinct_colors[color_assignment_index % len(distinct_colors)])
                color_assignment_index += 1
            else: # Fallback if distinct_colors is somehow empty (should not happen with the list above)
                plot_colors.append(f"#{random.randint(0, 0xFFFFFF):06x}")


    # Create scatter plot objects for each body
    scatter_plots = [ax.scatter([], [], [], s=size, color=plot_colors[i], label=name) 
                     for i, (name, size) in enumerate(zip(names, sizes))]
    
    # Create line plot objects for the orbital trails, using the same body-specific colors
    trails = [ax.plot([], [], [], '-', color=plot_colors[i], linewidth=0.5)[0] 
              for i in range(num_bodies)]
                     
    def init():
        """Initializes the plot elements."""
        ax.set_title('Pylanetary Simulator')
        ax.set_xlabel('X (AU)')
        ax.set_ylabel('Y (AU)')
        ax.set_zlabel('Z (AU)')
        ax.legend(loc='upper right') # Display legend
        
        max_range = np.max(np.abs(position_history)) * 1.1
        if max_range == 0: # Handle case with no movement or single point
            max_range = 1.0
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
            trails[i].set_data(trail_data[:, 0], trail_data[:, 1])
            trails[i].set_3d_properties(trail_data[:, 2])
        return scatter_plots + trails

    # Adjust frame_skip to ensure a reasonable number of frames for animation
    # Aim for around 1000 frames for a smooth animation, but not less than 1
    frame_skip = max(1, num_steps // 1000 if num_steps > 1000 else 1) 
    
    anim = FuncAnimation(fig, update, frames=range(0, num_steps, frame_skip), \
                         init_func=init, blit=False, interval=20) # interval is ms between frames
    
   # anim.save("C:\Users\Avafs\Desktop\School\Spring 25\CSS 458\CSS458_SpacePyProject\AvahVisualizations") # Kept as original
    plt.show()
