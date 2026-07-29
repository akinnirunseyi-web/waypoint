from waypoint_core.distance import Distance


class Trail:
    """
    Represents a hiking trail with a name, distance, elevation gain,
    and difficulty level.

    Parameters:
    trail_id (str): Unique identifier for the trail.
    name (str): Name of the trail.
    distance (Distance): A Distance object representing trail length.
    elevation_gain_m (float): Elevation gain in metres. Must be non-negative.
    difficulty (str): Must be one of 'easy', 'moderate', 'hard', 'expert'.

    Returns: A Trail object.
    """

    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard", "expert")
    default_unit = "km"

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty):
        self.trail_id        = trail_id
        self.name            = name
        self.distance        = distance
        self.elevation_gain_m = elevation_gain_m
        self._difficulty     = None
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        """
        This sets the difficulty, rejecting any value not in the allowed set.

        Parameters:
        difficulty (str): It has to be one of 'easy', 'moderate', 'hard', 'expert'.

        Returns: None
        """
        if difficulty not in self.ALLOWED_DIFFICULTIES:
            raise ValueError(
                "Invalid difficulty '%s'. Must be one of: %s"
                % (difficulty, self.ALLOWED_DIFFICULTIES)
            )
        self._difficulty = difficulty

    def get_difficulty(self):
        """Returns the current difficulty level."""
        return self._difficulty

    @classmethod
    def from_dict(cls, data):
        """
        Alternate constructor — builds a Trail from an API-shaped dictionary.

        Parameters:
        data (dict): Must contain keys: 'id', 'name', 'distance',
        'distance_unit', 'elevation_gain_m', 'difficulty'.

        Returns:
        Trail: A new Trail object.
        """
        distance = Distance(data["distance"], data.get("distance_unit", cls.default_unit))
        return cls(
            data["id"],
            data["name"],
            distance,
            data["elevation_gain_m"],
            data["difficulty"]
        )

    @staticmethod
    def is_valid_difficulty(difficulty):
        """
        This will check whether a difficulty string is valid.

        Parameters:
        difficulty (str): The difficulty string to check.

        Returns:
        bool: True if valid, False otherwise.
        """
        return difficulty in Trail.ALLOWED_DIFFICULTIES

    def __eq__(self, other):
        """Two trails are equal if they share the same trail_id."""
        if not isinstance(other, Trail):
            return False
        return self.trail_id == other.trail_id

    def __str__(self):
        return "%s (%s, %dm gain, %s)" % (
            self.name, self.distance, self.elevation_gain_m, self._difficulty
        )

    def __repr__(self):
        return "Trail(id=%s, name=%s)" % (self.trail_id, self.name)