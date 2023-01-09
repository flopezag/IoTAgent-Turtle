from unittest import TestCase
from sdmx2jsonld.sdmxattributes.confirmationStatus import ConfStatus
from sdmx2jsonld.sdmxattributes.exceptions import ClassConfStatusError


class TestConfStatus(TestCase):
    def setUp(self):
        self.conversion = ConfStatus()

    def test_fix_value_data_in_predefined_values(self):
        value = 'F'
        expected = 'F'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

        value = 'f'
        expected = 'F'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

    def test_fix_value_data_in_predefined_values_with_prefix(self):
        value = 'confStatus-A'
        expected = 'A'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

        value = 'confstatus-a'
        expected = 'A'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

    def test_fix_value_data_with_valid_prefix_but_not_expected_value(self):
        value = 'confStatus-EEEEE'
        expected = "confStatus-EEEEE -> ConfStatus value is not included in the list of available values,\n" + \
                   "    got:confStatus-EEEEE\n" + \
                   "    expected:['confStatus-F', 'confStatus-N', 'confStatus-C', 'confStatus-D', 'confStatus-S', " \
                   "'confStatus-A', 'confStatus-O', 'confStatus-T', 'confStatus-G', 'confStatus-M', 'confStatus-E', " \
                   "'confStatus-P']"

        with self.assertRaises(ClassConfStatusError) as error:
            _ = self.conversion.fix_value(value=value)

        self.assertEqual(str(error.exception), expected)

    def test_fix_value_unexpected_value(self):
        value = 'EEEE'
        expected = 'Error...'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

        value = 'lkdjlks-A'
        expected = 'Error...'
        obtained = self.conversion.fix_value(value=value)
        assert obtained == expected, f"\nconfStatus was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"
