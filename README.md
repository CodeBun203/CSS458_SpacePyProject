# CSS458_SpacePyProject
To ensure clear organization, file descriptions are listed here, either copy/paste here or fully written out.

## Driver.py
For this file, it will be the drive all the files within our model. The purpose is to handle validation while checking the model's behavior and physics during simulation and calculation. There are some aspect that can change, but towards polishing this model, those will be noted for users. 

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

Body.py implements two classes, Vector3 and Planetary_Body. VEctor3 has methods implementing basic arithmentic operations as well as other helpful Vector operations such as Normalization. The Planetary_Body class has 4 attributes; name (string), position (Vector3), velocity (Vector3), and mass (float). This class also contains functions for applying forces on bodies, updating their position, and finding the distance between two bodies. Utilizes Gravity equation uses the universal law of gravitation. Body.py will be used by both Simulation.py and Driver.py.

## Visualization.py
File not created.

At this moment in time, we're focused on the calculations first before doing anything as far as displaying or visualizing. This will be the last file to be created. 
