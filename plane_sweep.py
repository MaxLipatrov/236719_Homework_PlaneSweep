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

from enum import IntEnum
from typing import Optional
import numpy as np
from avl_tree import AVLTree


class PointEventType(IntEnum):
    """ Represents event type for point.
     To be used in plane sweep algorithm """
    UNDEFINED = 0
    START = 1
    INTERSECTION = 2
    END = 3


class Point:
    """ Represents a point on a plane.
    When is not start/end point of a segment or intersection point its type is UNDEFINED and segment is None.
    When point is intersection point, its second_segment is not None
    """

    def __init__(self, x: float, y: float,
                 event_type: PointEventType = PointEventType.UNDEFINED,
                 segment=None, second_segment=None):
        self.x = x
        self.y = y
        self.event_type = event_type
        self.segment = segment
        self.second_segment = second_segment

    def __str__(self):
        return str('Point: x = ' + str(self.x) + ', y = ' + str(self.y) + ', type: ' + str(self.event_type)) + '\n'

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

    def __lt__(self, other):
        self_x = self.value_at_x(Segment.x_coordinate_comparator)
        other_x = other.value_at_x(Segment.x_coordinate_comparator)
        return self_x < other_x

    def __gt__(self, other):
        self_x = self.value_at_x(Segment.x_coordinate_comparator)
        other_x = other.value_at_x(Segment.x_coordinate_comparator)
        return self_x > other_x

    def __str__(self):
        return 'Segment: its start and end are:\n' + str(self.start) + str(self.end)

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


class EventQueue:
    """ Implemented as AVLTree instead of MinHeap. """

    def __init__(self):
        self.tree = AVLTree()
        self.size = 0

    def insert_event(self, event: Point) -> bool:
        res = self.tree.insert(event)
        if res:
            self.size += 1
        return res

    def get_nearest_event(self) -> Optional[Point]:
        return self.tree.min()

    def remove_event(self, event: Point) -> bool:
        res = self.tree.delete(event)
        if res:
            self.size -= 1
        return res


class SweepLineStatus:
    """ Implemented with AVLTree. """

    def __init__(self):
        self.tree = AVLTree()
        self.size = 0

    def add_segment(self, segment: Segment) -> bool:
        res = self.tree.insert(segment)
        if res:
            self.size += 1
        return res

    def remove_segment(self, segment: Segment) -> bool:
        res = self.tree.delete(segment)
        if res:
            self.size -= 1
        return res

    def get_above_neighbor(self, segment: Segment) -> Optional[Segment]:
        current = self.tree.find(segment)
        assert (current is not None)
        above = self.tree.successor(current)
        if above is not None:
            return above.key
        return None

    def get_below_neighbor(self, segment: Segment) -> Optional[Segment]:
        current = self.tree.find(segment)
        assert (current is not None)
        below = self.tree.predecessor(current)
        if below is not None:
            return below.key
        return below

    def intersection_with_upper(self, segment: Segment) -> Optional[Point]:
        current = self.tree.find(segment)
        assert (current is not None)
        # Successor, because upper's y coordinate is bigger
        upper = self.tree.successor(current)
        if upper is None:
            return None
        else:
            point = calculate_intersection_point(upper.key, segment)
            if point is None:
                return None
            return point

    def intersection_with_lower(self, segment: Segment) -> Optional[Point]:
        current = self.tree.find(segment)
        assert (current is not None)
        lower = self.tree.predecessor(current)
        if lower is None:
            return None
        else:
            point = calculate_intersection_point(lower.key, segment)
            if point is None:
                return None
            return point

    def reach_intersection_of(self, upper: Segment, lower: Segment):
        upper_node = self.tree.find(upper)
        lower_node = self.tree.find(lower)

        temp_key = upper_node.key
        upper_node.key = lower_node.key
        lower_node.key = temp_key


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
    if first.start.y < second.start.y:
        p1 = first.start
        p2 = first.end
        p3 = second.end
        p4 = second.start
    else:
        p1 = second.start
        p2 = second.end
        p3 = first.end
        p4 = first.start

    # Verify that p1,p2 are on different sides of second
    if calculate_triangle_area(p1, p3, p4) >= 0 and calculate_triangle_area(p2, p4, p3) >= 0:
        # Verify that p3,p4 are on different sides of first
        if calculate_triangle_area(p2, p1, p3) >= 0 and calculate_triangle_area(p2, p4, p1) >= 0:
            # Segments are definitely intersecting, now need to find their intersection point
            k_first = first.slope()
            k_second = second.slope()

            b_first = first.interceptor()
            b_second = second.interceptor()

            if k_first == k_second:
                # If same slope, they collinear, and hence cannot intersect
                return None
            x_intersection = (b_second - b_first) / (k_first - k_second)
            y_intersection = k_first * x_intersection + b_first

            return Point(x_intersection, y_intersection, PointEventType.INTERSECTION, first, second)
    return None


def plane_sweep(segments: set) -> int:
    """ Actual implementation of algorithm.
    Set of segments as input, number of intersections between them as output. """

    # At first, events are start/end points only and sweep-line status is empty
    events = EventQueue()
    sweep_line_status = SweepLineStatus()

    for segment in segments:
        events.insert_event(segment.start)
        events.insert_event(segment.end)

    # A value to return
    intersections_num = 0

    while events.size > 0:
        current_event_point = events.get_nearest_event()
        current_event_type = current_event_point.event_type

        assert (current_event_type != PointEventType.UNDEFINED)

        Segment.x_coordinate_comparator = current_event_point.x

        if current_event_type == PointEventType.START:
            segment = current_event_point.segment
            sweep_line_status.add_segment(segment)

            upper_intersection = sweep_line_status.intersection_with_upper(segment)
            if upper_intersection and upper_intersection.x >= current_event_point.x:
                events.insert_event(upper_intersection)

            lower_intersection = sweep_line_status.intersection_with_lower(segment)
            if lower_intersection and lower_intersection.x >= current_event_point.x:
                events.insert_event(lower_intersection)

        elif current_event_type == PointEventType.END:
            segment = current_event_point.segment
            predecessor = sweep_line_status.get_above_neighbor(segment)
            successor = sweep_line_status.get_below_neighbor(segment)
            sweep_line_status.remove_segment(segment)

            if predecessor and successor:
                point = calculate_intersection_point(predecessor, successor)
                if point and point.x >= current_event_point.x:
                    events.insert_event(point)

        elif current_event_type == PointEventType.INTERSECTION:
            intersections_num += 1

            first = current_event_point.segment
            second = current_event_point.second_segment

            # Determine who is new upper and who is lower
            if first.slope() > second.slope():
                new_upper = first
                new_lower = second
            else:
                new_upper = second
                new_lower = first

            Segment.x_coordinate_comparator -= 0.01

            # Segments are still not swapped in status!
            upper_to_check = sweep_line_status.get_above_neighbor(new_lower)
            lower_to_check = sweep_line_status.get_below_neighbor(new_upper)

            if upper_to_check:
                upper_intersection = calculate_intersection_point(upper_to_check, new_upper)
                if upper_intersection and upper_intersection.x >= current_event_point.x:
                    events.insert_event(upper_intersection)

            if lower_to_check:
                lower_intersection = calculate_intersection_point(lower_to_check, new_lower)
                if lower_intersection and lower_intersection.x >= current_event_point.x:
                    events.insert_event(lower_intersection)

            sweep_line_status.reach_intersection_of(first, second)

        events.remove_event(current_event_point)

    return intersections_num
