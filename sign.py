import argparse
import OpenSSL
import secrets
import sqlite3
import time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--private-key', type=str, default="ca/cakey.pem")
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")
parser.add_argument('--csr', type=str, default='csr.pem')
parser.add_argument('--crt', type=str, default='crt.pem')

DATABASE_FILE = "ca/ca.db"
VALID_NOT_BEFORE = 0
VALID_NOT_AFTER = 3600 * 24 * 356 * 3 # 3 years

"""
Generate a serial number (actually not serial but random number)
"""
def generate_serial():
    return secrets.randbits(160)

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

    # Get the requested common name
    cn = req.get_subject().CN

    # Open the database
    db = sqlite3.connect(DATABASE_FILE)

    # Check the common name first
    cur = db.cursor()
    sql = 'select count(*) from cert where cn=? and active=true'
    cur.execute(sql, (cn, ))
    res = cur.fetchone()
    if res[0] > 0:
        print("Duplicate common name: {}".format(cn))
        db.close()
        return False

    # Generate a serial number
    serial = generate_serial()
    serial_str = '{:0>40x}'.format(serial)

    # Sign the CSR by the CA certificate
    cert = sign(req, cacert, key, serial)

    # Dump the signed certificate as a PEM file
    cert_pem = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

    # Start the transaction
    db.execute('begin')
    cur = db.cursor()
    sql = 'select count(*) from cert where (serial=? or cn=?) and active=true'
    cur.execute(sql, (serial_str, cn))
    res = cur.fetchone()
    if res[0] > 0:
        print('Duplicate serial number or common nameerror:\nSerial: {}\nCommon Name: {}'.format(serial_str, cn))
        db.close()
        return False
    sql = 'insert into cert (serial, cn, cert, active) values (?, ?, ?, ?)'
    try:
        cur.execute(sql, (serial_str, cn, cert_pem.decode('utf-8'), True))
    except sqlite3.IntegrityError:
        print('Transaction error')
        db.close()
        return False
    db.commit()

    # Close the database
    db.close()

    # Save the signed certificate
    with open(args.crt, 'wb') as f:
        f.write(cert_pem)
        f.close()

    print("Saved the signed certificate to {}".format(args.crt))
    print(cert_pem.decode('utf-8'))

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
