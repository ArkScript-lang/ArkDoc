#!/usr/bin/env python3

import sys
import argparse


EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def main() -> int:
    parser = argparse.ArgumentParser(description='ArkScript Documentation generator')

    args = parser.parse_args()
    print(args)

    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())