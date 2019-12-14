from plane_sweep import *
from avl_tree import AVLTree


def main():
    """ Elementary testing the plane-sweep """

    # p1 = Point(0, 0)
    # p2 = Point(5, 0)
    #
    # p3 = Point(1, 1)
    # p4 = Point(4, -1)
    #
    # s1 = Segment(p1, p2)
    # s2 = Segment(p3, p4)
    #
    # print(p1.segment)
    # Segment.x_coordinate_comparator = 1
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 2
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 3
    # print(s1 < s2)
    # Segment.x_coordinate_comparator = 4
    # print(s1 < s2)


    test_cases = parse_input("test.txt")
    # print(test_cases)
    print(plane_sweep(test_cases[0]))
    print(plane_sweep(test_cases[1]))
    print(plane_sweep(test_cases[2]))
    print(plane_sweep(test_cases[3]))


if __name__ == "__main__":
    main()
