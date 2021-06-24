class Point:

    def __init__(self, stx_str_line) -> None:
        self.stx_str_line = stx_str_line
        self.is_valid = False
        self._name = None
        self._x = None
        self._y = None
        self._z = None
        self._quality = None
        self._description = None

        self.process_string()

    def process_string(self):

        separated_data = self.stx_str_line.split()

        if len(separated_data) == 6:
            try:
                self._name = separated_data[0]
                self._y = float(separated_data[1])
                self._x = float(separated_data[2])
                self._z = float(separated_data[3])
                self._quality = int(separated_data[4])
                self._description = separated_data[5]
                self.is_valid = True
            except:
                self.is_valid = False

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def get_layer(self):
        return self._description
