# Body.py
import numpy as np
import csv

AU_TO_KM = 149597870.691
MONTH_TO_SECONDS = 2629800
AU_PER_MONTH_TO_KM_PER_SECOND = AU_TO_KM / MONTH_TO_SECONDS
KM_PER_S_TO_AU_PER_MONTH = 1 / AU_PER_MONTH_TO_KM_PER_SECOND
DAYS_PER_MONTH = 365.25 / 12.0

# Gravitational constant in AU^3/(MEarth * day^2)
_G_ASTRO_DAYS_REF = (0.017202098950233253**2) / 333000.0 # Approx 8.886e-10

# Gravitational constant in AU^3/(MEarth * month^2)
G_ASTRO_MONTHS = _G_ASTRO_DAYS_REF * (DAYS_PER_MONTH**2) # Approx 8.231e-7

# Converts acceleration from AU/month^2 to km/(s*month)
CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH = AU_PER_MONTH_TO_KM_PER_SECOND


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
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Mass', 'Pos.x', 'Pos.y', 'Pos.z', 'Vel.x',
                         'Vel.y', 'Vel.z']) # Assuming Mass is MEarth, Pos is AU, Vel is km/s
        for body_item in system: # Changed from indexed loop for clarity
            writer.writerow(body_item.as_type_list())

#------------------------------ CSV Read Method -------------------------------
def read_system(file_name):
    """Write a system of bodies to a CSV file.
    
    Method Arguments:
    * file_name: A path and file name to read thae data from. (Example: 
      Data/System.csv).

    Output:
    * A list of bodies that were stored in the file
    """
    system = []
    try:
        with open(file_name, 'r', newline='') as csvfile: # Added 'r' mode
            reader = csv.reader(csvfile)
            try:
                header = next(reader) # Skip header
            except StopIteration:
                print(f"Warning: CSV file '{file_name}' is empty or has no header.")
                return system 
            
            for row in reader:
                if len(row) >= 8:
                    # Assuming Planetary_Body and Vector3 constructors handle float conversion
                    new_name = row[0]
                    new_mass = row[1] # MEarth
                    new_pos = Vector3(row[2], row[3], row[4]) # AU
                    new_vel = Vector3(row[5], row[6], row[7]) # km/s
                    # Ensure constructor keywords match your Planetary_Body.__init__
                    new_body = Planetary_Body(mass_val=new_mass,
                                              pos_vector=new_pos,
                                              vel_vector=new_vel,
                                              name_val=new_name)
                    system.append(new_body)
                elif any(field.strip() for field in row): # Check if row is not just empty
                    print(f"Warning: Encountered a row in '{file_name}' with too few data fields: {row}")
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    return system

#-------------------------- Body Gravitational Force --------------------------
def get_gravitatonal_force_euler(body1, body2): # Removed delta_time as it wasn't used
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
    if isinstance(body1, Planetary_Body) and isinstance(body2, Planetary_Body):
        import scipy.constants as sp # Local import as per original style
        
        m1 = float(body1.mass) 
        m2 = float(body2.mass) 
        G_si = sp.gravitational_constant 
        r_val = get_body_distance(body1, body2) # Returns AU

        if not isinstance(r_val, (int, float)):
            print(f"Warning: Could not calculate distance for {body1.name} and {body2.name}, get_body_distance returned: {r_val}")
            return 0.0
        
        # Handle case of 2 bodies at the same position
        if np.isclose(r_val, 0.0):
            F = 0.0
        else:
            # Law of Universal Gravitaion Equation
            F = ( ( G_si * m1 * m2 ) / ( r_val ** 2 ) ) 

        return F 
    
    # One of the parametes was not a body
    else:
        if not isinstance(body1, Planetary_Body):
            raise TypeError("get_gravitatonal_force_euler requires body1 to be Planetary_Body")
        else: 
            raise TypeError("get_gravitatonal_force_euler requires body2 to be Planetary_Body")

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
    if isinstance(body1, Planetary_Body) and isinstance(body2, Planetary_Body):
        components_vector = body1.pos - body2.pos 
        try:
            # Magnitude of the difference vector
            distance = np.sqrt(
                float(components_vector.x)**2 + 
                float(components_vector.y)**2 + 
                float(components_vector.z)**2
            )
            return distance
        except (AttributeError, TypeError) :
            print(f"Warning: Error in distance calculation components for {body1.name}, {body2.name}")
            return 0.0
    else:
        if not isinstance(body1, Planetary_Body): 
            raise TypeError("get_body_distance requires body1 to be Planetary_Body")
        else: 
            raise TypeError("get_body_distance requires body2 to be Planetary_Body")

