from django.db import models


class Trail(models.Model):
    """
    Represents a hiking trail stored in the database.

    Fields:
    name           (str):   Name of the trail.
    distance_km    (float): Trail length in kilometres.
    elevation_gain (int):   Elevation gain in metres.
    difficulty     (str):   One of easy, moderate, hard, expert.
    is_open        (bool):  Whether the trail is currently open.
    added          (date):  Date the trail was added (auto-set).
    """

    DIFFICULTY_CHOICES = [
        ("easy",     "Easy"),
        ("moderate", "Moderate"),
        ("hard",     "Hard"),
        ("expert",   "Expert"),
    ]

    name           = models.CharField(max_length=200)
    distance_km    = models.DecimalField(max_digits=6, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty     = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    is_open        = models.BooleanField(default=True)
    added          = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["distance_km"]