from django.test import TestCase, Client
from django.urls import reverse
from trails.models import Trail, Park
from waypoint_core.distance import Distance


class OpenTrailsQueryTest(TestCase):
    """
    Tests that the catalog query returns only open trails
    and excludes closed ones.
    """

    def setUp(self):
        """
        Creates test park and trails before each test.
        """
        self.park = Park.objects.create(
            name   = "Test Park",
            region = "Ontario"
        )
        Trail.objects.create(
            name           = "Open Trail",
            distance_km    = 5.0,
            elevation_gain = 100,
            difficulty     = "easy",
            is_open        = True,
            park           = self.park
        )
        Trail.objects.create(
            name           = "Closed Trail",
            distance_km    = 8.0,
            elevation_gain = 200,
            difficulty     = "moderate",
            is_open        = False,
            park           = self.park
        )

    def test_only_open_trails_appear_in_catalog(self):
        """
        The catalog view must only show open trails.
        """
        response = self.client.get(reverse("catalog"))
        self.assertEqual(response.status_code, 200)
        trails = response.context["trails"]
        for trail in trails:
            self.assertTrue(trail.is_open)

    def test_closed_trail_excluded_from_catalog(self):
        """
        A closed trail must not appear in the catalog queryset.
        """
        response = self.client.get(reverse("catalog"))
        trail_names = [t.name for t in response.context["trails"]]
        self.assertNotIn("Closed Trail", trail_names)

    def test_open_trail_appears_in_catalog(self):
        """
        An open trail must appear in the catalog queryset.
        """
        response = self.client.get(reverse("catalog"))
        trail_names = [t.name for t in response.context["trails"]]
        self.assertIn("Open Trail", trail_names)


class TrailDetailTest(TestCase):
    """
    Tests the park detail page and 404 behaviour.
    """

    def setUp(self):
        """
        Creates a test park before each test.
        """
        self.park = Park.objects.create(
            name   = "Detail Park",
            region = "British Columbia"
        )

    def test_park_detail_returns_200(self):
        """
        A valid park id must return a 200 response.
        """
        response = self.client.get(
            reverse("park-detail", args=[self.park.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_park_detail_404_for_invalid_id(self):
        """
        An invalid park id must return a 404 response.
        """
        response = self.client.get(
            reverse("park-detail", args=[99999])
        )
        self.assertEqual(response.status_code, 404)


class DistanceDomainTest(TestCase):
    """
    Tests the Distance domain class from waypoint_core.
    """

    def test_distance_rejects_negative_magnitude(self):
        """
        Creating a Distance with a negative magnitude must raise ValueError.
        """
        with self.assertRaises(ValueError):
            Distance(-1, "km")

    def test_distance_addition(self):
        """
        Adding two Distance objects must return the correct sum.
        """
        d1 = Distance(3, "km")
        d2 = Distance(2, "km")
        result = d1 + d2
        self.assertEqual(result.magnitude, 5.0)
        self.assertEqual(result.unit, "km")

    def test_distance_convert_roundtrip(self):
        """
        Converting km to mi and back must return a value
        within a small tolerance of the original.
        """
        d      = Distance(10, "km")
        in_mi  = d.convert()
        back   = in_mi.convert()
        self.assertAlmostEqual(back.magnitude, 10.0, places=2)