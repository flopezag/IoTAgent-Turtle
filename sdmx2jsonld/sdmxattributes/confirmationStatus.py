from re import search
from sdmx2jsonld.sdmxattributes.exceptions import ClassConfStatusError


class ConfStatus:
    status: list() = [
        "F",
        "N",
        "C",
        "D",
        "S",
        "A",
        "O",
        "T",
        "G",
        "M",
        "E",
        "P"
    ]

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form confStatus-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        if value_upper in self.status:
            return value_upper
        else:
            # we could receive a value in the format confStatus-<value>
            m = search('CONFSTATUS-(.*)', value_upper)

            if m is not None:
                status = m.group(1)

                if status in self.status:
                    return status
                else:
                    message = f"ConfStatus value is not included in the list of available values,\n" \
                              f"    got:{value}\n" \
                              f"    expected:{['confStatus-'+x for x in self.status]}"

                    raise ClassConfStatusError(data=value, message=message)

            else:
                # We received a value that it is not following the template format
                raise ClassConfStatusError(value)
