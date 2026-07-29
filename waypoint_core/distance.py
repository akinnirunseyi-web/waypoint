class Distance:
    """
    Represents a distance value with a magnitude and a unit.

    Parameters:
    magnitude (float): The numeric distance value. Must be non-negative.
    unit (str): The unit of measurement. Must be 'km' or 'mi'.

    Returns: A Distance object.
    """

    def __init__(self, magnitude, unit):
        if magnitude < 0:
            raise ValueError("Distance magnitude cannot be negative.")
        if unit not in ("km", "mi"):
            raise ValueError("Unit must be 'km' or 'mi'.")
        self._magnitude = magnitude
        self._unit = unit

    @property
    def magnitude(self):
        """Read-only accessor for the magnitude."""
        return self._magnitude

    @property
    def unit(self):
        """Read-only accessor for the unit."""
        return self._unit

    def convert(self):
        """
        Converts the distance to the other unit.

        Returns:
        Distance: A new Distance object in the opposite unit.
        """
        if self._unit == "km":
            return Distance(round(self._magnitude * 0.621371, 4), "mi")
        else:
            return Distance(round(self._magnitude / 0.621371, 4), "km")

    def __str__(self):
        return "%.2f %s" % (self._magnitude, self._unit)

    def __repr__(self):
        return "Distance(%s, '%s')" % (self._magnitude, self._unit)