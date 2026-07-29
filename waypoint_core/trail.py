from abc import ABC, abstractmethod
from waypoint_core.distance import Distance


# Mixins

class ElevationMixin:
    """
    Mixin that adds elevation grade calculation to a trail.
    Grade is expressed as a percentage: elevation gain / distance in metres.
    """

    def grade_percent(self):
        """
        Calculates the elevation grade as a percentage.

        Parameters: None

        Returns:
        float: The grade percentage rounded to 2 decimal places.
        """
        distance_m = self.distance._to_km() * 1000
        if distance_m == 0:
            return 0.0
        return round((self.elevation_gain_m / distance_m) * 100, 2)


class RatingMixin:
    """
    Mixin that adds a star-rating system to a trail.
    Ratings are stored as a list of integers (1-5).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ratings = []

    def add_rating(self, stars):
        """
        Adds a star rating to the trail.

        Parameters:
        stars (int): A rating between 1 and 5 inclusive.

        Returns: None
        """
        if not 1 <= stars <= 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._ratings.append(stars)

    def average_rating(self):
        """
        Returns the average star rating.

        Parameters: None

        Returns:
        float: The average rating, or 0.0 if no ratings exist.
        """
        if not self._ratings:
            return 0.0
        return round(sum(self._ratings) / len(self._ratings), 2)


# Abstract base class

class Trail(ABC):
    """
    Abstract base class representing a hiking trail.
    Subclasses must implement estimated_time() and summary().

    Parameters:
    trail_id (str): Unique identifier for the trail.
    name (str): Name of the trail.
    distance (Distance): A Distance object representing trail length.
    elevation_gain_m (float): Elevation gain in metres.
    difficulty (str): One of 'easy', 'moderate', 'hard', 'expert'.

    Returns: A Trail object (only via subclasses).
    """

    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard", "expert")
    default_unit = "km"

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty):
        self.trail_id         = trail_id
        self.name             = name
        self.distance         = distance
        self.elevation_gain_m = elevation_gain_m
        self._difficulty      = None
        self.set_difficulty(difficulty)

    @abstractmethod
    def estimated_time(self):
        """
        Returns the estimated time to complete the trail in hours.

        Returns:
        float: Estimated hours as a float.
        """
        pass

    @abstractmethod
    def summary(self):
        """
        Returns a one-line human-readable summary of the trail.

        Returns:
        str: A summary string.
        """
        pass

    def set_difficulty(self, difficulty):
        """
        This sets the difficulty, rejecting invalid values.

        Parameters:
        difficulty (str): One of 'easy', 'moderate', 'hard', 'expert'.

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
        Alternate constructor — builds a Trail subclass from a dictionary.

        Parameters:
        data (dict): Must contain keys: 'id', 'name', 'distance',
        'distance_unit', 'elevation_gain_m', 'difficulty'.

        Returns:
        Trail: A new Trail subclass object.
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


# Concrete subclasses

class DayHike(Trail):
    """
    A single-day hiking trail.
    Estimated time is based on a pace of 4 km/h plus 1 hour per 500m elevation.

    Parameters: same as Trail.
    """

    def estimated_time(self):
        """
        Estimates time in hours at 4 km/h plus 1hr per 500m elevation gain.

        Returns:
        float: Estimated hours rounded to 2 decimal places.
        """
        moving_time    = self.distance._to_km() / 4.0
        elevation_time = self.elevation_gain_m / 500.0
        return round(moving_time + elevation_time, 2)

    def summary(self):
        """
        Returns a summary string for a day hike.

        Returns:
        str: One-line summary.
        """
        return "Day Hike: %s | %s | %dm gain | ~%.1f hrs" % (
            self.name, self.distance, self.elevation_gain_m, self.estimated_time()
        )


