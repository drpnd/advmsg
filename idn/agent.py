import argparse
import socket

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bind-address', type=str, default="0.0.0.0")
parser.add_argument('--bind-port', type=int, default=10914)

"""
Main routine
"""
def main(args):

    # Open a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((args.bind_address, args.bind_port))
    sock.listen(10)
    while True:
        client, caddr = sock.accept()
        print(client, caddr)
        pass
    sock.close()

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
