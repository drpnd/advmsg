import argparse
import OpenSSL
import secrets
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--private-key', type=str, default="key.pem")
parser.add_argument('--public-key', type=str, default="pub.pem")
parser.add_argument('--csr', type=str, default="csr.pem")

# ID Length
ID_BITS = 256

"""
Generate ID
"""
def generate_id(tostr=False):
    # Generate a cryptographically-secure pseudo-random number as an identifier
    ident = secrets.randbits(ID_BITS)
    if tostr:
        return '{:0>64x}'.format(ident)
    else:
        return ident

"""
Generate CSR
"""
def generate_csr(cn, key):
    # Generate a new CSR
    req = OpenSSL.crypto.X509Req()
    # Set the common name
    req.get_subject().CN = cn
    # Set the public key to the request (with SHA256 fingerprint)
    req.set_pubkey(key)
    req.sign(key, 'sha256')
    return req

"""
Main routine
"""
def main(args):
    # Generate an identifier
    ident = generate_id(True)
    # Generate a key pair using 256-bit ECDSA
    key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    # Private key PEM
    key_pem = key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm=serialization.NoEncryption())
    # Public key
    pub_pem = key.public_key().public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)

    # Save the private and public keys
    with open(args.private_key, 'wb') as f:
        f.write(key_pem)
        f.close()
    with open(args.public_key, 'wb') as f:
        f.write(pub_pem)
        f.close()

    # Convert the private key information to OpenSSL format
    okey = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, key_pem)

    # Generate a CSR
    req = generate_csr(ident, okey)
    # Dump the CSR as a PEM file
    req_pem = OpenSSL.crypto.dump_certificate_request(OpenSSL.crypto.FILETYPE_PEM, req)

    # Save the CSR file
    with open(args.csr, 'wb') as f:
        f.write(req_pem)
        f.close()

    print('Generated an ID: {}\n\tPrivate key: {}\n\tPublic key: {}\n\tCSR: {}\n'.format(ident, args.private_key, args.public_key, args.csr))
    print(req_pem.decode('utf-8'))

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
