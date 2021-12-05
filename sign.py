import argparse
import OpenSSL
import secrets
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--private-key', type=str, default="ca/cakey.pem")
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")
parser.add_argument('--csr', type=str, default='csr.pem')

VALID_NOT_BEFORE = 0
VALID_NOT_AFTER = 3600 * 24 * 356 * 3 # 3 years

"""
Sign a CSR by the CA certificate
"""
def sign(req, cacert, key, serial):
    # Create a self-signed certificate
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(serial)
    cert.gmtime_adj_notBefore(VALID_NOT_BEFORE)
    cert.gmtime_adj_notAfter(VALID_NOT_AFTER)
    cert.set_issuer(cacert.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, 'sha256')
    return cert

"""
Main routine
"""
def main(args):
    # Load th CSR
    with open(args.csr, 'rb') as f:
        req_pem = f.read()
        f.close()

    # Load the CA private key
    with open(args.private_key, 'rb') as f:
        key_pem = f.read()
        f.close()

    # Load the CA certificate
    with open(args.cacert, 'rb') as f:
        cacert_pem = f.read()
        f.close()

    # PEMs to OpenSSL crypto instances
    key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_pem)
    cacert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cacert_pem)
    req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req_pem)

    # Sign the CSR by the CA certificate
    cert = sign(req, cacert, key, 2)

    # Dump the signed certificate as a PEM file
    cert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    print(cert_pem.decode('utf-8'))

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
