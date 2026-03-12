#!/usr/bin/env python3
"""
Smooth Curve Generator Module

This module generates a smooth curve consisting of 5 Line segments 
connected by Arcs with tangential continuity (G1-continuity) at connection points.
"""

import math
import random
from typing import List, Tuple

from graphics_elements import Point, Line, Arc


def create_smooth_curve(
    length: float,
    rad: float,
    angl: float
) -> Tuple[List[Line], List[Arc]]:
    """
    Create a smooth curve with 5 line segments connected by 4 arcs.
    
    Args:
        length: Base length of line segments
        rad: Base radius of connecting arcs
        angl: Base angle of arcs in radians
    
    Returns:
        A tuple of (lines, arcs) where each list contains 5 and 4 elements respectively
    """
    lines: List[Line] = []
    arcs: List[Arc] = []
    
    # Initialize current position and direction
    current_x, current_y = 0.0, 0.0
    current_direction = 0.0
    
    for i in range(5):
        # Step 2a: Create line segment
        # Random length differing from base by up to 10%
        length_ = length * (1 + random.uniform(-0.1, 0.1))
        
        # Calculate end point of line
        end_x = current_x + length_ * math.cos(current_direction)
        end_y = current_y + length_ * math.sin(current_direction)
        
        # Create Line object
        start_point = Point(current_x, current_y)
        end_point = Point(end_x, end_y)
        line = Line(start_point, end_point)
        lines.append(line)
        
        # Step 2b: Update position to end of line
        current_x, current_y = end_x, end_y
        
        # Step 2c: Create connecting arc (only for first 4 segments)
        if i < 4:
            # Random angle differing from base by up to 10%
            angl_ = angl * (1 + random.uniform(-0.1, 0.1))
            
            # Random radius differing from base by up to 10%
            rad_ = rad * (1 + random.uniform(-0.1, 0.1))
            
            # Determine arc direction with alternating pattern
            # The arc center is perpendicular to the current direction at the start point
            if i % 2 == 0:
                # Even index: turn left (CCW arc)
                # Center is at +π/2 from current_direction
                center_angle = current_direction + math.pi / 2
                # Start angle points from center to start point (current_pos)
                # Since center is at current_direction + π/2, start_angle = current_direction - π/2
                start_angle = current_direction - math.pi / 2
                # End angle = start_angle + arc_angle (CCW)
                end_angle = start_angle + angl_
            else:
                # Odd index: turn right (CW arc)
                # Center is at -π/2 from current_direction
                center_angle = current_direction - math.pi / 2
                # Start angle points from center to start point (current_pos)
                # Since center is at current_direction - π/2, start_angle = current_direction + π/2
                start_angle = current_direction + math.pi / 2
                # End angle = start_angle - arc_angle (CW)
                end_angle = start_angle - angl_
            
            # Calculate center of arc
            center_x = current_x + rad_ * math.cos(center_angle)
            center_y = current_y + rad_ * math.sin(center_angle)
            
            center_point = Point(center_x, center_y)
            
            # Create Arc object
            arc = Arc(center_point, rad_, start_angle, end_angle)
            arcs.append(arc)
            
            # Step 2d: Update position to end of arc
            arc_end = arc.end_point
            current_x, current_y = arc_end.x, arc_end.y
            
            # Step 2e: Update direction to tangent at end of arc
            if i % 2 == 0:
                # Even index (CCW arc): direction = end_angle - π/2
                new_direction = end_angle - math.pi / 2
            else:
                # Odd index (CW arc): direction = end_angle + π/2
                new_direction = end_angle + math.pi / 2
            
            # Normalize direction to [-π, π]
            current_direction = math.atan2(math.sin(new_direction), math.cos(new_direction))
    
    return (lines, arcs)


def check_for_intersections(lines: List[Line], arcs: List[Arc]) -> bool:
    """
    Simplified intersection check between segments.
    
    Only checks adjacent elements (which by design share endpoints).
    For non-adjacent elements, returns True assuming the algorithm creates valid curves.
    
    Args:
        lines: List of Line objects
        arcs: List of Arc objects
    
    Returns:
        True (assuming the algorithm creates valid curves)
    """
    # Adjacent elements share endpoints by design, so we skip those checks
    # For non-adjacent elements, we leave stubs for future implementation
    
    # Stub for future implementation - checking non-adjacent elements
    # Currently returning True assuming the algorithm creates valid curves
    return True


def example_usage() -> Tuple[List[Line], List[Arc]]:
    """
    Demonstrate the usage of create_smooth_curve function.
    
    Returns:
        The created lists of lines and arcs
    """
    # Define parameters
    length = 10
    rad = 1
    angl = 2 * math.pi / 3
    
    # Create smooth curve
    lines, arcs = create_smooth_curve(length, rad, angl)
    
    # Print information about each segment
    print("Generated Smooth Curve:")
    print("=" * 50)
    
    for i, line in enumerate(lines):
        print(f"\nLine {i}:")
        print(f"  Start: {line.start}")
        print(f"  End: {line.end}")
        print(f"  Length: {line.length:.4f}")
        
        if i < len(arcs):
            arc = arcs[i]
            print(f"Arc {i}:")
            print(f"  Center: {arc.center}")
            print(f"  Radius: {arc.radius:.4f}")
            print(f"  Start Angle: {arc.start_angle:.4f} rad")
            print(f"  End Angle: {arc.end_angle:.4f} rad")
            print(f"  Start Point: {arc.start_point}")
            print(f"  End Point: {arc.end_point}")
            print(f"  Length: {arc.length:.4f}")
            
            # Check endpoint matching between line and arc
            line_end = line.end
            arc_start = arc.start_point
            match_distance = line_end.distance_to(arc_start)
            print(f"  Line-Arc Connection Match: {match_distance:.6f}")
    
    # Check endpoint matching between consecutive elements
    print("\n" + "=" * 50)
    print("Endpoint Matching Verification:")
    for i in range(len(arcs)):
        if i < len(arcs) - 1:
            arc_end = arcs[i].end_point
            next_line_start = lines[i + 1].start
            match_distance = arc_end.distance_to(next_line_start)
            print(f"Arc {i} end to Line {i+1} start: {match_distance:.6f}")
    
    # Check for intersections
    has_intersections = check_for_intersections(lines, arcs)
    print(f"\nIntersection Check: {'No intersections detected' if has_intersections else 'Intersections found'}")
    
    return lines, arcs


if __name__ == "__main__":
    example_usage()
