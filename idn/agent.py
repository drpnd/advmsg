import argparse

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=10914)

"""
Main routine
"""
def main(args):
    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
