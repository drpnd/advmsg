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
    def __init__(self, csock):
        threading.Thread.__init__(self)
        self.csock = csock
        self.running = True

    def run(self):
        while self.running:
            data = self.csock.recv(4096)
            print(data)
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
    threads = []
    main_thread = threading.current_thread()
    while True:
        # Accept a client
        csock, caddr = sock.accept()
        print(csock, caddr)
        th = ClientThread(csock)
        th.start()
        threads.append(th)

        for th in threading.enumerate():
            if th == threading.main_thread():
                continue
            if not th.is_alive():
                th.join()
            print(th, th.is_alive())
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
