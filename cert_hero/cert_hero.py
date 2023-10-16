"""Main module."""

import ssl
import socket
from logging import getLogger

from asn1crypto.x509 import Certificate
from asn1crypto.keys import PublicKeyInfo
from datetime import datetime, date


LOG = getLogger('cert_hero')


def create_ssl_context() -> ssl.SSLContext:
    # upgrade the socket to SSL without checking the certificate
    # !!!! don't transfer any sensitive data over this socket !!!!
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    return ctx


key_map = {
    'country_name': 'Country',
    'locality_name': 'Locality',
    'organization_name': 'Organization',
    'organizational_unit_name': 'Organization Unit',
    'state_or_province_name': 'State/Province',
    'common_name': 'Common Name',
    # 'C': 'Country',
    # 'countryName': 'Country',
    # 'ST': 'State/Province',
    # 'stateOrProvinceName': 'State/Province',
    # 'L': 'Locality',
    # 'localityName': 'Locality',
    # 'O': 'Organization',
    # 'organizationName': 'Organization',
    # 'OU': 'Organization Unit',
    # 'organizationalUnitName': 'Organization Unit',
    # 'CN': 'Common Name',
    # 'commonName': 'Common Name',
}

ctx = create_ssl_context()


def key_algo(cert: Certificate):
    pub_key: PublicKeyInfo = cert.public_key
    # print(pub_key.native)

    return f'{pub_key.algorithm.upper()}-{pub_key.bit_size}'


def sig_algo(cert: Certificate):
    """
    :return:
        A unicode string of "md2", "md5", "sha1", "sha224", "sha256",
        "sha384", "sha512", "sha512_224", "sha512_256" or "shake256"
    """
    algorithm = cert['signature_algorithm']['algorithm'].native
    return algorithm.upper().replace('_', 'WITH', 1)


def set_expired(certs: 'CertDict | list[CertDict] | None'):
    """
    Set or update a value for ``Validity > Expired`` (:type:`bool`) on
    a :class:`CertDict` response
    from :func:`cert_please()` or :func:`certs_please()`.

    Example Usage::

        >>> from cert_hero import cert_please, set_expired
        >>> cert = cert_please('google.com')
        >>> assert 'Expired' not in cert['Validity']
        >>> set_expired(cert)
        >>> assert 'Expired' in cert['Validity']

    """
    if not certs:
        return

    if isinstance(certs, CertDict):
        set_expired([certs])
        return

    today = datetime.utcnow().date()

    for cert in certs:
        if cert:
            cert['Validity']['Expired'] = cert.not_after_date < today


class CertDict(dict):
    _not_after_date: date
    _not_before_date: date

    @property
    def not_after_date(self):
        return self._not_after_date

    @property
    def not_before_date(self):
        return self._not_before_date


