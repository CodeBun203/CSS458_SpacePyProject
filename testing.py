'''
    Note:
        There are certain files that have not been created, or added, yet. Some tests were
        written with the assumption to be uncommented out once those files have been imported
        into this file. 
'''

import numpy as np
import unittest as ut
import os
import csv
#from body import Planetary_Body, Vector3
#from simulation import simulation as sim

# Placeholder constants
DRIFT_TOLERANCE = 0.05  # in AU


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


''' ~{}~~~~~~~~~~~~Uncomment me out~~~~~~~~~~~~~~~{}~~
class TestSimIntegration(ut.TestCase):
    def test_simulation_runs(self):
        sun = Body("Sun", 1.0, [0, 0, 0], [0, 0, 0])
        earth = Body("Earth", 3e-6, [1, 0, 0], [0, 30, 0])
        sim = Simulator([sun, earth])

        try:
            sim.run(100)
        except Exception as e:
            self.fail(f"Simulation failed with error: {e}")
~{}~~~~~~~~~~~~Uncomment me out~~~~~~~~~~~~~~~{}~~ '''

if __name__ == '__main__':
    ut.main()
