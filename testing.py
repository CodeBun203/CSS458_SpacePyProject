import math as m
import unittest as ut
import os
import csv
from Body import Planetary_Body, Vector3, get_body_distance, get_gravitatonal_force_euler, KM_PER_S_TO_AU_PER_MONTH, AU_PER_MONTH_TO_KM_PER_SECOND

# Constants
DRIFT_TOLERANCE = 0.05  # in AU

class TestVectorClass(ut.TestCase):
    def test_vector_math_func(self):
        
#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        f1 = Vector3(5, 5, 2)
        f2 = Vector3(5, 5, 2)
        f3 = Vector3(3, 3, 2)
        scalar = 2.0

#These need to be adjusted based on the numbers above

        result_add = f1.__add__(f2)
        result_sub = f1.__sub__(f3)
        result_mul = f1.__mul__(scalar)
        result_div = f1.__truediv__(scalar)
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~

#Testing Addition
        expected_add = f1 + f2

        add_= (m.isclose(result_add.x, expected_add.x) and
                  m.isclose(result_add.y, expected_add.y) and
                  m.isclose(result_add.z, expected_add.z))
        
        if add_ :
            print("\nTest Vector Math Function (Addition): Passed")
        else:
            print("\nTest Vector Math Function (Addition): Failed\n")
            print(f"Input Values: \nf1 = {f1} \nf2 = {f2}")
            print(f"\nExpected: \n{expected_add} \nGot: {result_add}")

#Testing Multiplication
        expected_mul = f1 * scalar

        mul_= (m.isclose(result_mul.x, expected_mul.x) and
                  m.isclose(result_mul.y, expected_mul.y) and
                  m.isclose(result_mul.z, expected_mul.z))
        
        if mul_ :
            print("\nTest Vector Math Function (Multiplication): Passed")
        else:
            print("\nTest Vector Math Function (Multiplication): Failed\n")
            print(f"Input Values: \nf1 = {f1} \nf2 = {f2}")
            print(f"\nExpected: \n{expected_mul} \nGot: {result_mul}")

#Testing Subtraction
        expected_sub = f1 - f3

        sub_= (m.isclose(result_sub.x, expected_sub.x) and
                  m.isclose(result_sub.y, expected_sub.y) and
                  m.isclose(result_sub.z, expected_sub.z))
        
        if sub_ :
            print("\nTest Vector Math Function (Subtraction): Passed")
        else:
            print("\nTest Vector Math Function (Subtraction): Failed\n")
            print(f"Input Values: \nf1 = {f1} \nf2 = {f2}")
            print(f"\nExpected: \n{expected_sub} \nGot: {result_sub}")


#Testing True Division
        expected_div = f1 / scalar

        div_= (m.isclose(result_div.x, expected_div.x) and
                  m.isclose(result_div.y, expected_div.y) and
                  m.isclose(result_div.z, expected_div.z))
        
        if div_ :
            print("\nTest Vector Math Function (True Division): Passed")
        else:
            print("\nTest Vector Math Function (True Division): Failed\n")
            print(f"Input Values: \nf1 = {f1} \nf2 = {f2}")
            print(f"\nExpected: \n{expected_div} \nGot: {result_div}")

    def test_vector_mag_and_norm(self):
       
#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        f1 = Vector3(3, 4, 10)
        expected_mag = m.sqrt(3**2 + 4**2 + 10**2) 
        expected_norm = Vector3(f1.x / expected_mag, f1.y / expected_mag, f1.z / expected_mag)
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~

        result_mag = f1.magnitude()
        result_norm = f1.normalize()

        if expected_mag != 0:
            expected_norm = Vector3(f1.x / expected_mag, f1.y / expected_mag, f1.z / expected_mag)
        else:
            expected_norm = Vector3(0,0,0)
       
        mag_pass = m.isclose(result_mag, expected_mag, rel_tol=1e-5)
        norm_pass = (
            m.isclose(result_norm.x, expected_norm.x, rel_tol=1e-5) and
            m.isclose(result_norm.y, expected_norm.y, rel_tol=1e-5) and
            m.isclose(result_norm.z, expected_norm.z, rel_tol=1e-5)
        )


        if mag_pass and norm_pass :
            print("\nTest Vector Magnitude and Normalization: Passed")
        else:
            print("\nTest Vector Magnitude and Normalization: Failed\n")
            print(f"Input Values: \nf1 = {f1}")
            print(f"\nExpected Magnitude: \n{expected_mag} \nGot: {result_mag}")
            print(f"\nExpected Normalization: \n{expected_norm} \nGot: {result_norm}")

class TestBody(ut.TestCase):
    def test_update_pos(self):

#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
            body = Planetary_Body(1.0, Vector3(0, 0, 0), Vector3(AU_PER_MONTH_TO_KM_PER_SECOND, AU_PER_MONTH_TO_KM_PER_SECOND, AU_PER_MONTH_TO_KM_PER_SECOND), "Test")
            dt = 1  # 1 month
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~
            body.update_pos(dt)
            result_pos = body.pos
            expected_position = Vector3(1, 1, 1)

            pos_pass = (
                m.isclose(body.pos.x, expected_position.x) and
                m.isclose(body.pos.y, expected_position.y) and
                m.isclose(body.pos.z, expected_position.z)
            )

            if pos_pass:
                print("\nTest Update Position: Passed")
            else:
                print("\nTest Update Position: Failed")
                print(f"Expected Position: {expected_position}\nGot: {result_pos}")
          
    def test_asType_list(self):

