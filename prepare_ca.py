import argparse
import OpenSSL
import secrets
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--private-key', type=str, default="ca/cakey.pem")
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")

CA_CN = "Advent Calendar CA Root 2021"
VALID_NOT_BEFORE = 0
VALID_NOT_AFTER = 3600 * 24 * 356 * 10 # 10 years

"""
Generate CA cert
"""
def generate_cacert(cn, key):
    # Generate a new CSR
    req = OpenSSL.crypto.X509Req()
    # Set the common name
    req.get_subject().CN = cn
    # Set the public key to the request (with SHA256 fingerprint)
    req.set_pubkey(key)
    req.sign(key, 'sha256')
    # Extension for CA
    extensions = ([
        OpenSSL.crypto.X509Extension(b'basicConstraints', False, b'CA:true'),
    ])
    req.add_extensions(extensions)
    # Create a self-signed certificate
    cert = OpenSSL.crypto.X509()
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(VALID_NOT_BEFORE)
    cert.gmtime_adj_notAfter(VALID_NOT_AFTER)
    cert.set_issuer(req.get_subject())
    cert.set_subject(req.get_subject())
    cert.set_pubkey(req.get_pubkey())
    cert.sign(key, 'sha256')
    return cert

"""
Main routine
"""
def main(args):
    # Generate a key pair using 256-bit ECDSA
    key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    # Private key PEM
    key_pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    # Public key
    pub_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # Save the private keys
    with open(args.private_key, 'wb') as f:
        f.write(key_pem)
        f.close()

    # Convert the private key information to OpenSSL format
    okey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_pem)

    # Generate a self-signed CA certificate
    cacert = generate_cacert(CA_CN, okey)
    # Dump the CSR as a PEM file
    cacert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cacert)

    # Save the CSR file
    with open(args.cacert, 'wb') as f:
        f.write(cacert_pem)
        f.close()

    print('Generated CA certificate:\n\tPrivate key: {}\n\tCA Certificate: {}\n'.format(args.private_key, args.cacert))
    print(cacert_pem.decode('utf-8'))

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
