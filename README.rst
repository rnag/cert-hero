=========
Cert Hero
=========


.. image:: https://img.shields.io/pypi/v/cert-hero.svg
        :target: https://pypi.org/project/cert-hero

.. image:: https://img.shields.io/pypi/pyversions/cert-hero.svg
        :target: https://pypi.org/project/cert-hero

.. image:: https://github.com/rnag/cert-hero/actions/workflows/dev.yml/badge.svg
        :target: https://github.com/rnag/cert-hero/actions/workflows/dev.yml

.. image:: https://readthedocs.org/projects/cert-hero/badge/?version=latest
        :target: https://cert-hero.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/rnag/cert-hero/shield.svg
     :target: https://pyup.io/repos/github/rnag/cert-hero/
     :alt: Updates



Python Stand-alone Library to Download SSL Certificate for *Any Host™*


* Free software: MIT license
* Documentation: https://cert-hero.readthedocs.io.


Rationale
---------

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

Usage
-----

Retrieve the certificate for **host** ``google.com``:

.. code:: python3

    import json
    import cert_hero

    cert = cert_hero.cert_please('google.com')

    print('Cert is Valid Till:', cert.not_after_date.isoformat())
    print(f'Cert Details:', json.dumps(cert, indent=2), sep='\n')

Output (Sample):

.. code::

    Cert is Valid Till: 2023-10-28
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

Usage as a CLI
--------------

After the installation step you can use cert-hero just typing ``ch`` in your terminal window.

The ``ch`` command allows you to retrieve the SSL certificate(s) for one or more given host.

For example::

    ch google.com cnn.com

You can get help about the main command using::

    ch --help

Credits
-------

This package was created with Cookiecutter_ and the `rnag/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`rnag/cookiecutter-pypackage`: https://github.com/rnag/cookiecutter-pypackage
