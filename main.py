"""
Created by Maxim Lipatrov at 7-12-2019
maxim-li@campus.technion.ac.il

PlaneSweep algorithm runner.
Give a test file as a parameter,
e.g. if your test file is "test.txt",
run it as:

python3 main.py test.txt

"""

from plane_sweep import *
import sys


def parse_input(input_file_name: str) -> list:
    with open(input_file_name, 'r') as in_file:
        num_test_cases = int(in_file.readline())
        test_cases = []
        for i in range(num_test_cases):
            num_segments = int(in_file.readline())
            current_case = set()
            for j in range(num_segments):
                coordinates = in_file.readline().split(" ")
                assert (len(coordinates) == 4)
                first_point = Point(float(coordinates[0]), float(coordinates[1]))
                second_point = Point(float(coordinates[2]), float(coordinates[3]))
                segment = Segment(first_point, second_point)
                current_case.add(segment)
            test_cases.append(current_case)
        # Sanity check
        assert (num_test_cases == len(test_cases))
        last = in_file.readline()
        assert (int(last) == -1)
    return test_cases


def main():
    if len(sys.argv) < 2:
        print("Not enough input parameters. Provide a input test file as parameter.")
        exit(1)
    elif len(sys.argv) > 2:
        print("Too much input parameters. Provide only one test file as parameter.")
        exit(1)
    test_cases = parse_input(sys.argv[1])
    for case in test_cases:
        print(plane_sweep(case))


if __name__ == "__main__":
    main()
