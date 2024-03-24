import time
import unittest
from SystemTime import SystemTime

class TestSystemTime(unittest.TestCase):
    def test_1s_multiplier1(self):
        system_time = SystemTime()
        timer_0 = time.time()
        t_0 = system_time.time()

        time.sleep(1)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 1.0, 0, "time difference does not equal 1s")

    def test_1s_multiplier2(self):
        system_time = SystemTime()
        timer_0 = time.time()
        system_time.set_multiplier(2)
        t_0 = system_time.time()

        time.sleep(1)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 2.0, 0, "time difference does not equal 2s")

    def test_10s_multiplier1(self):
        system_time = SystemTime()
        timer_0 = time.time()
        system_time.set_multiplier(1)
        t_0 = system_time.time()

        time.sleep(10)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 10.0, 0, "time difference does not equal 10s")

    def test_10s_multiplier2(self):
        system_time = SystemTime()
        timer_0 = time.time()
        system_time.set_multiplier(2)
        t_0 = system_time.time()

        time.sleep(10)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 20.0, 0, "time difference does not equal 20s")

    def test_60s_multiplier10(self):
        system_time = SystemTime()
        timer_0 = time.time()
        system_time.set_multiplier(10)
        t_0 = system_time.time()

        time.sleep(60)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 600, 0, "time difference does not equal 600s")


    def test_172800s_multiplier10(self):
        system_time = SystemTime()
        timer_0 = time.time()
        system_time.set_multiplier(10)
        t_0 = system_time.time()

        time.sleep(600000)

        t_1 = system_time.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 17280, 0, "time difference does not equal 172800s")