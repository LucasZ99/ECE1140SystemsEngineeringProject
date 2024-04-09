import unittest

from Track_Controller_SW import Switch


class TestSwitching(unittest.TestCase):

    def test_switch_toggle(self):
        switch_1 = Switch(
            block=10,
            pos_a=11,
            pos_b=12,
            current_pos=11
        )

        switch_1.toggle()
        self.assertEqual(
            first=switch_1.current_pos,
            second=12
        )

    def test_switch_constructor_invalid(self):
        self.assertRaises(ValueError,
                          Switch,
                          10, 11, 12, 9)

    def test_switch_to_string(self):
        switch_1 = Switch(
            block=10,
            pos_a=11,
            pos_b=12,
            current_pos=11
        )
        test_str = "Switch at block 10 -> 11"

        self.assertEqual(test_str, switch_1.to_string())