class GuidedDayHike(DayHike):
    """
    A guided single-day hike — extends DayHike with a guide name field.
    Adds 0.5 hours to account for guided briefing time.

    Parameters:
    guide_name (str): Name of the trail guide.
    All other parameters same as DayHike.
    """

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, guide_name):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.guide_name = guide_name

    def estimated_time(self):
        """
        Extends DayHike estimated_time by adding 0.5 hours for guided briefing.

        Returns:
        float: Estimated hours rounded to 2 decimal places.
        """
        return round(super().estimated_time() + 0.5, 2)

    def summary(self):
        """
        Returns a summary string for a guided day hike.

        Returns:
        str: One-line summary including guide name.
        """
        return "Guided Day Hike: %s | Guide: %s | %s | ~%.1f hrs" % (
            self.name, self.guide_name, self.distance, self.estimated_time()
        )


class BackpackingRoute(Trail):
    """
    A multi-day backpacking route.
    Estimated time is based on a slower pace of 3 km/h plus 1hr per 400m elevation.

    Parameters:
    num_days (int): Number of days the route takes.
    All other parameters same as Trail.
    """

    def __init__(self, trail_id, name, distance, elevation_gain_m, difficulty, num_days):
        super().__init__(trail_id, name, distance, elevation_gain_m, difficulty)
        self.num_days = num_days

    def estimated_time(self):
        """
        Estimates time in hours at 3 km/h plus 1hr per 400m elevation gain.

        Returns:
        float: Estimated hours rounded to 2 decimal places.
        """
        moving_time    = self.distance._to_km() / 3.0
        elevation_time = self.elevation_gain_m / 400.0
        return round(moving_time + elevation_time, 2)

    def summary(self):
        """
        Returns a summary string for a backpacking route.

        Returns:
        str: One-line summary including number of days.
        """
        return "Backpacking Route: %s | %d days | %s | ~%.1f hrs" % (
            self.name, self.num_days, self.distance, self.estimated_time()
        )


class TrailRun(Trail):
    """
    A trail running route.
    Estimated time is based on a fast pace of 10 km/h plus 1hr per 1000m elevation.

    Parameters: same as Trail.
    """

    def estimated_time(self):
        """
        Estimates time in hours at 10 km/h plus 1hr per 1000m elevation gain.

        Returns:
        float: Estimated hours rounded to 2 decimal places.
        """
        moving_time    = self.distance._to_km() / 10.0
        elevation_time = self.elevation_gain_m / 1000.0
        return round(moving_time + elevation_time, 2)

    def summary(self):
        """
        Returns a summary string for a trail run.

        Returns:
        str: One-line summary.
        """
        return "Trail Run: %s | %s | %dm gain | ~%.1f hrs" % (
            self.name, self.distance, self.elevation_gain_m, self.estimated_time()
        )


class ScenicTrailRun(ElevationMixin, RatingMixin, TrailRun):
    """
    A scenic trail run composed with ElevationMixin and RatingMixin.
    Method Resolution Order: ScenicTrailRun -> ElevationMixin -> RatingMixin -> TrailRun -> Trail

    Parameters: same as TrailRun.
    """

    def summary(self):
        """
        Returns a summary string including grade and average rating.

        Returns:
        str: One-line summary with grade % and star rating.
        """
        return "Scenic Trail Run: %s | %s | Grade: %.1f%% | Rating: %.1f stars" % (
            self.name, self.distance, self.grade_percent(), self.average_rating()
        )


# Duck-typed FakeTrail for testing 

class FakeTrail:
    """
    A duck-typed trail that inherits nothing but implements estimated_time()
    and summary() so it can participate in the polymorphic loop.

    Parameters:
    name (str): Name of the fake trail.
    """

    def __init__(self, name):
        self.name = name

    def estimated_time(self):
        """Returns a fixed estimated time of 1.0 hour."""
        return 1.0

    def summary(self):
        """Returns a simple summary string."""
        return "FakeTrail: %s | ~1.0 hrs" % self.name