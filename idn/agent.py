import argparse
import socket
import threading

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--bind-address', type=str, default="0.0.0.0")
parser.add_argument('--bind-port', type=int, default=10914)
parser.add_argument('--rendezvous', type=str, default="idn/rendezvous.txt")
parser.add_argument('--id-key', type=str, default="idn/key.pem")
parser.add_argument('--id-crt', type=str, default="idn/crt.pem")

NUM_WORKERS = 10

"""
Peer
"""
class Peer():
    received_data = ""

    """
    Constructor
    """
    def __init__(self, sock, ipaddr, port):
        self.sock = sock
        self.ipaddr = ipaddr
        self.port = port

    """
    Receive and parse data
    """
    def recv(self):
        # Receive data
        data = self.sock.recv(4096)
        if len(data) == 0:
            return False
        # Parse the data

    """
    Join
    """
    def join(self):
        pass

    """
    Connect
    """
    def connect(self):
        pass

"""
Thread
"""
class PeerThread(threading.Thread):
    """
    Constructor
    """
    def __init__(self, peer):
        threading.Thread.__init__(self)
        self.peer = peer
        self.running = True

    """
    Run this thread
    """
    def run(self):
        while self.running:
            # Receive data
            if not self.peer.recv():
                self.running = False

"""
Peer manager
"""
class PeerManager():
    threads = {}
    """
    Constructor
    """
    def __init__(self):
        pass

    """
    Add a new peer
    """
    def add_new_peer(self, peer):
        th = PeerThread(peer)
        self.threads[th.ident] = th
        th.start()

    """
    Clean threads
    """
    def clean_threads(self):
        # Join dead threads
        for th in threading.enumerate():
            if th == threading.main_thread():
                continue
            if not th.is_alive():
                del self.threads[th.ident]
                th.join()

"""
Main routine
"""
def main(args):
    # Open a rendezvous-point file
    with open(args.rendezvous, 'r') as f:
        peers = []
        for ln in f:
            ln = ln.strip()
            ipaddr, port = ln.split()
            peers.append((ipaddr, port))

    # Prepare a PeerManager
    pm = PeerManager()

    # Establish connections to all peers
    for p in peers:
        try:
            # Establish a connection to a peer
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((p[0], int(p[1])))
            # Start a peer thread
            peer = Peer((p[0], int(p[1])))
            pm.add_new_peer(peer)
        except:
            # In case of encountering an error
            pass

    # Open a socket and listen connections on it
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.bind_address, args.bind_port))
    sock.listen(NUM_WORKERS)
    while True:
        # Accept a client and start a thread
        csock, caddr = sock.accept()
        peer = Peer(csock, caddr[0], caddr[1])
        pm.add_new_peer(peer)
        # Clean dead threads
        pm.clean_threads()
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
