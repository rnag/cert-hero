"""
Cert Hero
~~~~~~~~~

Python Stand-alone Library to Download the SSL Certificate for *Any Host™*

Sample Usage:

    >>> import cert_hero
    >>> cert = cert_hero.cert_please('google.com')
    >>> cert.not_after_date
    datetime.date(2023, 10, 28)
    >>> f'Cert is Valid Till: {cert.not_after_date.isoformat()}'
    'Cert is Valid Till: 2023-10-28'
    >>> cert
    CertDict(
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
    )
    >>> cert_hero.set_expired(cert)
    >>> cert['Validity']
    {'Not After': '2023-10-28', 'Not Before': '2023-10-14', 'Expired': False}

For full documentation and more advanced usage, please see
<https://cert-hero.readthedocs.io>.

:copyright: (c) 2023 by Ritvik Nag.
:license:MIT, see LICENSE for more details.
"""

__all__ = [
    # Core exports
    'cert_please',
    # Models
    'CertDict',
    # Utilities
    'create_ssl_context',
    'set_expired',
]

import logging

from .cert_hero import CertDict, cert_please, create_ssl_context, set_expired

# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger('cert_hero').addHandler(logging.NullHandler())
