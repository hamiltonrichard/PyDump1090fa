"""Main application"""
import time
from py1090dumpfa_lib import Py1090Dumpfa
if __name__ == "__main__":
    try:
        # Initialize a class instance
        flightdata = Py1090Dumpfa()

        # Insert Your Code Here 

    except RuntimeError as e:
        print(f"Error: {e}")
