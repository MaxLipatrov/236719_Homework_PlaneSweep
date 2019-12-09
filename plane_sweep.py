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
from avl_tree import AVLTree


class PointEventType(Enum):
    """ Represents event type for point.
     To be used in plane sweep algorithm """
    UNDEFINED = 0
    START = 1
    INTERSECTION = 2
    END = 3


class Point:
    """ Represents a point on a plane.
     When is not start/end point of a segment or intersection point its type is UNDEFINED and segment is None. """

    def __init__(self, x: float, y: float, event_type: PointEventType = PointEventType.UNDEFINED, segment=None):
        self.x = x
        self.y = y
        self.event_type = event_type
        self.segment = segment

    def __str__(self):
        return str('Point: x = ' + str(self.x) + ', y = ' + str(self.y) + ', type: ' + str(self.event_type))

    """ Operators of smaller / greater compare by x coordinate, and then by y coordinate, and then by event type. """

    def __lt__(self, other):
        """ Overloads comparison operator """
        if self.x == other.x:
            if self.y == other.y:
                return self.event_type < other.event_type
            else:
                return self.y < other.y
        else:
            return self.x < other.x

    def __gt__(self, other):
        """ Overloads comparison operator """
        if self.x == other.x:
            if self.y == other.y:
                return self.event_type > other.event_type
            else:
                return self.y > other.y
        else:
            return self.x > other.x


class Segment:
    """
    Represents a non-vertical line segment on a plane,
    start is the leftmost point, end is the rightmost (by x coordinate),
    event_type is a type needed for plane sweep algorithm.
    """

    """ In order to compare segments corresponding to some x coordinate """
    x_coordinate_comparator: float

    def __init__(self, p1: Point, p2: Point):
        if p1.x <= p2.x:
            self.start = p1
            self.end = p2
        else:
            self.start = p2
            self.end = p1
        self.start.event_type = PointEventType.START
        self.end.event_type = PointEventType.END
        self.start.segment = self
        self.end.segment = self

    def slope(self):
        """ Represents a slope, e.g. k of line y = kx + b which this segment belongs to  """
        return (self.end.y - self.start.y) / (self.end.x - self.start.x)

    def interceptor(self):
        """ Represents a y coefficient at x = 0, e.g. the b, of line y = kx + b which this segment belongs to  """
        return self.end.y - self.end.x * self.slope()

    def value_at_x(self, x):
        """ Return y value of line y = kx + b at given x.
        If given x is not in corresponding to segment, returns None. """
        if x < self.start.x or x > self.end.x:
            return None
        else:
            return self.slope() * x + self.interceptor()

    def __lt__(self, other):
        return self.value_at_x(Segment.x_coordinate_comparator) < other.value_at_x(Segment.x_coordinate_comparator)

    def __gt__(self, other):
        return self.value_at_x(Segment.x_coordinate_comparator) > other.value_at_x(Segment.x_coordinate_comparator)


class EventQueue:
    """ Implemented as AVLTree. """

    def __init__(self):
        self.tree = AVLTree()
        self.size = 0

    def insert_event(self, point: Point):
        self.tree.insert(point)
        self.size += 1

    def get_nearest_event(self):
        return self.tree.min()

    def remove_nearest_event(self):
        leftmost_point = self.tree.min()
        if leftmost_point is not None:
            self.tree.delete(leftmost_point)
            self.size -= 1


class SweepLineStatus:
    def __init__(self):
        self.tree = AVLTree()
        self.size = 0

    def insert(self, item):
        self.tree.insert(item)
        self.size += 1

    def predecessor(self, item):
        self.tree.predecessor(item)


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
    events = EventQueue()
    sweep_line_status = []

    for segment in segments:
        start_tup = (segment.start, segment)
        end_tup = (segment.end, segment)

        events.insert_event(start_tup)
        events.insert_event(end_tup)

    # A value to return
    intersections_num = 0

    # Maintain counter to avoid checking length every time
    events_size = len(events)
    #
    # for e in events:
    #     print(e)
    # while events_size > 0:
    #     current_event_tuple = events[0]
    #     current_event_type = current_event_tuple[0].event_type
    #
