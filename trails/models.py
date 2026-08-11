from django.db import models


class Park(models.Model):
    """
    Represents a provincial park that contains trails.

    Fields:
    name   (str): Name of the park.
    region (str): Geographic region where the park is located.
    """

    name   = models.CharField(max_length=200)
    region = models.CharField(max_length=200)

    def __str__(self):
        return "%s (%s)" % (self.name, self.region)

    class Meta:
        ordering = ["name"]


class Trail(models.Model):
    """
    Represents a hiking trail stored in the database.
    Each trail belongs to a Park via a ForeignKey relationship.

    Fields:
    name           (str):   Name of the trail.
    distance_km    (float): Trail length in kilometres.
    elevation_gain (int):   Elevation gain in metres.
    difficulty     (str):   One of easy, moderate, hard, expert.
    is_open        (bool):  Whether the trail is currently open.
    added          (date):  Date the trail was added (auto-set).
    park           (Park):  The park this trail belongs to. SET_NULL used so deleting a park does not delete its trails, rather, they become park-less instead, which preserves trail data integrity.
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
    park           = models.ForeignKey(
                        Park,
                        on_delete=models.SET_NULL,
                        null=True,
                        blank=True,
                        related_name="trails"
                    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["distance_km"]