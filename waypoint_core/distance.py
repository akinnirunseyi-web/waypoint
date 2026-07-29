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

    def _to_km(self):
        
        if self._unit == "km":
            return self._magnitude
        return self.convert().magnitude

    def __add__(self, other):
        """
        It will add two Distance objects. Mixed units are auto-converted to km.

        Parameters:
        other (Distance): The distance to add.

        Returns:
        Distance: A new Distance in km representing the sum.
        """
        return Distance(round(self._to_km() + other._to_km(), 4), "km")

    def __sub__(self, other):
        """
        This subtracts one Distance from another. Mixed units are auto-converted to km.

        Parameters:
        other (Distance): The distance to subtract.

        Returns:
        Distance: A new Distance in km representing the difference.
        """
        result = round(self._to_km() - other._to_km(), 4)
        if result < 0:
            raise ValueError("Subtraction would produce a negative distance.")
        return Distance(result, "km")

    def __eq__(self, other):
        """Two distances are equal if their km values are equal."""
        if not isinstance(other, Distance):
            return False
        return round(self._to_km(), 6) == round(other._to_km(), 6)

    def __lt__(self, other):
        """Returns True if this distance is less than other."""
        return self._to_km() < other._to_km()

    def __gt__(self, other):
        """Returns True if this distance is greater than other."""
        return self._to_km() > other._to_km()

    def __str__(self):
        return "%.2f %s" % (self._magnitude, self._unit)

    def __repr__(self):
        return "Distance(%s, '%s')" % (self._magnitude, self._unit)