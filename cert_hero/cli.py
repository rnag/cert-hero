"""Console script for cert_hero."""
import argparse
import sys

from . import cert_please


def main():
    """Console script for cert_hero."""
    parser = argparse.ArgumentParser(prog='ch', description='Retrieve the SSL certificate(s) for one or more given host')
    parser.add_argument('hosts', nargs='*')
    args = parser.parse_args()

    for host in args.hosts:
        cert = cert_please(host)
        print(f'=== {host} ===')
        print(cert)
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
