#!/usr/bin/env python3

from robot import Robot
import time


def main():
    r = Robot()
    try:
        pass
    finally:
        print("RESET")
        r.reset()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
