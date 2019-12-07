"""
Created by Maxim Lipatrov at 7-12-2019
maxim-li@campus.technion.ac.il

Plane sweep algorithm implementation

Given assumptions:
The input file contains at most 25,000 sets of segments.
• Each set of segments contains at most 1,000 segments.
• Spacing in the input file is insignificant.
• There are no vertical segments.
• No two segments intersect in more than one point.
• No three segments intersect in one point.
• No numerical errors occur when using C’s double-precision floating point numbers.
That is, segment endpoints are well separated, as well as intersections of segments,
and events of the algorithm are separated enough along the x direction.
• You may not assume that the first endpoint of a segment lies to the left of the second
endpoint, but need to check and handle both cases.
"""
from enum import Enum
from typing import Optional
import numpy as np


class PointEventType(Enum):
    """ Represents event type for point.
     To be used in plane sweep algorithm """
    UNDEFINED = 'Undefined'
    START = 'Start'
    END = 'End'
    INTERSECTION = 'Intersection'


class Point:
    """ Represents a point on a plane.
     When is not start/end point of a segment or intersection point its type is UNDEFINED """
    x: float
    y: float
    event_type: PointEventType

    def __init__(self, x: float, y: float, event_type: PointEventType = PointEventType.UNDEFINED):
        self.x = x
        self.y = y
        self.event_type = event_type

    def __str__(self):
        return str('Point: x = ' + str(self.x) + ', y = ' + str(self.y) + ', type: ' + str(self.event_type))


class Segment:
    """
    Represents a non-vertical line segment on a plane.
    Start is the leftmost point, end is the rightmost (by x coordinate).
    """
    start: Point
    end: Point

    def __init__(self, p1: Point, p2: Point):
        if p1.x <= p2.x:
            self.start = p1
            self.start.event_type = PointEventType.START
            self.end = p2
            self.end.event_type = PointEventType.END
        else:
            self.start = p2
            self.start.event_type = PointEventType.START
            self.end = p1
            self.end.event_type = PointEventType.END

    def slope(self):
        """ Represents a slope, e.g. k of line y = kx + b which this segment belongs to  """
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def interceptor(self):
        """ Represents a y coefficient at x = 0, of line y = kx + b which this segment belongs to  """
        return self.end.y - self.end.x * self.slope()


def calculate_triangle_area(p1: Point, p2: Point, p3: Point) -> float:
    """ Calculate triangle area, based on determinant. Sign of result is point orientation, as meant in lecture. """
    matrix = np.array([
        [p1.x, p1.y, 1],
        [p2.x, p2.y, 1],
        [p3.x, p3.y, 1]
    ])
    # print(0.5 * np.linalg.det(matrix))
    return 0.5 * np.linalg.det(matrix)


def calculate_intersection_point(first: Segment, second: Segment) -> Optional[Point]:
    # Exactly like in lecture
    p1 = first.start
    p2 = first.end
    p3 = second.end
    p4 = second.start

    # Verify that p1,p2 are on different sides of second
    if calculate_triangle_area(p1, p3, p4) >= 0 and calculate_triangle_area(p2, p4, p3) >= 0:
        # Verify that p3,p4 are on different sides of first
        if calculate_triangle_area(p2, p1, p3) >= 0 and calculate_triangle_area(p2, p4, p1) >= 0:
            # Segments are definitely intersecting, now need to find their intersection point
            k_first = first.slope()
            k_second = second.slope()

            b_first = first.interceptor()
            b_second = second.interceptor()

            x_intersection = (b_second - b_first) / (k_first - k_second)
            y_intersection = k_first * x_intersection + b_first

            return Point(x_intersection, y_intersection, PointEventType.INTERSECTION)
    return None


def plane_sweep(segments: set) -> int:
    """ Actual implementation of algorithm.
    Set of segments as input, number of intersections between them as output. """

    # At first, events are start/end points only and sweep-line status is empty
    events = []
    sweep_line_status = []

    for segment in segments:
        events.append(segment.start)
        events.append(segment.end)

    # Sort events by their x coordinate
    events.sort(key=lambda point: point.x)

    for e in events:
        print(e)

    return 0

