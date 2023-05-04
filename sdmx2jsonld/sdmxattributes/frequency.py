from re import search
from sdmx2jsonld.sdmxattributes.exceptions import ClassFreqError


class Frequency:
    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form freq-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        m = search('FREQ-(.*)', value_upper)

        if m is not None:
            status = m.group(1)
            return status
        else:
            # We received a value that it is not following the template format
            raise ClassFreqError(value)
