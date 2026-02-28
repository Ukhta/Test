#!/usr/bin/env python3
"""
Example usage of the graphics elements library.
"""

from graphics_elements import Point, Line, Circle, Arc
import math

def main():
    print("=== Point Examples ===")
    p1 = Point(0, 0)
    p2 = Point(3, 4)
    print(f"Point 1: {p1}")
    print(f"Point 2: {p2}")
    print(f"Distance between points: {p1.distance_to(p2)}")
    print(f"Translated point: {p1.translate(5, 5)}")

    print("\n=== Line Examples ===")
    line = Line(p1, p2)
    print(f"Line: {line}")
    print(f"Length: {line.length}")
    print(f"Slope: {line.slope()}")
    print(f"Angle (degrees): {line.angle_degrees():.2f}")
    print(f"Midpoint: {line.midpoint()}")

    print("\n=== Circle Examples ===")
    center = Point(0, 0)
    circle = Circle(center, 5)
    print(f"Circle: {circle}")
    print(f"Diameter: {circle.diameter}")
    print(f"Circumference: {circle.circumference:.2f}")
    print(f"Area: {circle.area:.2f}")
    test_point = Point(3, 4)
    print(f"Does circle contain point {test_point}: {circle.contains_point(test_point)}")

    print("\n=== Arc Examples ===")
    arc = Arc(center, 5, 0, math.pi / 2)  # Quarter circle
    print(f"Arc: {arc}")
    print(f"Arc start point: {arc.start_point}")
    print(f"Arc end point: {arc.end_point}")
    print(f"Arc length: {arc.length:.2f}")
    print(f"Arc sweep angle: {arc.sweep_angle:.2f} radians")

if __name__ == "__main__":
    main()