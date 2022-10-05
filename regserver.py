"""
Authors: George Toumbas, Shanzay Waseem
"""
import sys

def main():
    """
    Reads arguments from the command line and opens the GUI or the help message
    """
    if len(sys.argv) != 3:
        print("Usage: python %s host port file’ % sys.argv[0]")
        sys.exit(2)