from waypoint_core.distance import Distance
from waypoint_core.trail import (
    DayHike, GuidedDayHike, BackpackingRoute, TrailRun, ScenicTrailRun, FakeTrail
)

# a mixed list of trail types
trails = [
    DayHike("T1", "Maple Ridge", Distance(12, "km"), 400, "moderate"),
    GuidedDayHike("T2", "Summit View", Distance(8, "km"), 600, "hard", "Maria"),
    BackpackingRoute("T3", "Wilderness Loop", Distance(45, "km"), 1800, "expert", 3),
    TrailRun("T4", "River Sprint", Distance(10, "km"), 200, "easy"),
    ScenicTrailRun("T5", "Peak Runner", Distance(15, "km"), 900, "hard"),
    FakeTrail("Test Trail"),
]

# Polymorphic loop
print("=" * 60)
print("WAYPOINT — Trail estimated times")
print("=" * 60)
for trail in trails:
    print("%.2f hrs  |  %s" % (trail.estimated_time(), trail.summary()))

# Distance operators
print()
print("=" * 60)
print("Distance operator tests")
print("=" * 60)
d1 = Distance(3, "km")
d2 = Distance(2, "km")
d3 = Distance(2, "mi")

print("d1 = %s,  d2 = %s,  d3 = %s (mi)" % (d1, d2, d3))
print("d1 + d2 =", d1 + d2)
print("d1 + d3 (mixed units, auto-converts to km) =", d1 + d3)
print("d1 > d2 :", d1 > d2)
print("d2 < d1 :", d2 < d1)
print("d1 == d1:", d1 == Distance(3, "km"))

# Method Resolution Order
print()
print("=" * 60)
print("ScenicTrailRun MRO:")
print("=" * 60)
for cls in ScenicTrailRun.__mro__:
    print(" ", cls)