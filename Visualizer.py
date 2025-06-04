# visualizer.py

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize

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
        masses (list[float]): A list of masses for each body, used for color-coding.
    """
    num_steps, num_bodies, _ = position_history.shape

    if len(masses) != num_bodies:
        raise ValueError("The length of 'masses' list must match the number of bodies.")
    if len(names) != num_bodies:
        raise ValueError("The length of 'names' list must match the number of bodies.")

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    # --- Color mapping based on mass ---
    np_masses = np.array(masses)

    # Handle cases where all masses are the same
    if np.ptp(np_masses) == 0:
        # For simplicity, if all masses are equal, they'll all get the middle color.
        normalized_masses = np.full(num_bodies, 0.5)
    else:
        # Normalize masses to the range [0, 1] for the colormap
        # Bigger objects (like the Sun) will have higher mass and thus a different color.
        min_mass = np.min(np_masses)
        max_mass = np.max(np_masses)
        normalized_masses = (np_masses - min_mass) / (max_mass - min_mass)

    # `viridis` goes from yellow (high) to blue/purple (low).
    colormap = plt.cm.viridis

    # Create scatter plot objects for each body
    sizes = [100 if name == 'Sun' else 20 for name in names]
    # colors = plt.cm.get_cmap('tab10', num_bodies) # OLD color logic
    
    # Get colors from the colormap based on normalized mass
    plot_colors = [colormap(norm_mass) for norm_mass in normalized_masses]

    scatter_plots = [ax.scatter([], [], [], s=size, color=plot_colors[i], label=name) 
                     for i, (name, size) in enumerate(zip(names, sizes))]
    
    # Create line plot objects for the orbital trails, using the same mass-based colors
    trails = [ax.plot([], [], [], '-', color=plot_colors[i], linewidth=0.5)[0] 
              for i in range(num_bodies)]

    # --- Add a colorbar ---
    # Create a ScalarMappable for the colorbar
    if np.ptp(np_masses) == 0:
        # If all masses are the same, set a fixed range for the colorbar
        norm = Normalize(vmin=np_masses[0] - 0.5 if num_bodies > 0 else 0, vmax=np_masses[0] + 0.5 if num_bodies > 0 else 1)
    else:
        norm = Normalize(vmin=np.min(np_masses), vmax=np.max(np_masses))
    
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
    sm.set_array([]) # You can set an array of values that your colormap is based on.
                     # For just showing the range, an empty array is fine if norm is set.

    def init():
        """Initializes the plot elements."""
        ax.set_title('Pylanetary Simulator')
        ax.set_xlabel('X (AU)')
        ax.set_ylabel('Y (AU)')
        ax.set_zlabel('Z (AU)')
        ax.legend()
        
        max_range = np.max(np.abs(position_history)) * 1.1
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])

        # Add the colorbar to the figure
        # Doing it in init or just once after figure creation is fine.
        # To prevent adding it multiple times if init is called more than once
        if not hasattr(init, 'colorbar_added'):
            cbar = fig.colorbar(sm, ax=ax, pad=0.1, shrink=0.6, aspect=15)
            cbar.set_label('Mass (Earth Masses)')
            init.colorbar_added = True
            
        return scatter_plots + trails

    def update(frame):
        """Updates the plot for each animation frame."""
        for i in range(num_bodies):
            pos = position_history[frame, i]
            scatter_plots[i]._offsets3d = ([pos[0]], [pos[1]], [pos[2]])

            trail_data = position_history[:frame+1, i]
            trails[i].set_data(trail_data[:, 0], trail_data[:, 1])
            trails[i].set_3d_properties(trail_data[:, 2])
        return scatter_plots + trails

    frame_skip = max(1, num_steps // 1000)
    anim = FuncAnimation(fig, update, frames=range(0, num_steps, frame_skip),
                         init_func=init, blit=False, interval=20)

    plt.show()