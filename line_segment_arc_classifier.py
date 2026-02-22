import math
import random
from typing import List, Tuple, Union
from enum import Enum
try:
    import matplotlib.pyplot as plt
    import numpy as np
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class SegmentType(Enum):
    STRAIGHT = "straight"
    ARC = "arc"


class Point:
    """Represents a 2D point"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def distance_to(self, other: 'Point') -> float:
        """Calculate Euclidean distance to another point"""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"
    
    def to_tuple(self):
        """Convert to tuple representation"""
        return (self.x, self.y)


class LineSegment:
    """Represents a straight line segment between two points"""
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end
        self.length = start.distance_to(end)
    
    def get_point_at_distance(self, distance_from_start: float) -> Point:
        """Get a point at a specific distance from the start along the segment"""
        if distance_from_start <= 0:
            return Point(self.start.x, self.start.y)
        elif distance_from_start >= self.length:
            return Point(self.end.x, self.end.y)
        
        # Calculate the ratio along the segment
        ratio = distance_from_start / self.length
        x = self.start.x + ratio * (self.end.x - self.start.x)
        y = self.start.y + ratio * (self.end.y - self.start.y)
        return Point(x, y)
    
    def __repr__(self):
        return f"LineSegment({self.start} -> {self.end})"
    
    def get_points_for_plotting(self, num_points=100):
        """Generate points along the line for plotting purposes"""
        points_x = []
        points_y = []
        
        for i in range(num_points + 1):
            ratio = i / num_points
            x = self.start.x + ratio * (self.end.x - self.start.x)
            y = self.start.y + ratio * (self.end.y - self.start.y)
            points_x.append(x)
            points_y.append(y)
        
        return points_x, points_y


class ArcSegment:
    """Represents an arc segment defined by center, radius, start angle, and end angle"""
    def __init__(self, center: Point, radius: float, start_angle: float, end_angle: float):
        self.center = center
        self.radius = radius
        self.start_angle = start_angle  # in radians
        self.end_angle = end_angle      # in radians
        self.length = abs(end_angle - start_angle) * radius
    
    def get_point_at_distance(self, distance_from_start: float) -> Point:
        """Get a point at a specific distance from the start along the arc"""
        if self.length == 0:
            angle = self.start_angle
        else:
            # Calculate the angle at the given distance from start
            angle_ratio = distance_from_start / self.length
            angle = self.start_angle + angle_ratio * (self.end_angle - self.start_angle)
        
        x = self.center.x + self.radius * math.cos(angle)
        y = self.center.y + self.radius * math.sin(angle)
        return Point(x, y)
    
    def __repr__(self):
        return f"ArcSegment(center={self.center}, radius={self.radius}, angles=[{math.degrees(self.start_angle):.2f}°, {math.degrees(self.end_angle):.2f}°])"
    
    def get_points_for_plotting(self, num_points=100):
        """Generate points along the arc for plotting purposes"""
        points_x = []
        points_y = []
        
        angle_diff = self.end_angle - self.start_angle
        for i in range(num_points + 1):
            t = i / num_points
            angle = self.start_angle + t * angle_diff
            x = self.center.x + self.radius * math.cos(angle)
            y = self.center.y + self.radius * math.sin(angle)
            points_x.append(x)
            points_y.append(y)
        
        return points_x, points_y


class ConnectedPath:
    """Represents a path composed of connected line segments and arcs"""
    def __init__(self):
        self.segments = []
        self.segment_types = []
        self.cumulative_lengths = [0]
    
    def add_segment(self, segment: Union[LineSegment, ArcSegment], seg_type: SegmentType):
        """Add a segment to the path"""
        self.segments.append(segment)
        self.segment_types.append(seg_type)
        self.cumulative_lengths.append(self.cumulative_lengths[-1] + segment.length)
    
    def get_total_length(self) -> float:
        """Get the total length of the path"""
        return self.cumulative_lengths[-1] if self.cumulative_lengths else 0
    
    def get_segment_at_distance(self, distance: float) -> Tuple[int, float]:
        """Find which segment and position within that segment corresponds to the given distance"""
        if distance <= 0:
            return 0, 0
        
        # Find the segment that contains this distance
        for i, cum_len in enumerate(self.cumulative_lengths):
            if distance <= cum_len:
                # Calculate distance within the current segment
                segment_distance = distance - self.cumulative_lengths[i-1] if i > 0 else distance
                return i-1, segment_distance
        
        # If distance is beyond the path, return the last segment
        return len(self.segments)-1, self.segments[-1].length if self.segments else 0
    
    def get_point_at_distance(self, distance: float) -> Tuple[Point, SegmentType]:
        """Get the point and type at a specific distance along the path"""
        segment_idx, dist_in_segment = self.get_segment_at_distance(distance)
        if segment_idx < 0 or segment_idx >= len(self.segments):
            return None, None
        
        segment = self.segments[segment_idx]
        point = segment.get_point_at_distance(dist_in_segment)
        seg_type = self.segment_types[segment_idx]
        
        return point, seg_type
    
    def generate_random_points(self, num_points: int) -> List[Tuple[Point, SegmentType]]:
        """Generate random points along the path"""
        points_and_types = []
        total_length = self.get_total_length()
        
        for _ in range(num_points):
            random_distance = random.uniform(0, total_length)
            point, seg_type = self.get_point_at_distance(random_distance)
            points_and_types.append((point, seg_type))
        
        return points_and_types
    
    def plot_path_with_points(self, random_points: List[Tuple[Point, SegmentType]], save_path: str = None):
        """Plot the path with the random points colored by segment type"""
        if not MATPLOTLIB_AVAILABLE:
            print("Matplotlib is not available. Cannot create visualization.")
            return
        
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot each segment of the path
        for i, (segment, seg_type) in enumerate(zip(self.segments, self.segment_types)):
            if seg_type == SegmentType.STRAIGHT:
                # Plot straight segment
                x_vals, y_vals = segment.get_points_for_plotting()
                ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='Straight' if i == 0 else "")
            else:  # ARC
                # Plot arc segment
                x_vals, y_vals = segment.get_points_for_plotting()
                ax.plot(x_vals, y_vals, 'g-', linewidth=2, label='Arc' if i == 0 else "")
        
        # Separate points by type for different colors
        straight_points_x = []
        straight_points_y = []
        arc_points_x = []
        arc_points_y = []
        
        for point, seg_type in random_points:
            if seg_type == SegmentType.STRAIGHT:
                straight_points_x.append(point.x)
                straight_points_y.append(point.y)
            else:
                arc_points_x.append(point.x)
                arc_points_y.append(point.y)
        
        # Plot the random points
        if straight_points_x:
            ax.scatter(straight_points_x, straight_points_y, c='red', s=50, zorder=5, label='Points on Straight', edgecolors='black')
        if arc_points_x:
            ax.scatter(arc_points_x, arc_points_y, c='orange', s=50, zorder=5, label='Points on Arc', edgecolors='black')
        
        ax.set_title('Path with Random Points Classification')
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend()
        ax.axis('equal')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        else:
            plt.show()


def main():
    """Main function demonstrating the functionality"""
    print("Creating a path with straight segments and arcs...")
    
    # Create a path with alternating straight segments and arcs
    path = ConnectedPath()
    
    # Add a straight segment from (0, 0) to (5, 0)
    path.add_segment(LineSegment(Point(0, 0), Point(5, 0)), SegmentType.STRAIGHT)
    
    # Add an arc segment (quarter circle) centered at (7, 0) with radius 2
    path.add_segment(ArcSegment(Point(7, 0), 2, -math.pi/2, math.pi/2), SegmentType.ARC)
    
    # Add another straight segment from the end of the arc to (9, 4)
    path.add_segment(LineSegment(Point(7, 2), Point(9, 4)), SegmentType.STRAIGHT)
    
    # Add another arc segment (quarter circle) centered at (7, 4) with radius 2
    path.add_segment(ArcSegment(Point(7, 4), 2, math.pi/2, 3*math.pi/2), SegmentType.ARC)
    
    # Add a final straight segment
    path.add_segment(LineSegment(Point(7, 2), Point(12, 2)), SegmentType.STRAIGHT)
    
    print(f"Total path length: {path.get_total_length():.2f}")
    print(f"Number of segments: {len(path.segments)}")
    
    # Generate random points along the path
    num_random_points = 8
    random_points = path.generate_random_points(num_random_points)
    
    print(f"\nGenerated {num_random_points} random points:")
    print("Original Distance | Point Location          | Type")
    print("-" * 55)
    
    # Calculate the original distances used to generate these points
    total_length = path.get_total_length()
    original_distances = []
    for _ in random_points:
        original_distances.append(random.uniform(0, total_length))
    
    for orig_dist, (point, seg_type) in zip(original_distances, random_points):
        print(f"{orig_dist:13.2f} | {point!s:20} | {seg_type.value}")
    
    # Count how many points belong to each type
    straight_count = sum(1 for _, seg_type in random_points if seg_type == SegmentType.STRAIGHT)
    arc_count = sum(1 for _, seg_type in random_points if seg_type == SegmentType.ARC)
    
    print(f"\nSummary:")
    print(f"Points on straight segments: {straight_count}")
    print(f"Points on arcs: {arc_count}")
    print(f"Total points: {len(random_points)}")
    
    # Visualize the path and points
    print("\nGenerating visualization...")
    path.plot_path_with_points(random_points)


if __name__ == "__main__":
    main()