import math
from typing import Tuple, Optional


class Point:
    """
    Represents a 2D point with x and y coordinates.
    """
    
    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate the Euclidean distance to another point."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def translate(self, dx: float, dy: float) -> 'Point':
        """Return a new point translated by dx and dy."""
        return Point(self.x + dx, self.y + dy)
    
    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y


class Line:
    """
    Represents a 2D line segment defined by two endpoints.
    """
    
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
    
    @property
    def length(self) -> float:
        """Calculate the length of the line segment."""
        return self.start.distance_to(self.end)
    
    def midpoint(self) -> Point:
        """Calculate the midpoint of the line segment."""
        return Point(
            (self.start.x + self.end.x) / 2,
            (self.start.y + self.end.y) / 2
        )
    
    def slope(self) -> Optional[float]:
        """Calculate the slope of the line. Returns None for vertical lines."""
        if self.start.x == self.end.x:
            return None
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)
    
    def angle_radians(self) -> float:
        """Calculate the angle of the line in radians."""
        return math.atan2(self.end.y - self.start.y, self.end.x - self.start.x)
    
    def angle_degrees(self) -> float:
        """Calculate the angle of the line in degrees."""
        return math.degrees(self.angle_radians())
    
    def translate(self, dx: float, dy: float) -> 'Line':
        """Return a new line translated by dx and dy."""
        return Line(
            self.start.translate(dx, dy),
            self.end.translate(dx, dy)
        )
    
    def __repr__(self) -> str:
        return f"Line(start={self.start}, end={self.end})"


class Circle:
    """
    Represents a 2D circle defined by center point and radius.
    """
    
    def __init__(self, center: Point, radius: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.center = center
        self.radius = radius
    
    @property
    def diameter(self) -> float:
        """Calculate the diameter of the circle."""
        return 2 * self.radius
    
    @property
    def circumference(self) -> float:
        """Calculate the circumference of the circle."""
        return 2 * math.pi * self.radius
    
    @property
    def area(self) -> float:
        """Calculate the area of the circle."""
        return math.pi * self.radius**2
    
    def contains_point(self, point: Point) -> bool:
        """Check if the circle contains a given point."""
        return self.center.distance_to(point) <= self.radius
    
    def intersects_circle(self, other: 'Circle') -> bool:
        """Check if this circle intersects with another circle."""
        centers_distance = self.center.distance_to(other.center)
        return centers_distance <= (self.radius + other.radius)
    
    def translate(self, dx: float, dy: float) -> 'Circle':
        """Return a new circle translated by dx and dy."""
        return Circle(
            self.center.translate(dx, dy),
            self.radius
        )
    
    def __repr__(self) -> str:
        return f"Circle(center={self.center}, radius={self.radius})"


class Arc:
    """
    Represents a 2D arc defined by center, radius, start angle, and end angle.
    Angles are in radians.
    """
    
    def __init__(self, center: Point, radius: float, start_angle: float, end_angle: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative")
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle
    
    @property
    def start_point(self) -> Point:
        """Calculate the starting point of the arc."""
        x = self.center.x + self.radius * math.cos(self.start_angle)
        y = self.center.y + self.radius * math.sin(self.start_angle)
        return Point(x, y)
    
    @property
    def end_point(self) -> Point:
        """Calculate the ending point of the arc."""
        x = self.center.x + self.radius * math.cos(self.end_angle)
        y = self.center.y + self.radius * math.sin(self.end_angle)
        return Point(x, y)
    
    @property
    def length(self) -> float:
        """Calculate the length of the arc."""
        # Normalize angles to calculate the difference
        angle_diff = self.end_angle - self.start_angle
        
        # Handle cases where the arc crosses the 0/2π boundary
        while angle_diff < 0:
            angle_diff += 2 * math.pi
        while angle_diff > 2 * math.pi:
            angle_diff -= 2 * math.pi
            
        return abs(angle_diff) * self.radius
    
    @property
    def sweep_angle(self) -> float:
        """Calculate the sweep angle of the arc in radians."""
        angle_diff = self.end_angle - self.start_angle
        
        # Handle cases where the arc crosses the 0/2π boundary
        while angle_diff < 0:
            angle_diff += 2 * math.pi
        while angle_diff > 2 * math.pi:
            angle_diff -= 2 * math.pi
            
        return abs(angle_diff)
    
    def midpoint(self) -> Point:
        """Calculate the midpoint of the arc."""
        mid_angle = self.start_angle + self.sweep_angle / 2
        x = self.center.x + self.radius * math.cos(mid_angle)
        y = self.center.y + self.radius * math.sin(mid_angle)
        return Point(x, y)
    
    def translate(self, dx: float, dy: float) -> 'Arc':
        """Return a new arc translated by dx and dy."""
        return Arc(
            self.center.translate(dx, dy),
            self.radius,
            self.start_angle,
            self.end_angle
        )
    
    def __repr__(self) -> str:
        return f"Arc(center={self.center}, radius={self.radius}, " \
               f"start_angle={self.start_angle:.2f}, end_angle={self.end_angle:.2f})"