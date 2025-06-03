KM_PER_S_TO_AU_PER_MONTH = 0.0175671
DAYS_PER_MONTH = 365.25 / 12.0

# Gravitational constant in AU^3/(MEarth * day^2)
_G_ASTRO_DAYS_REF = (0.017202098950233253**2) / 333000.0 # Approx 8.886e-10

# Gravitational constant in AU^3/(MEarth * month^2)
# Scipy constants gives G in m^3/(kg * s^2),:
G_ASTRO_MONTHS = _G_ASTRO_DAYS_REF * (DAYS_PER_MONTH**2) # Approx 8.231e-7
CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH = 1.0 / KM_PER_S_TO_AU_PER_MONTH


#==============================================================================
#                                 Package Methods
#==============================================================================

#------------------------------ CSV Write Method ------------------------------
def write_system(system, file_name):
    """Write a system of bodies to a CSV file.
    
    Method Arguments:
    * system: A list of bodies
    * file_name: A path and file name to save thae data into. (Example: 
      Data/System.csv).

    Output:
    * None
    """
    import csv
    
    with open(file_name, 'w', newline=',') as csvfile:
        writer = csv.writer(csvfile)
        # Write a header
        writer.writerow(['Name', 'Mass', 'Pos.x', 'Pos.y', 'Pos.z', 'Vel.x', \
                         'Vel.y', 'Vel.z'])
        # Write the system
        for i in range(0, len(system)):
            writer.writerow(system[i].as_type_list())



#------------------------------ CSV Read Method -------------------------------
def read_system(file_name):
    """Write a system of bodies to a CSV file.
    
    Method Arguments:
    * file_name: A path and file name to read thae data from. (Example: 
      Data/System.csv).

    Output:
    * A list of bodies that were stored in the file
    """
    import csv
    
    with open(file_name, newline=',') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header
        next(reader) 
        # Read the system
        system = []
        for row in reader:
            if(len(row) >= 8):
                new_name = row[0]
                new_mass = row[1]
                new_pos = Vector3(row[2], row[3], row[4])
                new_vel = Vector3(row[5], row[6], row[7])
                new_body = Planetary_Body(new_mass, new_pos, new_vel, new_name)
                system.append(new_body)
            else:
                print("Encountered a row with too little data to make a body")
                print(row)
        return system



#-------------------------- Body Gravitational Force --------------------------
def get_gravitatonal_force_euler(body1, body2, delta_time):
    """Get the gravitational force between 2 bodies based on the elasped 
    time using eulers method
    
    Method Arguments:
    * body1: The first body. Must be of the Planetary_Body class.
    * body2: The second body. Must be of the Planetary_Body class.
    * delta_time: The time since the previous call in months.

    Output:
    * None

    Uses the law of universal gravitation to determine the force applied to 
    both bodies from their current positions.
    """
    if isinstance(body1, Planetary_Body) and isinstance(body2, Planetary_Body): # Corrected basic check
        import scipy.constants as sp
        import numpy as np
        
        # Law of Universal Gravitaion Variables
        m1 = float(body1.mass) # Ensure float for calculation
        m2 = float(body2.mass) # Ensure float for calculation
        G = sp.gravitational_constant 
        r_val = Planetary_Body.get_body_distance(body1, body2)

        # Check if r_val is a number
        if not isinstance(r_val, (int, float)):
            # return a default if get_body_distance fails
            print(f"Warning: Could not calculate distance for {body1.name} and {body2.name}, get_body_distance returned: {r_val}")
            return 0.0

        # Handle case of 2 bodies at the same position
        if np.isclose(r_val, 0.0):
            F = 0.0
        # Law of Universal Gravitaion Equation
        else:
            F = ( ( G * m1 * m2 ) / np.pow( r_val, 2 ) )
        
        # Return the force
        return F  
    
    # One of the parametes was not a body
    else:
        if not isinstance(body1, Planetary_Body):
            raise ValueError("get_attraction_force(body1, body2) " + \
                             "requires that the first parameter be of " + \
                                 "type Planetary_Body")
        else: # Implies body2 is not a Planetary_Body
            raise ValueError("get_attraction_force(body1, body2) " + \
                             "requires that the second parameter be of" + \
                                 " type Planetary_Body")

