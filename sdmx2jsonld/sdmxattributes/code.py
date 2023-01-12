from re import search
from sdmx2jsonld.sdmxattributes.exceptions import ClassCode


class Code:
    status: list()
    type: str()
    data_range: list()

    def __init__(self, typecode):
        self.typecode = typecode

        if typecode == "decimals":
            self.data_range = range(0, 15)
        elif typecode == "unitMult":
            self.data_range = range(0, 13)

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form obsStatus-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        m = search(f'sdmx-code:{self.typecode}-(.*)', str(value))

        if m is not None:
            number = int(m.group(1))

            if number not in self.data_range:
                raise ClassCode(data=value,
                                message=f'{self.typecode} out of range, got: {number}   {self.data_range}')
        else:
            # The data is not following the sdmx-code:<value> we have to check which one
            # 1) Check if there is a value without the prefix
            m = search(f'{self.typecode}-(.*)', str(value))

            if m is not None:
                number = int(m.group(1))

                if number not in self.data_range:
                    raise ClassCode(data=value,
                                    message=f'{self.typecode} out of range, got: {number}   {self.data_range}')
            else:
                # We need to check is there is an integer number between a valid range
                if isinstance(value, int):
                    # Need to check the range
                    number = value
                    if number not in self.data_range:
                        raise ClassCode(data=value,
                                        message=f'{self.typecode} out of range, got: {number}   {self.data_range}')
                elif isinstance(value, str):
                    number = int(value)
                    if number not in self.data_range:
                        raise ClassCode(data=value,
                                        message=f'{self.typecode} out of range, got: {number}   {self.data_range}')
                else:
                    print("Error")

        return number
