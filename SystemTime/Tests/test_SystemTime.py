import time
import unittest
import SystemTime


class TestSystemTime(unittest.TestCase):
    def test_1s_multiplier1(self):
        timer_0 = time.time()
        SystemTime.set_multiplier(1)
        t_0 = SystemTime.time()

        time.sleep(1)

        t_1 = SystemTime.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 1.0, 0, "time difference does not equal 1s")

    def test_1s_multiplier2(self):
        SystemTime.set_multiplier(2)
        t_0 = SystemTime.time()

        time.sleep(1)

        t_1 = SystemTime.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 2.0, 0, "time difference does not equal 2s")

    def test_10s_multiplier1(self):
        SystemTime.set_multiplier(1)
        t_0 = SystemTime.time()

        time.sleep(10)

        t_1 = SystemTime.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 10.0, 0, "time difference does not equal 10s")

    def test_10s_multiplier2(self):
        SystemTime.set_multiplier(2)
        t_0 = SystemTime.time()

        time.sleep(10)

        t_1 = SystemTime.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 20.0, 0, "time difference does not equal 20s")

    def test_10s_multiplier10(self):
        SystemTime.set_multiplier(10)
        t_0 = SystemTime.time()

        time.sleep(10)

        t_1 = SystemTime.time()

        time_elapsed = t_1 - t_0

        self.assertAlmostEqual(time_elapsed, 100, 0, "time difference does not equal 10s")