#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body = Planetary_Body(1.0, Vector3(1, 2, 3), Vector3(4, 5, 6), "Test")
        result = body.as_type_list()
        expected = ["Test", 1.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~

        if result == expected:
            print("\nTest as_type_list: Passed")
        else:
            print("\nTest as_type_list: Failed")
            print(f"Expected: {expected}\nGot: {result}")
                
    def test_grav_accel_RK4(self):

#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body1 = Planetary_Body(5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0), "Earth")
        body2 = Planetary_Body(7.348e22, Vector3(384400000, 0, 0), Vector3(0, 0, 0), "Moon")
        system = [body1, body2]
        timeStep = 1;
        accel = body1.get_gravitatonal_acceleration_rk4(0, system, timeStep)
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~

        G = 6.67430e-11
        r = 384400000
        expected_accel_x = G * body2.mass / (r ** 2)
        expected_accel = Vector3(expected_accel_x, 0, 0)

        accel_pass = (
            m.isclose(accel.x, expected_accel.x, rel_tol=1e-5) and
            m.isclose(accel.y, expected_accel.y, rel_tol=1e-5) and
            m.isclose(accel.z, expected_accel.z, rel_tol=1e-5)
        )

        if accel_pass:
            print("\nTest Gravitational Acceleration RK4: Passed")
        else:
            print("\nTest Gravitational Acceleration RK4: Failed")
            print(f"Expected: {expected_accel}\nGot: {accel}")

    def test_grav_force_extert_cal(self):
    
#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body1 = Planetary_Body(5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0), "Earth")
        body2 = Planetary_Body(7.348e22, Vector3(384400000, 0, 0), Vector3(0, 0, 0), "Moon")  # 384,400 km away
        expected_magnitude = 384400000 # meters
        expected_force = Vector3(expected_magnitude, 0, 0)
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~
        result_force = Planetary_Body.calculate_gravitational_force_exerted_by_on(body1,body2)

        G = 6.67430e-11
        r = 384400000

        force_pass = (
            m.isclose(result_force.x, expected_force.x, rel_tol=1e-5) and
            m.isclose(result_force.y, expected_force.y, rel_tol=1e-5) and
            m.isclose(result_force.z, expected_force.z, rel_tol=1e-5)
        )

        if force_pass:
            print("\nTest Gravitational Force Exert Calculation: Passed")
        else:
            print("\nTest Gravitational Force Exert Calculation: Failed")
            print(f"Expected: {expected_force}\nGot: {result_force}")

class TestPackageFunction(ut.TestCase):
    def test_body_dist(self):

#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body1 = Planetary_Body(5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0), "Earth")
        body2 = Planetary_Body(7.348e22, Vector3(380000, 20, 384399812.175), Vector3(0, 0, 0), "Moon")  
        expect_dist = 384400000 #AU 
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~
        
        result_dist = get_body_distance(body1, body2)
        dist_ = m.isclose(expect_dist, result_dist, rel_tol=1e-4)

        if dist_:
            print("\nTest Calculations of distance between two bodies: Passed")
        else:
            print("\nTest Calculations of distance between two bodies: Failed")
            print(f"\nExpected: {expect_dist}\nGot: {result_dist}")

    def test_grav_force_euler(self):
#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body1 = Planetary_Body(5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0), "Earth")
        body2 = Planetary_Body(7.348e22, Vector3(384400000, 0, 0), Vector3(0, 0, 0), "Moon")  
        expect_euler = 1.982e20
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~
        
        result_euler = get_gravitatonal_force_euler(body1, body2)
        euler_ = m.isclose(expect_euler, result_euler, rel_tol=1e-4)

        if euler_:
            print("\nTest Graviational Force using Euler: Passed")
        else:
            print("\nTest Graviational Force using Euler: Failed")
            print(f"\nExpected: {expect_euler}\nGot: {result_euler}")

    def test_write_and_read_csv(self):
#~{}~~~~~~~~~~~~~~User Modification Area~~~~~~~~~~~~~~{}~
        body1 = Planetary_Body(5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0), "Earth")
        body2 = Planetary_Body(7.348e22, Vector3(384400000, 0, 0), Vector3(0, 1022, 0), "Moon")
        test_system = [body1, body2]
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~
        test_file = "test_system.csv"
        
        write_ = write_system(test_system, test_file)
        read_ = read_system(test_file)
        
# Checking to see if the read was done correctly
        passed = True
        for original, loaded in zip(test_system, read_):
            if (str(original.mass) != str(loaded.mass) or
                str(original.name) != str(loaded.name) or
                str(original.pos.x) != str(loaded.pos.x) or
                str(original.pos.y) != str(loaded.pos.y) or
                str(original.pos.z) != str(loaded.pos.z) or
                str(original.vel.x) != str(loaded.vel.x) or
                str(original.vel.y) != str(loaded.vel.y) or
                str(original.vel.z) != str(loaded.vel.z)):
                passed = False
                break
          
                if passed == True:
                    print("\nTest Write to a CSV File: Passed")
                else:
                    print("\nTest Write to a CSV File: Failed")
# Clean up
        if os.path.exists(test_file):
            os.remove(test_file)
        
if __name__ == '__main__':
    ut.main()
