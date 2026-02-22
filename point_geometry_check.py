import math

def point_on_line(x, y, x1, y1, x2, y2, tolerance=1e-9):
    """
    Check if a point (x, y) lies on the line segment defined by endpoints (x1, y1) and (x2, y2).
    
    Args:
        x, y: Coordinates of the point to check
        x1, y1: First endpoint of the line segment
        x2, y2: Second endpoint of the line segment
        tolerance: Tolerance for floating point comparisons
    
    Returns:
        bool: True if the point lies on the line segment, False otherwise
    """
    # Check if the point is collinear with the line segment
    # Using cross product: if (P1P × P1P2) = 0, then points are collinear
    cross_product = (x - x1) * (y2 - y1) - (y - y1) * (x2 - x1)
    
    if abs(cross_product) > tolerance:
        return False  # Point is not on the line
    
    # Check if the point lies within the bounds of the line segment
    dot_product = (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)
    squared_distance = (x2 - x1)**2 + (y2 - y1)**2
    
    if dot_product < 0 or dot_product > squared_distance:
        return False  # Point is outside the line segment
    
    return True


def point_on_arc(x, y, cx, cy, radius, start_angle, end_angle, tolerance=1e-9):
    """
    Check if a point (x, y) lies on an arc defined by center (cx, cy),
    radius, and angular range from start_angle to end_angle (in radians).
    
    Args:
        x, y: Coordinates of the point to check
        cx, cy: Center of the arc
        radius: Radius of the arc
        start_angle: Start angle of the arc (in radians)
        end_angle: End angle of the arc (in radians)
        tolerance: Tolerance for floating point comparisons
    
    Returns:
        bool: True if the point lies on the arc, False otherwise
    """
    # Calculate distance from point to center
    dist_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
    
    # Check if the distance is approximately equal to the radius
    if abs(dist_to_center - radius) > tolerance:
        return False  # Point is not on the circle
    
    # Calculate the angle of the point relative to the center
    point_angle = math.atan2(y - cy, x - cx)
    
    # Normalize angles to [0, 2π) range
    start_angle = start_angle % (2 * math.pi)
    end_angle = end_angle % (2 * math.pi)
    point_angle = point_angle % (2 * math.pi)
    
    # Handle the case where the arc crosses the 0 angle boundary
    if start_angle <= end_angle:
        # Arc does not cross 0 boundary
        return start_angle <= point_angle <= end_angle
    else:
        # Arc crosses 0 boundary, so it spans from start_angle to 2π and from 0 to end_angle
        return point_angle >= start_angle or point_angle <= end_angle


def point_on_circle(x, y, cx, cy, radius, tolerance=1e-9):
    """
    Check if a point (x, y) lies on a full circle defined by center (cx, cy) and radius.
    
    Args:
        x, y: Coordinates of the point to check
        cx, cy: Center of the circle
        radius: Radius of the circle
        tolerance: Tolerance for floating point comparisons
    
    Returns:
        bool: True if the point lies on the circle, False otherwise
    """
    dist_to_center = math.sqrt((x - cx)**2 + (y - cy)**2)
    return abs(dist_to_center - radius) <= tolerance


def test_point_on_line():
    """Test the point_on_line function."""
    print("Testing point_on_line function:")
    
    # Test point on line segment
    result = point_on_line(1, 1, 0, 0, 2, 2, 1e-9)
    print(f"Point (1,1) on line segment (0,0)-(2,2): {result}")
    
    # Test point not on line segment
    result = point_on_line(1, 2, 0, 0, 2, 2, 1e-9)
    print(f"Point (1,2) on line segment (0,0)-(2,2): {result}")
    
    # Test point beyond line segment
    result = point_on_line(3, 3, 0, 0, 2, 2, 1e-9)
    print(f"Point (3,3) on line segment (0,0)-(2,2): {result}")


def test_point_on_arc():
    """Test the point_on_arc function."""
    print("\nTesting point_on_arc function:")
    
    # Test point on arc
    result = point_on_arc(1, 0, 0, 0, 1, 0, math.pi/2, 1e-9)
    print(f"Point (1,0) on arc centered at (0,0), radius 1, from 0 to π/2: {result}")
    
    # Test point not on arc
    result = point_on_arc(0, 1.5, 0, 0, 1, 0, math.pi/2, 1e-9)
    print(f"Point (0,1.5) on arc centered at (0,0), radius 1, from 0 to π/2: {result}")
    
    # Test point on circle but outside angle range
    result = point_on_arc(-1, 0, 0, 0, 1, 0, math.pi/2, 1e-9)
    print(f"Point (-1,0) on arc centered at (0,0), radius 1, from 0 to π/2: {result}")


def test_point_on_circle():
    """Test the point_on_circle function."""
    print("\nTesting point_on_circle function:")
    
    # Test point on circle
    result = point_on_circle(1, 0, 0, 0, 1, 1e-9)
    print(f"Point (1,0) on circle centered at (0,0), radius 1: {result}")
    
    # Test point not on circle
    result = point_on_circle(1.5, 0, 0, 0, 1, 1e-9)
    print(f"Point (1.5,0) on circle centered at (0,0), radius 1: {result}")


def main():
    """Main function to demonstrate the geometric algorithms."""
    print("Geometric Algorithms for Point Location")
    print("=" * 40)
    
    test_point_on_line()
    test_point_on_arc()
    test_point_on_circle()
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    main()