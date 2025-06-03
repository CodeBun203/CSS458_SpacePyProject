'''
    Note:
        There are certain files that have not been created, or added, yet. Some tests were
        written with the assumption to be uncommented out once those files have been imported
        into this file.

        Current classes that are finished testing:
        Vector3

        Needs to be fixed:
        All functions within body testing

        Needs to be rewritten:
        Everything that's in comments (cause i realized that they dont call
        the funtion until now)


''' 
import numpy as np
import math as m
import unittest as ut
import os
import csv
from Body import Planetary_Body, Vector3
#import Simulation

# Placeholder constants
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
#~{}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~{}~

        result_mag = f1.magnitude()
        result_norm = f1.normalize()

        expected_mag = m.sqrt(f1.x**2 + f1.y**2 + f1.z**2)

        if expected_mag != 0:
            expected_norm = Vector3(f1.x / expected_mag, f1.y / expected_mag, f1.z / expected_mag)
        else:
            expected_norm = Vector3(0,0,0)
       
        mag_pass = m.isclose(result_mag, expected_mag)
        norm_pass = (
            m.isclose(result_norm.x, expected_norm.x) and
            m.isclose(result_norm.y, expected_norm.y) and
            m.isclose(result_norm.z, expected_norm.z)
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
            body = Planetary_Body("Test", 1.0, Vector3(0, 0, 0), Vector3(1, 1, 1))
            dt = 1.0  # 1 second
            body.update(dt)

            expected_position = Vector3(1, 1, 1)

            pos_pass = (
                m.isclose(body.position.x, expected_position.x) and
                m.isclose(body.position.y, expected_position.y) and
                m.isclose(body.position.z, expected_position.z)
            )

            if pos_pass:
                print("\nTest Update Position: Passed")
            else:
                print("\nTest Update Position: Failed")
                print(f"Expected Position: {expected_position}\nGot: {body.position}")
          
    def test_asType_list(self):
        body = Planetary_Body("Test", 1.0, Vector3(1, 2, 3), Vector3(4, 5, 6))
        result = body.as_type_list()
        expected = [1, 2, 3, 4, 5, 6]

        if result == expected:
            print("\nTest as_type_list: Passed")
        else:
            print("\nTest as_type_list: Failed")
            print(f"Expected: {expected}\nGot: {result}")
                
    def test_grav_accel_RK4(self):
        body1 = Planetary_Body("Earth", 5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0))
        body2 = Planetary_Body("Moon", 7.348e22, Vector3(384400000, 0, 0), Vector3(0, 0, 0))

        accel = body1.compute_gravitational_acceleration_rk4([body2])

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
        body1 = Planetary_Body("Earth", 5.972e24, Vector3(0, 0, 0), Vector3(0, 0, 0))
        body2 = Planetary_Body("Moon", 7.348e22, Vector3(384400000, 0, 0), Vector3(0, 0, 0))  # 384,400 km away

        result_force = body1.exert_gravitational_force(body2)

        G = 6.67430e-11
        r = 384400000
        expected_magnitude = G * body1.mass * body2.mass / (r ** 2)
        expected_force = Vector3(expected_magnitude, 0, 0)

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

'''
class TestGravitationalPhysics(ut.TestCase):
    def test_force_symmetric(self):
  
        from simulation import calculate_gravitational_force
        f1 = calculate_gravitational_force(5, 5, 2)
        f2 = calculate_gravitational_force(5, 5, -2)
        self.assertAlmostEqual(f1, f2)

    def test_zero_distance(self):
        from simulation import calculate_gravitational_force
        with self.assertRaises(ZeroDivisionError):
            calculate_gravitational_force(5, 5, 0)



class TestLagrangePoints(ut.TestCase):
    def setUp(self):
        from simulation import Body, Simulator
        self.sun = Body("Sun", 1.0, [0, 0, 0], [0, 0, 0])
        self.earth = Body("Earth", 3e-6, [1, 0, 0], [0, 30, 0])
        self.sim = Simulator([self.sun, self.earth])

    def test_l4_point_stability(self):
        from simulation import Body, calculate_lagrange_point
        l4 = calculate_lagrange_point(self.sun, self.earth, "L4")
        probe = Body("Probe", 1e-10, l4, [0, 30, 0])
        self.sim.add_body(probe)

        initial_pos = np.array(probe.position)
        self.sim.run(1000)
        final_pos = np.array(probe.position)

        drift = np.linalg.norm(final_pos - initial_pos)
        self.assertLess(drift, DRIFT_TOLERANCE, "Probe drifted too far from Lagrange point")



class TestOrbitalBehavior(ut.TestCase):
    def setUp(self):
        from simulation import Body, Simulator
        self.sun = Body("Sun", 1.0, [0, 0, 0], [0, 0, 0])
        self.planet = Body("Earth", 3e-6, [1, 0, 0], [0, 30, 0])
        self.sim = Simulator([self.sun, self.planet])

    def test_elliptical_orbit_consistency(self):
        initial = np.array(self.planet.position)
        self.sim.run(365 * 12)  # simulate 1 year assuming monthly timesteps
        final = np.array(self.planet.position)

        displacement = np.linalg.norm(final - initial)
        self.assertLess(displacement, 0.1, "Planet did not return to near starting position")




class TestDataLogging(ut.TestCase):
    def test_csv_logging_format(self):
        from simulation import Simulator, Body
        sun = Body("Sun", 1.0, [0, 0, 0], [0, 0, 0])
        earth = Body("Earth", 3e-6, [1, 0, 0], [0, 30, 0])
        sim = Simulator([sun, earth])
        sim.run_and_log("test_output.csv")

        with open("test_output.csv", newline='') as f:
            reader = csv.reader(f)
            headers = next(reader)
            expected = ["timestamp", "id", "mass", "x", "y", "z", "vx", "vy", "vz"]
            self.assertEqual(headers, expected)

        os.remove("test_output.csv")
'''
if __name__ == '__main__':
    ut.main()