#==============================================================================
#                                  Vector3 Class
#==============================================================================
class Vector3:

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
    
    #--------------------------- Comparison Method ----------------------------    
    def __eq__(self, scalar):
        """Compare if 2 vectors are equal
        
        Method Arguments:
        * scalar: A Vector3

        Output:
        * True: the 2 vectors hold the same data
        * False: any of the data held differs
        
        uses numpy isclos() to compare floats
        """
        if isinstance(scalar, Vector3):
            return (np.isclose(self.x, scalar.x) and
                    np.isclose(self.y, scalar.y) and
                    np.isclose(self.z, scalar.z))
        return False
    
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
            return Vector3(self.x + scalar.x, self.y + scalar.y, self.z + scalar.z)
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
            return Vector3(self.x - scalar.x, self.y - scalar.y, self.z - scalar.z)
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
        if isinstance(scalar, Vector3): # Component-wise
            return Vector3(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
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
        if isinstance(scalar, Vector3): 
            if scalar.x == 0 or scalar.y == 0 or scalar.z == 0:
                raise ValueError("Component-wise division by Vector3 containing zero.")
            return Vector3(self.x / scalar.x, self.y / scalar.y, self.z / scalar.z)
        else:
            if scalar == 0:
                raise ValueError("Vector3 division by zero scalar.")
            return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
            
    def magnitude(self):
        """Return the magnitude of this vector
        
        Method Arguments:
        * None

        Output:
        * The magnitude of this Vector3.
        """
        return np.sqrt( ( self.x ** 2 ) + ( self.y ** 2 ) + ( self.z ** 2) ) 

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

    def to_list(self): 
        """Return list of this Vector3.
        
        Method Arguments:
        * None
        """
        return [self.x, self.y, self.z]
    
    def copy(self): 
        """Return copy of this Vector3.
        
        Method Arguments:
        * None
        """
        return Vector3(self.x, self.y, self.z)
    
    def __str__(self): 
        """Return formatted string this Vector3.
        
        Method Arguments:
        * None
        """
        return f"Vector3(x={self.x:.4g}, y={self.y:.4g}, z={self.z:.4g})"


#==============================================================================
#                             Planetary_Body Class
#==============================================================================
class Planetary_Body: 
    km_per_s_to_AU_per_month = KM_PER_S_TO_AU_PER_MONTH 
    
    def __init__(self, mass_val = 0.0, pos_vector = None, 
                 vel_vector = None, name_val = ""):
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
        self.mass = float(mass_val) # MEarth
        self.pos = pos_vector if pos_vector is not None else Vector3() # AU
        self.velocity = vel_vector if vel_vector is not None else Vector3() # km/s
    
    def __eq__(self, scalar):
        """Compare if 2 bodies are equal
        
        Method Arguments:
        * other: A body

        Output:
        * True: the 2 bodies hold the same data
        * False: any of the data held differs
        
        uses numpy isclos() to compare floats
        """
        if isinstance(scalar, Planetary_Body):
            m = np.isclose(self.mass, scalar.mass)
            p = (self.pos == scalar.pos)
            v = (self.velocity == scalar.velocity)
            n = (self.name == scalar.name)
            return m and p and v and n
        return False
    
    @staticmethod
    def calculate_gravitational_force_exerted_by_on(acting_body, target_body):
        """Calculates force BY acting_body ON target_body. Uses G_ASTRO_MONTHS.
        Returns force in MEarth * AU / month^2.
        """
        r_vector = acting_body.pos - target_body.pos 
        dist_sq = float(r_vector.x)**2 + float(r_vector.y)**2 + float(r_vector.z)**2 
        if dist_sq == 0:
            return Vector3(0, 0, 0) 
        dist = np.sqrt(dist_sq)
        if dist == 0: 
            return Vector3(0,0,0)
        
        # F_vec = (G * M1 * M2 / r^3) * r_vector
        force_scalar_part = G_ASTRO_MONTHS * float(acting_body.mass) * float(target_body.mass) / (dist_sq * dist)
        force_vector = r_vector * force_scalar_part
        return force_vector
    
    @staticmethod # Added @staticmethod
    def calculate_gravity_field(exerting_body, target_body):
        """Returns the acceleration due to gravity an exerting object applies 
        to a target object.
        
        Method Arguments:
        * exerting_body: the body applying the force
        * target_body: the body being pulled

        Output:
        * The acceleration due to Gravity experienced by the target body.
        
        Uses the Gravitational Field Equation, which derives from Netwon's Law 
        Universal Gravitation and Newton's second law of Motion.
        
        G = Gravitational Constant
        r = distance between planets' center of mass
        M = mass of the exerting body
        a = Acceleration due to gravity

        a = ( G * M ) / r^2
        """
        import scipy.constants as sp
        
        # Gravitational Field Vars
        G = G_ASTRO_MONTHS
        r = get_body_distance(target_body, exerting_body)
        
        #Gravitational Field Equation
        # By dividing the gravitational force by an extra r, we don't have to 
        # divide the distance by r to get the direction of the acceleration
        grav_force_div_r = G * exerting_body.mass / r**3
        
        # Find the displacement of the bodies or (direction * r)
        accel = (exerting_body.pos - target_body.pos) * grav_force_div_r
        
        return accel

    def as_type_list(self):
        """Get the body data as a list.
        
        Method Arguments:
        * None

        Output:
        * The body class as a list.
        
        Values are in the order of Name, Mass, Pos.x, Pos.y, Pos.z, Vel.x, 
        Vel.y, Vel.z.
        """
        return [self.name, self.mass, self.pos.x, self.pos.y, self.pos.z,
                self.velocity.x, self.velocity.y, self.velocity.z]
    
    def get_gravitatonal_acceleration_rk4(self, body_index, system, delta_time):
        """
        Original RK4 method.
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
        self.pos = self.pos + (self.velocity * delta_time * Planetary_Body.km_per_s_to_AU_per_month)
        
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
        
    def apply_acceleration(self, accel_kms_month, delta_time):
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
        self.velocity = self.velocity + (accel_kms_month * delta_time) 

    def __str__(self):
        return (f"PlanetaryBody(Name: {self.name}, Mass: {self.mass:.3g} MEarth, "
                f"Pos: {self.pos} AU, Vel: {self.velocity} km/s)")
    

#==============================================================================
#                                  Test Code
#==============================================================================
if __name__ == "__main__": 
    print("Body.py - Phase 1 Refinements Test")
    print(f"G_ASTRO_MONTHS = {G_ASTRO_MONTHS:.4e} AU^3 MEarth^-1 month^-2")
    print(f"KM_PER_S_TO_AU_PER_MONTH = {KM_PER_S_TO_AU_PER_MONTH:.6f}")
    print(f"CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH = {CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH:.6f}")

    print("\nTesting Vector3 equality:")
    v1 = Vector3(1.00000001, 2.0, 3.0)
    v2 = Vector3(1.0, 2.0, 3.0)
    v3 = Vector3(1.0, 2.5, 3.0)
    print(f"v1 == v2 (expect True): {v1 == v2}")
    print(f"v1 == v3 (expect False): {v1 == v3}")

    print("\nTesting Planetary_Body equality:")
    b1 = Planetary_Body(mass_val=1.0, pos_vector=v1, vel_vector=v2, name_val="Body1")
    b2 = Planetary_Body(mass_val=1.00000001, pos_vector=v2, vel_vector=v1, name_val="Body1")
    b3 = Planetary_Body(mass_val=1.0, pos_vector=v1, vel_vector=v3, name_val="Body1")
    print(f"b1 == b2 (expect True due to np.isclose): {b1 == b2}")
    print(f"b1 == b3 (expect False): {b1 == b3}")

    print("\nTesting calculate_gravity_field:")
    sun_test = Planetary_Body(mass_val=333000.0, pos_vector=Vector3(0.0,0.0,0.0), name_val="Sun")
    earth_test = Planetary_Body(mass_val=1.0, pos_vector=Vector3(1.0,0.0,0.0), name_val="Earth")
    
    accel_on_earth = Planetary_Body.calculate_gravity_field(sun_test, earth_test)
    print(f"Calculated Accel on Earth by Sun: {accel_on_earth} AU/month^2")
    expected_accel_mag = G_ASTRO_MONTHS * sun_test.mass / (1.0**2)
    print(f"Expected accel magnitude: ~{expected_accel_mag:.4e} AU/month^2 (towards Sun, so x should be negative)")

    print("\nTesting calculate_gravitational_force_exerted_by_on:")
    force_on_earth = Planetary_Body.calculate_gravitational_force_exerted_by_on(sun_test, earth_test)
    print(f"Calculated Force on Earth by Sun: {force_on_earth} MEarth*AU/month^2")
    expected_force_mag = G_ASTRO_MONTHS * sun_test.mass * earth_test.mass / (1.0**2)
    print(f"Expected force magnitude: ~{expected_force_mag:.4e} MEarth*AU/month^2 (towards Sun)")

    print("\nTesting get_body_distance:")
    dist = get_body_distance(sun_test, earth_test)
    print(f"Distance Sun-Earth: {dist} AU (Expected: 1.0 AU)")

    # Test write_system and read_system
    test_system_out = [sun_test, earth_test]
    csv_test_file = "temp_body_test.csv"
    print(f"\nWriting to {csv_test_file}...")
    write_system(test_system_out, csv_test_file)
    print(f"Reading from {csv_test_file}...")
    read_back_system = read_system(csv_test_file)
    print("Read back system:")
    for i, body in enumerate(read_back_system):
        print(f"  Body {i}: {body}")
        print(f"  Matches original? {body == test_system_out[i]}")
    
    import os
    if os.path.exists(csv_test_file):
        os.remove(csv_test_file)