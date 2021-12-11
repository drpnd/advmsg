import argparse
import socket
import threading

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bind-address', type=str, default="0.0.0.0")
parser.add_argument('--bind-port', type=int, default=10914)

NUM_WORKERS = 10

"""
Thread
"""
class ClientThread(threading.Thread):
    """
    Constructor
    """
    def __init__(self, csock):
        threading.Thread.__init__(self)
        self.csock = csock
        self.running = True

    """
    Run this thread
    """
    def run(self):
        while self.running:
            data = self.csock.recv(4096)
            self.csock.send(data)
            if len(data) == 0:
                self.running = False

"""
Main routine
"""
def main(args):
    # Open a socket and listen connections on it
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.bind_address, args.bind_port))
    sock.listen(NUM_WORKERS)
    while True:
        # Accept a client and start a thread
        csock, caddr = sock.accept()
        th = ClientThread(csock)
        th.start()

        # Join dead threads
        for th in threading.enumerate():
            if th == threading.main_thread():
                continue
            if not th.is_alive():
                th.join()
    # Close the socket
    sock.close()

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
