import time
import unittest
from SystemTime import SystemTime

class TestSystemTime(unittest.TestCase):
    def test_1s_multiplier(self):
        system_time = SystemTime()
        timer_0 = time.time()
        t_0 = system_time.time()


        time.sleep(1)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 1.0, 2, "time difference does not equal 1s")