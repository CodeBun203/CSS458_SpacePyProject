# CSS458_SpacePyProject
To ensure clear organization, file descriptions are listed here, either copy/paste here or fully written out.

## BaseDriver.py
Originally, we wanted this file to be the main driver of our entire model. After realization, our group went with turning this into a base driver, and using it to create all the simulations that we wanted to see within our model. The base duration of all is set to 100 years with a 0.1 (around 3 days) time steps. 

The format is as follows:

1) Initialize the duration and time step of simulation. 
2) Initialize all the bodies that will be present for that simulation.
3) For each body in the list of bodies, get the calculations for all the vectors that are needed.
4) Create all the bodies within the Planetary Bodies class.
5) Run the simulations.
6) Print out the final positions of the planets within that simulation. 
7) (If needed) Call visual all that simulation. 


### AvahDriver.py
In this file, there was a total of 10 different simulations. Seven out of ten tests were conducting  using the default duration and time step. The other three were conducted using a 10,000 year duration with the default time step. The 

The first three tests lists have the duration of 10,000 years, while everything below is have the duration set to 100 years. These tests were conducting:

**Removed One Body:** Jupiter was removed.

**Removed Two Bodies:** Jupiter and Venus were removed.

**Perpendicular Planes:** Sun stays in the same place. Mercury's orbit plane stays the same. Venus's orbit plane rotates on a 90 degree angle. So on and so forth. 

**Evenly Distribution of Sun's Mass:** The Sun's Mass is evenly shared to all of the other planets.

**Random Masses:** Using a random number with 4 number float point generator, all bodies have different masses. Note that the random is already set in when the planets are initialized. 

**Swapped Places:** All of the planets, expect the Sun, swap places. Each time you run this sim, the 'random' module is called so no two runs will be the same.

**Random Velocities:** Same principles as the 'Swapped Places' simulation, expect you're changing the velocity of all the planets expect the Sun. 

**Lagrange Stability:** We wanted to answer the question:"How does the distance from both bodies change over time?" For this simulation, there's only four bodies: Sun, Earth, Small Astroid, and Jupiter. 

**Lagrange Larger Mass Body:** Same principle "Lagrange Stability" but the Small Astroid's mass has been changed to Jupiter's Mass. 

**Two Suns:** Just like the name suggests, a second sun is labeled. All of the planets will stay the same. 

### ChloeDriver.py

### HaydenDriver.py

## Testing.py
We wanted this file to help us handle calculation verification within our model. It will ensure we designed all the behaviors and implementations correctly and catch any critical errors. 

    What this file is verifying:
    - Gravitational Physics
        * Force Symmetric
        * Zero Distance

    - Lagrange Points
        * L4 (weakest) Point Stability

    - Elliptical Orbit
        * Orbit Consistency
    
    - Simulation Integration
        * Can our simulation file run our model without any issues?

## Simulation.py

Implements class that manages the overall N-body system and its evolution over time. It initializes with a list of bodies objects (from Body.py) and a time step, then executes the main simulation loop. In each step, it orchestrates the calculation of net gravitational forces on every body by calling methods in Body.py, then uses these forces to update each body's velocity and its position, again by invoking methods from Body.py. It records the trajectory of each body, ultimately returning a complete position history suitable for analysis or visualization.

## Body.py

Body.py implements two classes, Vector3 and Planetary_Body. Vector3 holds 3 values that describe the x, y, and z components of a vector and is primarily used for position and velocity. It has methods implementing basic arithmetic operations as well as other helpful Vector operations such as Normalization. The Planetary_Body class has 4 attributes; name (string), position (Vector3), velocity (Vector3), and mass (float). This class also contains functions for applying forces on bodies, updating their position, and finding the distance between two bodies. Utilizes Gravity equation uses the universal law of gravitation. Body.py will be used by both Simulation.py and Driver.py.

## Visualization.py
File not created.

At this moment in time, we're focused on the calculations first before doing anything as far as displaying or visualizing. This will be the last file to be created. 
