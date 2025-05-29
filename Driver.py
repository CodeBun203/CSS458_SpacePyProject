'''
driver.py

    For this file, it will be the drive all the files within our model.
    The purpose is to handle validation while checking the model's behavior and
    physics during simulation and calculation. 

    Note:
        This file was written assuming all files are completed. 
        Everything that is commented out is there for when those files are
        ready to to imported into this file. 
'''

import numpy as np
from body import Planetary_Body, Vector3
#from simulation import simulation as sim
#from visualization import visualization as vsl

'''
    Initializing planet constants
'''
SUN_MASS = 1.0  # in MEarth units or normalized units
EARTH_MASS = 3.003e-6
EARTH_POS = Vector3(1.0, 0.0, 0.0)  # AU
EARTH_VEL = Vector3(0.0, 29.78, 0.0)  # km/s
SUN_POS = Vector3(0.0, 0.0, 0.0)
SUN_VEL = Vector3(0.0, 0.0, 0.0)

'''
    Creating planetary bodies
'''
sun = Planetary_Body(name = "Sun", mass = SUN_MASS, position = SUN_POS, velocity = SUN_VEL)
earth = Planetary_Body(name = "Earth", mass = EARTH_MASS, position = EARTH_POS, velocity = EARTH_VEL)
# Other planets will be added later for now, we will have these two

'''
    Initializing and running simulation
'''
#bodies = [sun, earth]
#sim = Simulator(bodies = bodies, timestep = 1.0, duration = 1200)
#sim.run()