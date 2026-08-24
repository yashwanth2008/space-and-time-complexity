import sys
from analyzer import analyze_file


if len(sys.argv) != 2:
    print("Usage: python main.py <cpp_file>")
    sys.exit(1)

filename = sys.argv[1]

analyze_file(filename)