def cert_please(hostname: str,
                context: ssl.SSLContext = None,
                default_encoding='latin-1',
                ) -> CertDict[str, dict[str, str] | str | int] | None:
    """
    Retrieve the SSL certificate for a given ``hostname`` - works even
    in the case of expired or self-signed certificates.

    Usage::

    >>> import json
    >>> import cert_hero
    >>> cert = cert_hero.cert_please('google.com')
    >>> cert.not_after_date
    datetime.date(2023, 10, 28)
    >>> print('Cert is Valid Till:', cert.not_after_date.isoformat())
    Cert is Valid Till: 2023-10-28
    >>> print(f'Cert Details:', json.dumps(_cert, indent=2), sep='\n')
    Cert Details:
    {
      "Serial": "753DD6FF20CB1B4510CB4C1EA27DA2EB",
      "Subject Name": {
        "Common Name": "*.google.com"
      },
      "Issuer Name": {
        "Country": "US",
        "State/Province": "California",
        "Organization": "Zscaler Inc.",
        "Organization Unit": "Zscaler Inc.",
        "Common Name": "Zscaler Intermediate Root CA (zscalerthree.net) (t) "
      },
      "Validity": {
        "Not After": "2023-10-28",
        "Not Before": "2023-10-14"
      },
      "Wildcard": true,
      "Signature Algorithm": "SHA256WITHRSA",
      "Key Algorithm": "RSA-2048",
      "Subject Alt Names": [
        "*.google.com",
        "*.appengine.google.com",
        "youtu.be",
        "*.youtube.com",
        ...
      ],
      "Location": "https://www.google.com/",
      "Status": 301
    }

    Rationale:

    The builtin Python module ``ssl`` can be used to retrieve a certificate from a server via ``getpeercert``,
    but it'll work only if the certificate of interest can be successfully verified (source_).

    If, for any reason, verification fails, like, for example, with expired or a `self-signed certificate`_,
    we'll get ``ssl.SSLCertVerificationError`` instead of the requested info.

    We can work around this by asking for the certificate in the binary form:

        getpeercert(binary_form=True)

    But now we have to convert it, and thus we can use a third party ``asn1crypto`` module, instead of
    the (bulkier) ``cryptography`` module.

    ..  _source: https://stackoverflow.com/a/74349032/10237506
    .. _self-signed certificate: https://stackoverflow.com/a/68889470/10237506

    """
    if context is None:
        context = create_ssl_context()

    # with socket.create_connection()
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(3)
            with context.wrap_socket(
                sock, server_hostname=hostname
            ) as wrap_socket:
                wrap_socket.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
                )

                wrap_socket.connect((hostname, 443))

                # get certificate
                cert_bin = wrap_socket.getpeercert(True)

                headers = (
                    f'GET / HTTP/1.0\r\n'
                    f'Host: {hostname}\r\n'
                    'User-Agent: python-requests/2.22.0\r\n'
                    'Accept-Encoding: gzip, deflate\r\nAccept: */*'
                    '\r\n\r\n'
                )
                # print("\n\n" + headers)

                wrap_socket.send(headers.encode())  # send request

                data = bytes()
                while True:
                    this_data = wrap_socket.recv(512)
                    if not this_data:
                        break
                    data += this_data

                #  Latin-1 (or ISO-8859-1) is a safe default: it will always
                #  decode any bytes (though the result may not be useful).
                response = data.decode(default_encoding)

                # Get the first line (the "status line")
                # Ref: https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages
                status_line = response.split('\n', 1)[0]

                # HTTP/1.1 301 Moved Permanently
                try:
                    status_code = int(status_line.split(' ', 2)[1])
                except (ValueError, TypeError):
                    status_code = None

                # print(response)  # print receive response

                loc = None
                if (loc_start := response.find('\nLocation: ')) != -1:
                    loc = response[loc_start + 11:].split('\r\n', maxsplit=1)[
                        0
                    ]
    except socket.gaierror as e:
        # curl: (6) Could not resolve host: <hostname>
        if e.errno == 8:
            # [Errno 8] nodename nor servname provided, or not known
            LOG.error(f'gaierror: could not resolve host. {hostname=}')
            ...
        else:
            LOG.error(f'{e.__class__.__name__}: {e}. {hostname=}')
        return None
    except ssl.SSLEOFError:
        # SSL/TLS connection terminated abruptly.
        # message: "EOF occurred in violation of protocol"
        # this could indicate bad cert or website is down
        LOG.error(f'SSLEOFError: bad cert. {hostname=}')
        return None
    except ssl.SSLError as e:
        #
        LOG.error(f'{e.__class__.__name__}: {e}. {hostname=}')
        return None
    # except socket.error as e:
    #     print(f'{e.__class__.__name__}: Error for {hostname}: {e}')
    #     return None
    except Exception as e:
        LOG.error(f'{e.__class__.__name__}: General Error - {e}. {hostname=}')
        return None
    else:
        _cert: Certificate = Certificate.load(cert_bin)

        # print(_cert)
        # print(dumps(_cert.native, default=str))
        # print(_cert.self_signed)

        # print(dict(_cert.subject.native))
        # print(dict(_cert.issuer.native))
        # pprint(_cert.native)
        # print(_cert.subject_alt_name_value.native)

        cert_info = CertDict(
            {
                'Serial': format(_cert.serial_number, 'X'),
                'Subject Name': (
                    subject := {
                        key_map.get(k, k): v
                        for k, v in _cert.subject.native.items()
                    }
                ),
                'Issuer Name': {
                    key_map.get(k, k): v for k, v in _cert.issuer.native.items()
                },
                'Validity': {
                    'Not After': (
                        not_after_date := _cert.not_valid_after.date()
                    ).isoformat(),
                    'Not Before': (
                        not_before_date := _cert.not_valid_before.date()
                    ).isoformat(),
                },
                'Wildcard': subject['Common Name'].startswith('*'),
                'Signature Algorithm': sig_algo(_cert),
                'Key Algorithm': key_algo(_cert),
            }
        )

        cert_info._not_after_date = not_after_date
        cert_info._not_before_date = not_before_date

        if subj_alt_names := _cert.subject_alt_name_value.native:
            cert_info['Subject Alt Names'] = subj_alt_names

        if loc:
            cert_info['Location'] = loc

        if status_code:
            cert_info['Status'] = status_code  # type: ignore

        return cert_info