def partial_step(vec1, vec2, time_step):
    return (vec1 + vec2) * time_step



#------------------------------- Body Distance --------------------------------
def get_body_distance(body1, body2):
    """Find the distance between 2 bodies
        
    Method Arguments:
    * body1: The first body. Must be of the Planetary_Body class.
    * body2: The second body. Must be of the Planetary_Body class.

    Output:
    * The distance between the 2 bodies in AUs.
    
    Will raise an error if either of the arguments are not of the 
    Planetary_Body class.
    """
    if isinstance(body1, Planetary_Body) \
    and isinstance(body2, Planetary_Body): 
        import numpy as np 
        componenets = body1.pos - body2.pos # There is no subtraction operator for Planetary_Body
        distance = np.sqrt((componenets.x ** 2) + \
                           (componenets.y ** 2) + \
                           (componenets.z ** 2))
        return distance
    # One of the parametes was not a body
    else:
        if not isinstance(body1, Planetary_Body): 
            raise ValueError("get_body_distance(body1, body2) requires" + \
                             " that the first parameter be of type " + \
                             "Planetary_Body")
        else:
            raise ValueError("get_body_distance(body1, body2) requires" + \
                             " that the second parameter be of type " + \
                             "Planetary_Body")


#==============================================================================
#                                  Vector3 Class
#==============================================================================
class Vector3:
    
    #--------------------------- Constructor Method ---------------------------
    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0):
        """Initailize the viector 3 with 3 values.
        
        Method Arguments:
        * x: The x component (defaults to 0.0).
        * y: The y component (defaults to 0.0).
        * z: The z component (defaults to 0.0).

        Output:
        * None
        """
        self.x = float(x_val) 
        self.y = float(y_val)
        self.z = float(z_val)
    
    #--------------------------- Arithmetic Methods ---------------------------    
    def __add__(self, scalar):
        """The sum of a scalar or Vector3 and this Vector3.
        
        Method Arguments:
        * scalar: A numeric value or Vector3.

        Output:
        * A Vector3 sum of the input and this Vector3.
        
        If the input was a numeric value: Each component of this Vector3 + 
        the scalar value. (x + s), (y + s), (z + s).
        
        If the input was a Vector3: Each component this Vector3 are added to
        to the same component of the input Vector3. (x + x), (y + y), (z + z).
        """
        if isinstance(scalar, Vector3): 
            return Vector3(self.x + scalar.x, self.y + scalar.y, self.z + \
                           scalar.z)
        else:
            return Vector3(self.x + scalar, self.y + scalar, self.z + scalar)
    
    def __sub__(self, scalar):
        """The difference of a scalar or Vector3 and this Vector3.
        
        Method Arguments:
        * scalar: A numeric value or Vector3.

        Output:
        * A Vector3 difference of the input and this Vector3.
        
        If the input was a numeric value: Each component of this Vector3 - 
        the scalar value. (x - s), (y - s), (z - s).
        
        If the input was a Vector3: Each component this Vector3 are subtracted 
        from to the same component of the input Vector3. (x - x), (y - y), 
        (z - z).
        """
        if isinstance(scalar, Vector3): 
            return Vector3(self.x - scalar.x, self.y - scalar.y, self.z - \
                           scalar.z)
        else:
            return Vector3(self.x - scalar, self.y - scalar, self.z - scalar)
    
    def __mul__(self, scalar):
        """The product of a scalar or Vector3 and this Vector3.
        
        Method Arguments:
        * scalar: A numeric value or Vector3.

        Output:
        * A Vector3 product of the input and this Vector3.
        
        If the input was a numeric value: Each component of this Vector3 * 
        the scalar value. (x * s), (y * s), (z * s).
        
        If the input was a Vector3: Each component this Vector3 are multiplied 
        with the same component of the input Vector3. (x * x), (y * y), (z * z)
        """
        if isinstance(scalar, Vector3):
            return Vector3(self.x * scalar.x, self.y * scalar.y, self.z * \
                           scalar.z)
        else:
            return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        """The quotient of a scalar or Vector3 and this Vector3.
        
        Method Arguments:
        * scalar: A numeric value or Vector3.

        Output:
        * A Vector3 quotient of the input and this Vector3.
        
        If the input was a numeric value: Each component of this Vector3 / 
        the scalar value. (x / s), (y / s), (z / s).
        
        If the input was a Vector3: Each component this Vector3 are divided 
        from the same component of the input Vector3. (x / x), (y / y), (z / z)
        """
        if isinstance(scalar, Vector3): # Avoid division by zero
            if scalar.x == 0 or scalar.y == 0 or scalar.z == 0:
                raise ValueError("Component-wise division by Vector3 containing zero.")
            return Vector3(self.x / scalar.x, self.y / scalar.y, self.z / \
                           scalar.z)
        else:
             if scalar == 0:
                raise ValueError("Division by zero scalar.")
             return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    #----------------------------- Getter Methods -----------------------------
    def normalize(self):
        """Return a normalied version of this Vector3.
        
        Method Arguments:
        * None

        Output:
        * A normalized version of this Vector3.
        
        Returns a new Vector3 with the same direction as this vector, but with 
        a magnitude of 1.
        """
        mag = self.magnitude()
        if mag == 0: 
            return Vector3(0.0, 0.0, 0.0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def magnitude(self):
        """Return the magnitude of this vector
        
        Method Arguments:
        * None

        Output:
        * The magnitude of this Vector3.
        """
        import numpy as np
        return np.sqrt( ( self.x ** 2 ) + ( self.y ** 2 ) + ( self.z ** 2) ) 

    # Added to_list method for Simulation.py position history
    def to_list(self):
        return [self.x, self.y, self.z]

    # Added copy method for Simulation.py to avoid modifying original vectors during RK steps
    def copy(self):
        return Vector3(self.x, self.y, self.z)

    # Added __str__ for easier debugging
    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

#==============================================================================
#                             Planetary_Body Class
#==============================================================================
class Planetary_Body: 

    #---------------------------- Static Variables ----------------------------
    km_per_s_to_AU_per_month = KM_PER_S_TO_AU_PER_MONTH
    
    #--------------------------- Constructor Method ---------------------------
    def __init__(self, mass_val = 0.0, pos_vector = Vector3(), 
                 vel_vector = Vector3(), name_val = ""):
        """Inialize a gravitational body.
        
        Method Arguments:
        * mass_val: The mass of the body in Earth masses.
        * pos_vector: The position of the body.
        * vel_vector: The velovity vector of the body.
        * name_val: the name of the body.

        Output:
        * None
        """
        self.name = str(name_val)
        self.mass = float(mass_val) 
        self.pos = pos_vector
        self.velocity = vel_vector
    
    @staticmethod
    def calculate_gravitational_force_exerted_by_on(acting_body, target_body):
        import numpy as np 
        r_vector = acting_body.pos - target_body.pos 
        dist_sq = r_vector.x**2 + r_vector.y**2 + r_vector.z**2 
        if dist_sq == 0:
            return Vector3(0, 0, 0) 
        dist = np.sqrt(dist_sq)
        if dist == 0: 
            return Vector3(0,0,0)
        force_scalar_part = G_ASTRO_MONTHS * acting_body.mass * target_body.mass / (dist * dist_sq)
        force_vector = r_vector * force_scalar_part
        return force_vector

#----------------------------- Getter Methods -----------------------------    
    def as_type_list(self): 
        """Get the body data as a list.
        
        Method Arguments:
        * None

        Output:
        * The body class as a list.
        
        Values are in the order of Name, Mass, Pos.x, Pos.y, Pos.z, Vel.x, 
        Vel.y, Vel.z.
        """
        return [self.name, self.mass, self.pos.x, self.pos.y, self.pos.z, \
                self.velocity.x, self.velocity.y, self.velocity.z]
    
    def get_gravitatonal_acceleration_rk4(self, body_index, system, \
                                          delta_time):
        """
        
        """
        import scipy.constants as sp
        
        G = sp.gravitational_constant
        accel = Vector3(0.0, 0.0, 0.0)
        
        for index, external_body in enumerate(system):
            if index != body_index:
                r = get_body_distance(self, external_body)
                # Not sure if it should be r**2 or r**3
                temp = G * external_body.mass / r**3 
                
                #k1 - Euler's method
                k1 = (external_body.pos - self.pos) * temp
                
                #k2 - accelration 0.5 timesteps in the future based on k1
                #acceleration
                temp_vel = partial_step(self.velocity, k1, 0.5)
                temp_loc= partial_step(self.pos, temp_vel, 0.5 * delta_time)
                k2 = (external_body.pos - temp_loc) * temp
                
                #k3 - acceleration 0.5 timestemps in the future using k2 
                #acceleration
                temp_vel = partial_step(self.velocity, k2, 0.5)
                temp_loc= partial_step(self.pos, temp_vel, 0.5 * delta_time)
                k3 = (external_body.pos - temp_loc) * temp
                
                #k4 - location 1 timestep in the future using k3 acceleration
                temp_vel = partial_step(self.velocity, k3, 1)
                temp_loc= partial_step(self.pos, temp_vel, delta_time)
                k4 = (external_body.pos - temp_loc) * temp
                
                #calculate the acceleration
                accel = accel + ((k1 + (k2 * 2) + (k3 * 2) + k4) / 6)
        
        return accel
    
    def update_pos(self, delta_time): 
        """Update the body's position based on it's velocity.
        
        Method Arguments:
        * delta_time: the time since the previous call in months.

        Output:
        * None
        """
        self.pos = self.pos + (self.velocity * delta_time * \
        Planetary_Body.km_per_s_to_AU_per_month)
        
    def apply_force(self, force_vector, delta_time):
        """Apply a force on the body.
        
        Method Arguments:
        * force_vector: the force direction and magnitude.
        * delta_time: the time since the previous call in months.

        Output:
        * None
        
        Uses Newton's second law of motion, calculates the accelration vector 
        applied to the body.
        
            Force = Mass * Acceleration -> Acceleration = Force / Mass
            
        Acceleration is then used in the following kinematic equation to get 
        the change in the body's velocity.
        
            Velocity = Initial velocity + Acceleration * Duration of Force

        """
        if self.mass == 0:
            acceleration = Vector3(0,0,0)
        else:
            acceleration = force_vector / self.mass 
        self.velocity = self.velocity + (acceleration * delta_time) 
        
    def apply_acceleration(self, accel, delta_time): 
        """Accelrate a body
        
        Method Arguments:
        * accel: the acceleration direction and magnitude.
        * delta_time: the time since the previous call in months.

        Output:
        * None
            
        Acceleration is  used in the following kinematic equation to get 
        the change in the body's velocity.
        
            Velocity = Initial velocity + Acceleration * Duration of Force
            
        """
        self.velocity = self.velocity + (accel * delta_time) 

    # Added __str__ for debugging and readability
    def __str__(self):
        return (f"PlanetaryBody(Name: {self.name}, Mass: {self.mass}, "
                f"Pos: {self.pos}, Vel: {self.velocity})")


#==============================================================================
#                                  Test Code
#==============================================================================
if __name__ == "__main__": 
    print("Package Functions:")
    print("1. Body distance")
    print("2. Gravitational Force Euler")
    print("4. Write CSV") 
    print("5. Read CSV")

    print("\nNEW: Testing calculate_gravitational_force_exerted_by_on")
    try:
        sun_test = Planetary_Body(mass_val=333000.0, 
                                  pos_vector=Vector3(0.0,0.0,0.0), 
                                  vel_vector=Vector3(0.0,0.0,0.0), 
                                  name_val="TestSun")
        earth_test = Planetary_Body(mass_val=1.0, 
                                    pos_vector=Vector3(1.0,0.0,0.0), 
                                    vel_vector=Vector3(0.0,29.78,0.0), 
                                    name_val="TestEarth")
        force_on_earth = Planetary_Body.calculate_gravitational_force_exerted_by_on(sun_test, earth_test)
        print(f"Force by Sun on Earth (MEarth*AU/month^2): {force_on_earth.x:.3e}, {force_on_earth.y:.3e}, {force_on_earth.z:.3e}")
        print(f"Expected force magnitude on Earth: ~-0.274 MEarth*AU/month^2 (along x-axis)")
    except Exception as e:
        print(f"Error during new method test: {e}")
        import traceback 
        traceback.print_exc()