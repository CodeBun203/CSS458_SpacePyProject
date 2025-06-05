import math
import unittest
import os
import csv # For reading test CSV output if needed, though SimIO handles its own
from Body import Planetary_Body, Vector3, get_body_distance, \
                 write_system, read_system, \
                 G_ASTRO_MONTHS, KM_PER_S_TO_AU_PER_MONTH, AU_PER_MONTH_TO_KM_PER_SECOND, \
                 CONVERT_ACCEL_AU_MONTH2_TO_KM_S_MONTH # Ensure all needed constants are imported

# Assuming SimIO.py is in the same directory or accessible
import SimIO_CSV 

# Constants for testing
RELATIVE_TOLERANCE = 1e-5 # Relative tolerance for float comparisons
DEFAULT_TEST_FILENAME = "temp_test_system_for_testing_py.csv"
DEFAULT_SIMIO_TEST_DIR = "Test_Dumps_TestingPy" # Separate from main Dumps
DEFAULT_SIMIO_TEST_FILENAME = os.path.join(DEFAULT_SIMIO_TEST_DIR, "SimIO_Test_History.csv")

class TestVectorClass(unittest.TestCase):
    def test_vector_creation_and_attributes(self):
        v = Vector3(1.1, -2.2, 3.3)
        self.assertAlmostEqual(v.x, 1.1)
        self.assertAlmostEqual(v.y, -2.2)
        self.assertAlmostEqual(v.z, 3.3)
        v_default = Vector3()
        self.assertAlmostEqual(v_default.x, 0.0)

    def test_vector_math_operations(self):
        v1 = Vector3(1, 2, 3)
        v2 = Vector3(4, 5, 6)
        scalar = 2.0

        # Addition
        v_add = v1 + v2
        self.assertEqual(v_add, Vector3(5, 7, 9))
        v_add_scalar = v1 + scalar
        self.assertEqual(v_add_scalar, Vector3(3, 4, 5))

        # Subtraction
        v_sub = v1 - v2
        self.assertEqual(v_sub, Vector3(-3, -3, -3))
        v_sub_scalar = v1 - scalar
        self.assertEqual(v_sub_scalar, Vector3(-1, 0, 1))

        # Multiplication (scalar)
        v_mul_scalar = v1 * scalar
        self.assertEqual(v_mul_scalar, Vector3(2, 4, 6))
        v_rmul_scalar = scalar * v1
        self.assertEqual(v_rmul_scalar, Vector3(2, 4, 6))

        # Multiplication (component-wise with another Vector3 - if defined this way)
        # Your Vector3.__mul__ handles this.
        v_mul_vector = v1 * v2
        self.assertEqual(v_mul_vector, Vector3(4, 10, 18))


        # True Division (scalar)
        v_div_scalar = v1 / scalar
        self.assertEqual(v_div_scalar, Vector3(0.5, 1.0, 1.5))
        with self.assertRaises(ValueError): # Test division by zero scalar
            v_test = v1 / 0.0
        
        # True Division (component-wise with another Vector3 - if defined this way)
        # Your Vector3.__truediv__ handles this.
        v_div_vector = Vector3(8,10,12) / Vector3(2,2,3)
        self.assertEqual(v_div_vector, Vector3(4,5,4))
        with self.assertRaises(ValueError): # Test component-wise division by zero
            v_test = v1 / Vector3(1,0,1)


    def test_vector_magnitude_and_normalization(self):
        v = Vector3(3, 4, 0)
        self.assertAlmostEqual(v.magnitude(), 5.0, delta=RELATIVE_TOLERANCE)
        
        v_norm = v.normalize()
        self.assertAlmostEqual(v_norm.x, 0.6, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(v_norm.y, 0.8, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(v_norm.z, 0.0, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(v_norm.magnitude(), 1.0, delta=RELATIVE_TOLERANCE)

        v_zero = Vector3(0,0,0)
        self.assertAlmostEqual(v_zero.magnitude(), 0.0)
        v_zero_norm = v_zero.normalize()
        self.assertEqual(v_zero_norm, Vector3(0,0,0))

    def test_vector_helpers(self):
        v = Vector3(1.2, 3.4, 5.6)
        self.assertEqual(v.to_list(), [1.2, 3.4, 5.6])
        v_copy = v.copy()
        self.assertEqual(v, v_copy)
        self.assertIsNot(v, v_copy) # Ensure it's a different object
        self.assertEqual(str(v), "Vector3(x=1.2, y=3.4, z=5.6)") # Adjust format if needed
        self.assertEqual(repr(v), "Vector3(x=1.2, y=3.4, z=5.6)")


class TestPlanetaryBodyClass(unittest.TestCase):
    def setUp(self):
        # Common bodies for testing
        self.sun = Planetary_Body(mass_val=333000.0, 
                                  pos_vector=Vector3(0,0,0), 
                                  vel_vector=Vector3(0,0,0), 
                                  name_val="TestSun")
        self.earth = Planetary_Body(mass_val=1.0, 
                                   pos_vector=Vector3(1.0, 0, 0), # 1 AU on x-axis
                                   vel_vector=Vector3(0, KM_PER_S_TO_AU_PER_MONTH * AU_PER_MONTH_TO_KM_PER_SECOND, 0), # Approx 1 AU/month in km/s
                                   name_val="TestEarth")
        self.moon = Planetary_Body(mass_val=0.0123,
                                  pos_vector=Vector3(1.0 + 0.00257, 0, 0), # Moon near Earth
                                  vel_vector=Vector3(0, self.earth.velocity.y + (1.022 * KM_PER_S_TO_AU_PER_MONTH * AU_PER_MONTH_TO_KM_PER_SECOND), 0), # km/s
                                  name_val="TestMoon")

    def test_planetary_body_creation(self):
        self.assertEqual(self.earth.name, "TestEarth")
        self.assertAlmostEqual(self.earth.mass, 1.0)
        self.assertEqual(self.earth.pos, Vector3(1.0, 0, 0))
        # Check velocity components
        expected_earth_vy_kms = KM_PER_S_TO_AU_PER_MONTH * AU_PER_MONTH_TO_KM_PER_SECOND
        self.assertAlmostEqual(self.earth.velocity.y, expected_earth_vy_kms, delta=RELATIVE_TOLERANCE)


    def test_as_type_list(self):
        expected_list = ["TestEarth", 1.0, 1.0, 0.0, 0.0, 
                         0.0, self.earth.velocity.y, 0.0]
        actual_list = self.earth.as_type_list()
        self.assertEqual(len(actual_list), len(expected_list))
        for i in range(len(expected_list)):
            if isinstance(expected_list[i], float):
                self.assertAlmostEqual(actual_list[i], expected_list[i], delta=RELATIVE_TOLERANCE)
            else:
                self.assertEqual(actual_list[i], expected_list[i])

    def test_calculate_gravitational_force_exerted_by_on(self):
        # Test force Sun exerts on Earth
        force_on_earth = Planetary_Body.calculate_gravitational_force_exerted_by_on(self.sun, self.earth)
        
        # Expected force: F = G*M_sun*M_earth / r^2, directed towards Sun
        # r = 1 AU. Force vector should be (-F_mag, 0, 0)
        r_sq = 1.0**2
        expected_force_mag = G_ASTRO_MONTHS * self.sun.mass * self.earth.mass / r_sq
        
        self.assertAlmostEqual(force_on_earth.x, -expected_force_mag, delta=expected_force_mag * RELATIVE_TOLERANCE)
        self.assertAlmostEqual(force_on_earth.y, 0.0, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(force_on_earth.z, 0.0, delta=RELATIVE_TOLERANCE)

    def test_calculate_gravity_field(self):
        # Test field of Sun at Earth's position
        field_at_earth_pos = Planetary_Body.calculate_gravity_field(self.sun, self.earth) # Pass target_body
        
        # Expected field: a = G*M_sun / r^2, directed towards Sun
        # r = 1 AU. Field vector should be (-a_mag, 0, 0)
        r_sq = 1.0**2
        expected_field_mag = G_ASTRO_MONTHS * self.sun.mass / r_sq # AU/month^2
        
        self.assertAlmostEqual(field_at_earth_pos.x, -expected_field_mag, delta=abs(expected_field_mag * RELATIVE_TOLERANCE))
        self.assertAlmostEqual(field_at_earth_pos.y, 0.0, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(field_at_earth_pos.z, 0.0, delta=RELATIVE_TOLERANCE)

    def test_update_pos(self):
        # Earth's velocity is set to move ~1 AU in y-direction in 1 month (in km/s)
        # Original velocity: (0, KM_PER_S_TO_AU_PER_MONTH * AU_PER_MONTH_TO_KM_PER_SECOND, 0) km/s
        # KM_PER_S_TO_AU_PER_MONTH = 1 / AU_PER_MONTH_TO_KM_PER_SECOND
        # So, earth.velocity.y is 1.0 (if AU_PER_MONTH_TO_KM_PER_SECOND is the value that makes it 1 AU/month in km/s)
        # Let's set velocity to a simple value for testing update_pos more clearly
        test_body = Planetary_Body(mass_val=1.0, 
                                   pos_vector=Vector3(0,0,0), 
                                   # Velocity such that in 1 month it moves 1 AU in Y
                                   vel_vector=Vector3(0, AU_PER_MONTH_TO_KM_PER_SECOND, 0), 
                                   name_val="TestUpdater")
        dt_months = 1.0
        test_body.update_pos(dt_months) # pos_AU += vel_kms * dt_months * KM_PER_S_TO_AU_PER_MONTH
                                        # pos_AU += (AU_PER_MONTH_TO_KM_PER_SECOND) * 1.0 * (1.0/AU_PER_MONTH_TO_KM_PER_SECOND)
                                        # pos_AU += 1.0 AU in Y direction

        self.assertAlmostEqual(test_body.pos.x, 0.0, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(test_body.pos.y, 1.0, delta=RELATIVE_TOLERANCE)
        self.assertAlmostEqual(test_body.pos.z, 0.0, delta=RELATIVE_TOLERANCE)

    def test_planetary_body_equality(self):
        b1 = Planetary_Body(1.0, Vector3(1,2,3), Vector3(4,5,6), "BodyA")
        b2 = Planetary_Body(1.0, Vector3(1,2,3), Vector3(4,5,6), "BodyA")
        b3 = Planetary_Body(1.1, Vector3(1,2,3), Vector3(4,5,6), "BodyA") # Diff mass
        b4 = Planetary_Body(1.0, Vector3(0,2,3), Vector3(4,5,6), "BodyA") # Diff pos
        b5 = Planetary_Body(1.0, Vector3(1,2,3), Vector3(0,5,6), "BodyA") # Diff vel
        b6 = Planetary_Body(1.0, Vector3(1,2,3), Vector3(4,5,6), "BodyB") # Diff name

        self.assertEqual(b1, b2)
        self.assertNotEqual(b1, b3)
        self.assertNotEqual(b1, b4)
        self.assertNotEqual(b1, b5)
        self.assertNotEqual(b1, b6)


class TestBodyModuleFunctions(unittest.TestCase):
    def setUp(self):
        self.body1 = Planetary_Body(mass_val=1.0, pos_vector=Vector3(0,0,0), name_val="OriginBody")
        self.body2 = Planetary_Body(mass_val=0.1, pos_vector=Vector3(3,4,0), name_val="DistantBody") # Distance 5 AU
        self.test_system = [self.body1, self.body2]

    def test_get_body_distance(self):
        dist = get_body_distance(self.body1, self.body2)
        self.assertAlmostEqual(dist, 5.0, delta=RELATIVE_TOLERANCE) # Expected 5 AU

    def test_write_and_read_system(self):
        write_system(self.test_system, DEFAULT_TEST_FILENAME)
        read_back_system = read_system(DEFAULT_TEST_FILENAME)
        
        self.assertEqual(len(read_back_system), len(self.test_system))
        for original_body, loaded_body in zip(self.test_system, read_back_system):
            self.assertEqual(original_body, loaded_body) # Relies on Planetary_Body.__eq__

    def tearDown(self):
        if os.path.exists(DEFAULT_TEST_FILENAME):
            os.remove(DEFAULT_TEST_FILENAME)


class TestSimIO(unittest.TestCase):
    def setUp(self):
        self.test_bodies = [
            Planetary_Body(mass_val=1.0, pos_vector=Vector3(1,0,0), vel_vector=Vector3(0,1,0), name_val="BodyA"),
            Planetary_Body(mass_val=2.0, pos_vector=Vector3(0,1,0), vel_vector=Vector3(-1,0,0), name_val="BodyB")
        ]
        # Ensure the test dump directory exists and is empty
        if os.path.exists(DEFAULT_SIMIO_TEST_DIR):
            for f in os.listdir(DEFAULT_SIMIO_TEST_DIR):
                os.remove(os.path.join(DEFAULT_SIMIO_TEST_DIR, f))
        else:
            os.makedirs(DEFAULT_SIMIO_TEST_DIR, exist_ok=True)


    def test_initialize_and_append_dump_file(self):
        SimIO_CSV.initialize_dump_file(DEFAULT_SIMIO_TEST_FILENAME, self.test_bodies)
        
        # Verify file creation and header
        self.assertTrue(os.path.exists(DEFAULT_SIMIO_TEST_FILENAME))
        with open(DEFAULT_SIMIO_TEST_FILENAME, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            self.assertEqual(header, SimIO_CSV.DUMP_FILE_HEADER)
            # Check initial state rows (2 bodies)
            row1 = next(reader)
            self.assertEqual(int(row1[0]), 0) # TimeStep_Index
            self.assertAlmostEqual(float(row1[1]), 0.0) # Time_Months
            self.assertEqual(row1[2], "BodyA") # BodyName
            row2 = next(reader)
            self.assertEqual(row2[2], "BodyB")

        # Modify bodies for appending
        self.test_bodies[0].pos = Vector3(1.1, 0.1, 0)
        self.test_bodies[1].velocity = Vector3(-1.1, -0.1, 0)
        SimIO_CSV.append_to_dump_file(DEFAULT_SIMIO_TEST_FILENAME, 1, 0.1, self.test_bodies)

        with open(DEFAULT_SIMIO_TEST_FILENAME, 'r') as f:
            reader = csv.reader(f)
            all_rows = list(reader)
            # Header + 2 initial rows + 2 appended rows = 5 total rows
            self.assertEqual(len(all_rows), 1 + 2 + 2) 
            last_body_a_row = all_rows[3] # Data for BodyA at step 1
            self.assertEqual(int(last_body_a_row[0]), 1) # TimeStep_Index
            self.assertAlmostEqual(float(last_body_a_row[1]), 0.1) # Time_Months
            self.assertAlmostEqual(float(last_body_a_row[4]), 1.1) # PosX_AU

    def tearDown(self):
        # Clean up SimIO test files and directory
        if os.path.exists(DEFAULT_SIMIO_TEST_FILENAME):
            os.remove(DEFAULT_SIMIO_TEST_FILENAME)
        if os.path.exists(DEFAULT_SIMIO_TEST_DIR) and not os.listdir(DEFAULT_SIMIO_TEST_DIR):
            try:
                os.rmdir(DEFAULT_SIMIO_TEST_DIR)
            except OSError as e: # Might fail if other tests are creating files there too quickly
                print(f"Warning: Could not remove SimIO test directory {DEFAULT_SIMIO_TEST_DIR}: {e}")


class TestIntegration(unittest.TestCase):
    # These are more complex and would typically involve running a short simulation
    # and checking physical properties.

    def test_two_body_orbit_energy_conservation_placeholder(self):
        # 1. Setup a simple 2-body system (e.g., Earth around a fixed Sun, or two comparable masses)
        #    - Use Body.read_system from a predefined "TwoBody_Initial.csv" or create programmatically.
        # 2. Instantiate Simulation with these bodies and appropriate SimIO parameters (small number of steps).
        # 3. Run the simulation.
        # 4. For each step in the SimIO dump file (or in-memory history if preferred for test):
        #    a. Calculate total kinetic energy (0.5*m*v^2 for each body, sum them).
        #       - Need to convert km/s velocity to AU/month for KE in consistent units if PE is AU/MEarth based.
        #       - Or, convert everything to SI for energy calculation. This is tricky with mixed units.
        #       - Alternative: If using G_ASTRO_MONTHS, energy unit would be MEarth * (AU/month)^2.
        #         KE = 0.5 * mass_MEarth * (vel_AU_month.magnitude()**2)
        #         vel_AU_month = vel_kms * KM_PER_S_TO_AU_PER_MONTH
        #    b. Calculate total potential energy (-G_ASTRO_MONTHS * m1 * m2 / r for each pair).
        #    c. Sum KE + PE = Total Energy.
        # 5. Assert that Total Energy remains (almost) constant throughout the simulation.
        self.skipTest("Energy conservation test not yet implemented.")

    def test_two_body_orbit_angular_momentum_conservation_placeholder(self):
        # Similar to energy:
        # 1. Setup 2-body system.
        # 2. Run simulation.
        # 3. For each step:
        #    a. Calculate angular momentum for each body (L = r x p = r x (m*v)).
        #       - r is position vector from origin/CM (Vector3 AU).
        #       - v is velocity vector (Vector3 km/s, needs conversion to AU/month for consistency with r).
        #       - L_vec_AU_MEarth_AU_month = r_AU x (mass_MEarth * vel_AU_month)
        #    b. Sum angular momentum vectors for total system angular momentum.
        # 4. Assert that total angular momentum vector components remain (almost) constant.
        self.skipTest("Angular momentum conservation test not yet implemented.")

    def test_lagrange_point_stability_placeholder(self):
        # This is advanced.
        # 1. Setup a Sun-Earth like system.
        # 2. Calculate the position of L4 or L5.
        # 3. Place a massless (or very small mass) test particle at that L-point with the same
        #    angular velocity as the Earth around the Sun.
        # 4. Run simulation.
        # 5. Observe if the test particle stays near the L-point.
        self.skipTest("Lagrange point stability test not yet implemented.")


if __name__ == '__main__':
    unittest.main()