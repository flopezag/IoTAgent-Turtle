from re import search
from sdmx2jsonld.sdmxattributes.exceptions import ClassObsStatusError


class ObsStatus:
    status: list() = [
        "A",
        "B",
        "D",
        "E",
        "F",
        "G",
        "I",
        "K",
        "W",
        "O",
        "M",
        "P",
        "S",
        "L",
        "H",
        "Q",
        "J",
        "N",
        "U",
        "V"
    ]

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form obsStatus-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        if value_upper in self.status:
            return value_upper
        else:
            # we could receive a value in the format obsStatus-<value>
            m = search('OBSSTATUS-(.*)', value_upper)

            if m is not None:
                status = m.group(1)

                if status in self.status:
                    return status
                else:
                    message = f"ObsStatus value is not included in the list of available values,\n" \
                              f"    got:{value}\n" \
                              f"    expected:{['obsStatus-'+x for x in self.status]}"

                    raise ClassObsStatusError(data=value, message=message)

            else:
                # We received a value that it is not following the template format
                raise ClassObsStatusError(value)
