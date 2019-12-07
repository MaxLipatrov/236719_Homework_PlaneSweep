from plane_sweep import *


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

    p3 = Point(0, 1)
    p4 = Point(2, -1)

    s1 = Segment(p1, p2)
    s2 = Segment(p3, p4)

    print(calculate_intersection_point(s1, s2))
    s = set()
    s.add(s1)
    s.add(s2)
    plane_sweep(s)


if __name__ == "__main__":
    main()
