from waypoint_core.distance import Distance


class Itinerary:
    """
    Represents an ordered collection of trails forming a trip itinerary.

    Parameters: None (trails are added via add_trail)

    Returns: An Itinerary object with an empty trail list.
    """

    def __init__(self):
        self._trails = []

    def add_trail(self, trail):
        """
        This adds a trail to the end of the itinerary.

        Parameters:
        trail (Trail): The trail to add.

        Returns: None
        """
        self._trails.append(trail)

    def total_distance(self):
        """
        It calculates the total distance of all trails in the itinerary.
        All distances are converted to km before summing them.

        Parameters: None

        Returns:
        Distance: A Distance object representing the total in km.
        """
        total_km = 0.0
        for trail in self._trails:
            d = trail.distance
            if d.unit == "km":
                total_km += d.magnitude
            else:
                total_km += d.convert().magnitude
        return Distance(round(total_km, 4), "km")

    def __str__(self):
        if not self._trails:
            return "Itinerary: no trails added yet."
        lines = ["Itinerary:"]
        for i, trail in enumerate(self._trails, 1):
            lines.append("  %d. %s" % (i, trail))
        lines.append("  Total distance: %s" % self.total_distance())
        return "\n".join(lines)