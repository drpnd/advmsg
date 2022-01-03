import argparse
import OpenSSL
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")
parser.add_argument('--crt', type=str, default="crt.pem")
parser.add_argument('--key', type=str, default="key.pem")

"""
Verify a certificate with the specified CA certificate
"""
def verify_certificate(cert, cacert):
    # Verify the certificate with the CA certificate
    try:
        store = OpenSSL.crypto.X509Store()
        store.add_cert(cacert)
        store_ctx = OpenSSL.crypto.X509StoreContext(store, cert)
        store_ctx.verify_certificate()
        return True
    except Exception as e:
        return False

"""
Verify a signature
"""
def verify_signature(cert, e, m, d='sha256'):
    try:
        OpenSSL.crypto.verify(cert, e, m, d)
        return True
    except OpenSSL.crypto.Error as e:
        return False

"""
Generate a signature for a message with a key and a specified hash function
"""
def generate_signature(key, m, d):
    return OpenSSL.crypto.sign(key, m, d)

"""
Main routine
"""
def main(args):
    # Load the CA certificate
    with open(args.cacert, 'rb') as f:
        cacert_pem = f.read()
        f.close()
    cacert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cacert_pem)

    # Load the certificate
    with open(args.crt, 'rb') as f:
        cert_pem = f.read()
        f.close()
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_pem)

    # Load the private key
    with open(args.key, 'rb') as f:
        key_pem = f.read()
        f.close()
    key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_pem)

    m = b'test'
    d = 'sha256'
    e = generate_signature(key, m, d)
    print(verify_signature(cert, e, m, d))
    pubkey = cert.get_pubkey()

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
