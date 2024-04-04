import unittest
import CTC.Route as Route
from CTC.Route import Stop
from CTC.Track import GREEN_LINE, GREEN_LINE_YARD_SPAWN, PATH


class TestRoute(unittest.TestCase):
    def test_find_path_no_retrace(self):
        block1 = 62
        block2 = 65
        expected_route = [62, 63, 64, 65]
        self.assertEqual(expected_route, Route.find_path(GREEN_LINE, block1, block2))

    def test_get_route_times(self):
        block1 = 62
        block2 = 65
        expected_travel_time_s = 18.43

        self.assertEqual(expected_travel_time_s, round(Route.get_block_pair_travel_time(GREEN_LINE, 62, 65), 2))

        print(Route.find_path(GREEN_LINE, 2, -16))
        print(PATH[GREEN_LINE].index(2), PATH[GREEN_LINE].index(16))
        self.assertEqual(40, round(Route.get_block_pair_travel_time(GREEN_LINE, 2, -16)))

    def test_find_path(self):
        # test from yard

        # test to yard

        # test through double tracked section
        block1 = 76
        block2 = 101
        expected_route = [76, -77, -78, -79, -80, -81, -82, -83, -84, -85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 85, 84, 83, 82, 81, 80, 79, 78, 77, 101]

        print(Route.find_path(GREEN_LINE, GREEN_LINE_YARD_SPAWN, 31))
        print(Route.find_route(GREEN_LINE, GREEN_LINE_YARD_SPAWN, 31))

        self.assertEqual(expected_route, Route.find_path(GREEN_LINE, block1, block2))


if __name__ == '__main__':
    unittest.main()
