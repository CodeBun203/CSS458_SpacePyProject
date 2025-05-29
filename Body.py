class Vector3:
    def __init__(self, x_val = 0.0, y_val = 0.0, z_val = 0.0):
        self.x = x_val
        self.y = y_val
        self.z = z_val
        
    def __add__(self, scalar):
        if isinstance(Vector3(), scalar):
            return Vector3(self.x + scalar.x, self.y + scalar.y, self.z + scalar.z)
        else:
            return Vector3(self.x + scalar, self.y + scalar, self.z + scalar)
    
    def __sub__(self, scalar):
        if isinstance(Vector3(), scalar):
            return Vector3(self.x - scalar.x, self.y - scalar.y, self.z - scalar.z)
        else:
            return Vector3(self.x - scalar, self.y - scalar, self.z - scalar)
    
    def __mul__(self, scalar):
        if isinstance(Vector3(), scalar):
            return Vector3(self.x * scalar.x, self.y * scalar.y, self.z * scalar.z)
        else:
            return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        if isinstance(Vector3(), scalar):
            return Vector3(self.x / scalar.x, self.y / scalar.y, self.z / scalar.z)
        else:
            return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def normalize(self):
        import numpy as np
        component_sum = np.absolute(self.x) + np.absolute(self.y) +np.absolute(self.z)
        return Vector3(self.x / component_sum, self.y / component_sum, self.z / component_sum)
        




class Planetary_Body:
    def __init__(self, mass_val, pos_vector, vel_vector, name_val):
        self.name = name_val
        self.mass = mass_val
        self.pos = pos_vector
        self.velocity = vel_vector
    
    def update_pos(self, delta_time):
        self.pos = self.pos + (self.velocity * delta_time)
        
    def apply_force(self, force_vector):
        self.velocity = self.velocity + force_vector
    
    def get_body_distance(body1, body2):
        if isinstance(Planetary_Body(), body1) and isinstance(Planetary_Body(), body2):
            import numpy as np
            componenets = body1 - body2
            distance = np.sqrt(np.pow(componenets.x, 2) + np.pow(componenets.y, 2) + np.pow(componenets.z, 2))
            return distance
        else:
            if not isinstance(Planetary_Body(), body1):
                raise ValueError("get_body_distance(body1, body2) requires that the first parameter be of type Planetary_Body")
            else:
                raise ValueError("get_body_distance(body1, body2) requires that the second parameter be of type Planetary_Body")
    
    def apply_gravitatonal_force(body1, body2):
        if isinstance(Planetary_Body(), body1) and isinstance(Planetary_Body(), body2):
            import scipy.constants as sp
            import numpy as np
            m1 = body1.mass
            m2 = body2.mass
            G = sp.gravitational_constant
            r = Planetary_Body.get_body_distance(body1, body2)
            if r == 0:
                F = 0.0
            else:
                F = (G * m1 * m2) / np.pow(r, 2)
            
            body1.apply_force(F * (body1 - body2).normalize())
            body2.apply_force(F * (body2 - body1).normalize())            
        else:
            if not isinstance(Planetary_Body(), body1):
                raise ValueError("get_attraction_force(body1, body2) requires that the first parameter be of type Planetary_Body")
            else:
                raise ValueError("get_attraction_force(body1, body2) requires that the second parameter be of type Planetary_Body")
    
        
        