from plane_sweep import *
from avl_tree import AVLTree


def main():
    """ Elementary testing the plane-sweep """
    # p1 = Point(0, 0)
    # p2 = Point(2, 0)
    # p3 = Point(2, 5)
    # area = calculate_triangle_area(p1, p2, p3)
    # print(area)
    #
    # s = Segment(p1, p3)
    # print(s.slope())
    # print(s.interceptor())
    p1 = Point(0, 0)
    p2 = Point(5, 0)

    p3 = Point(1, 1)
    p4 = Point(4, -1)

    s1 = Segment(p1, p2)
    s2 = Segment(p3, p4)

    print(p1.segment)
    # Segment.x_coordinate_comparator = 1
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 2
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 3
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 4
    # print(s1 < s2)

    # print(calculate_intersection_point(s1, s2))
    # s = set()
    # s.add(s1)
    # s.add(s2)
    # plane_sweep(s)

    # q = EventQueue()
    # q.insert(p1)
    # q.insert(p2)
    # q.insert(p3)
    # q.insert(p4)
    #
    # print(q.min())
    # q.remove_min()
    #
    # q.remove_min()
    # print(q.min())
    #
    # q.remove_min()
    # print(q.min())
    #
    # q.remove_min()
    # print(q.min())
    #
    # t = AVLTree()
    # print('Min: ' + str(t.min()))
    #
    # t.insert(p4)
    # print('Min: ' + str(t.min()))
    #
    # t.insert(p3)
    # print('Min: ' + str(t.min()))
    #
    # t.insert(p1)
    # print('Min: ' + str(t.min()))
    #
    # t.insert(p2)
    # print('Min: ' + str(t.min()))


if __name__ == "__main__":
    main()
