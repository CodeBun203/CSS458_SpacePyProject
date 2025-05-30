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
def get_gravitatonal_force(body1, body2, delta_time):
    """Get the gravitational force between 2 bodies based on the elasped 
    time.
    
    Method Arguments:
    * body1: The first body. Must be of the Planetary_Body class.
    * body2: The second body. Must be of the Planetary_Body class.
    * delta_time: The time since the previous call in months.

    Output:
    * None

    Uses the law of universal gravitation to determine the force applied to 
    both bodies.
    """
    if isinstance(Planetary_Body(), body1) \
    and isinstance(Planetary_Body(), body2):
        import scipy.constants as sp
        import numpy as np
        
        # Law of Universal Gravitaion Variables
        m1 = body1.mass
        m2 = body2.mass
        G = sp.gravitational_constant
        r = Planetary_Body.get_body_distance(body1, body2)
        
        # Handle case of 2 bodies at the same position
        if np.isclose(r, 0.0):
            F = 0.0
        # Law of Universal Gravitaion Equation
        else:
            F = ( ( G * m1 * m2 ) / np.pow( r, 2 ) )
        
        # Return the force
        return F  
    
    # One of the parametes was not a body
    else:
        if not isinstance(Planetary_Body(), body1):
            raise ValueError("get_attraction_force(body1, body2) " + \
                             "requires that the first parameter be of " + \
                                 "type Planetary_Body")
        else:
            raise ValueError("get_attraction_force(body1, body2) " + \
                             "requires that the second parameter be of" + \
                                 " type Planetary_Body")



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
    if isinstance(Planetary_Body(), body1) \
    and isinstance(Planetary_Body(), body2):
        import numpy as np
        componenets = body1 - body2
        distance = np.sqrt(np.pow(componenets.x, 2) + \
                           np.pow(componenets.y, 2) + \
                           np.pow(componenets.z, 2))
        return distance
    # One of the parametes was not a body
    else:
        if not isinstance(Planetary_Body(), body1):
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
        self.x = x_val
        self.y = y_val
        self.z = z_val
    
    
    
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
        if isinstance(Vector3(), scalar):
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
        if isinstance(Vector3(), scalar):
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
        if isinstance(Vector3(), scalar):
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
        if isinstance(Vector3(), scalar):
            return Vector3(self.x / scalar.x, self.y / scalar.y, self.z / \
                           scalar.z)
        else:
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
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def magnitude(self):
        """Return the magnitude of this vector
        
        Method Arguments:
        * None

        Output:
        * The magnitude of this Vector3.
        """
        import numpy as np
        return( np.sqrt( ( self.x ** 2 ) + ( self.y ** 2 ) + ( self.z ** 2) ) ) 





#==============================================================================
#                             Planetary_Body Class
#==============================================================================
class Planetary_Body:
    
    #---------------------------- Static Variables ----------------------------
    km_per_s_to_AU_per_month = 0.0175671
    
    
    
    #--------------------------- Constructor Method ---------------------------
    def __init__(self, mass_val = 0.0, pos_vector = Vector3(), \
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
        self.name = name_val
        self.mass = mass_val
        self.pos = pos_vector
        self.velocity = vel_vector
    
    
    
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
    
    
    
    #----------------------------- Setter Methods -----------------------------
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
        acceleration = force_vector / self.mass
        self.velocity = self.velocity + (acceleration * delta_time)





#==============================================================================
#                                  Test Code
#==============================================================================
if __name__ == "__main__":
    print("Tests still need to be designed.")
    print("Vector class:")
    print("1. Vector math functions")
    print("2. Vector magnitude")
    print("3. Vector normalization")
    print()
    print("Body Class:")
    print("1. Apply force")
    print("2. Update position")
    print("3. As type list")
    print()
    print("Package Functions:")
    print("1. Body distance")
    print("2. Gravitational Force")
    print("4. Write CSV")
    print("5. Read CSV")