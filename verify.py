import argparse
import OpenSSL
import secrets
import sqlite3
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")

"""
Main routine
"""
def main(args):
    # Load th CA certificate
    with open(args.cacert, 'rb') as f:
        cacert_pem = f.read()
        f.close()
    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
