"""Console script for cert_hero."""
import argparse
import sys

from . import certs_please, set_expired


def main():
    """Console script for cert_hero."""
    parser = argparse.ArgumentParser(prog='ch', description='Retrieve the SSL certificate(s) for one or more given host')
    parser.add_argument('hosts', nargs='*')
    args = parser.parse_args()

    host_to_cert = certs_please(args.hosts)
    set_expired(host_to_cert)

    for host, cert in host_to_cert.items():
        print(f'=== {host} ===\n{cert!r}\n')

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
