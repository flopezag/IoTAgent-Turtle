from unittest import TestCase
from sdmx2jsonld.common.datatypeconversion import DataTypeConversion
import sys



class TestDataTypeConversion(TestCase):
    def setUp(self) -> None:
        pass

    def test_string_to_integer(self):
        dtc = DataTypeConversion()
        token_type = 'xsd:int'
        # token = Token('FORMATCONNECTOR', "432112")

        i: int = dtc.convert("432112", token_type)
        assert (i == 432112)

        i = dtc.convert("-100", token_type)
        assert (i == -100)

        i = dtc.convert("19223372036854775808", token_type)
        assert (i == 19223372036854775808)
        assert type(i) is int

        try:
            dtc.convert("invalid value", token_type)
            assert (False)
        except Exception:
            assert (True)

    def test_string_to_bool(self):
        dtc = DataTypeConversion()
        token_type = 'xsd:boolean'

        values = ("True", "true", "y", "yes", "T", "1", 1, True)
        for value in values:
            assert (dtc.convert(value, token_type))

        values = ("True", "true", "y", "yes", "T", "1", 1, True)
        for value in values:
            assert (dtc.convert(value, token_type))

        values = ("fAlsE", "False", "N", "No", "F", "0", "0.0", "", "None", None, [], {}, 0, 0.0)
        for value in values:
            assert (not dtc.convert(value, token_type))

        invalid_values = (5, 4.2, "invalid value", "nil")
        for value in invalid_values:
            try:
                dtc.convert(value, token_type)
                assert (False)
            except Exception:
                assert (True)

    def test_string_to_dates(self):
        dtc = DataTypeConversion()
        token_type = 'xsd:dateTime'

        dates = ("2022-01-15T08:00:00.000+00:00", "2022-01-10T09:00:00.000",
                 "2021-07-01T11:50:37.3", "2021-09-28T15:31:24.05",
                 "Mon Jan 13 09:52:52 MST 2014", "Thu Jun 02 11:56:53 CDT 2011",
                 "2022-12-12T10:00:00", "2022-05-11T10:00:00",
                 "Tue Dec 13 11:00:00 K 2022", "2021-07-01T11:58:08.642000")
        expected = ("2022-01-15T08:00:00+00:00", "2022-01-10T08:00:00+00:00",
                    "2021-07-01T09:50:37.300000+00:00", "2021-09-28T13:31:24.050000+00:00",
                    "2014-01-13T16:52:52+00:00", "2011-06-02T16:56:53+00:00",
                    "2022-12-12T09:00:00+00:00",  "2022-05-11T08:00:00+00:00",
                    "2022-12-13T01:00:00+00:00", "2021-07-01T09:58:08.642000+00:00")
                                               # "2021-07-01T09:58:08.642000+00:00"
        d = zip(dates, expected)

        for test_date, expected_date in d:
            print(test_date, " | ", dtc.convert(test_date, token_type))
            assert (expected_date == dtc.convert(test_date, token_type))