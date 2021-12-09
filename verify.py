import argparse
import OpenSSL

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--cacert', type=str, default="ca/cacert.pem")
parser.add_argument('--crt', type=str, default="crt.pem")

"""
Main routine
"""
def main(args):
    # Load th CA certificate
    with open(args.cacert, 'rb') as f:
        cacert_pem = f.read()
        f.close()
    cacert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cacert_pem)

    # Load th certificate
    with open(args.crt, 'rb') as f:
        cert_pem = f.read()
        f.close()
    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_pem)

    try:
        store = OpenSSL.crypto.X509Store()
        store.add_cert(cacert)
        store_ctx = OpenSSL.crypto.X509StoreContext(store, cert)
        store_ctx.verify_certificate()
    except Exception as e:
        return False

    return True

"""
Call the main routine
"""
if __name__ == "__main__":
    # Parse the arguments
    args = parser.parse_args()
    main(args)
