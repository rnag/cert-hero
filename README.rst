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


Python Stand-alone Library to Download the SSL Certificate for *Any Host™*

* Documentation: https://cert-hero.readthedocs.io.

-------------------

**Why Use?**

* This library *always* returns the SSL certificate, if a server has one. This works for expired
  and `self-signed certificate`_, whereas the builtin `ssl`_ library returns an empty ``dict`` if verification fails
  for any reason (source_).

* The *only* dependency is `asn1crypto`_ (with over 300 stars on GitHub), which is ~94% more lightweight and robust
  than a solution with `pyOpenSSL`_.

* If host a *redirects* to another URL, this info is captured in ``Location`` and ``Status``.

* Convenience methods such as ``__repr__()`` to make output more human-readable.

**Core Exports**

* `cert_please`_ - Retrieve the SSL certificate for a given hostname.
* `certs_please`_ - Retrieve (concurrently) the SSL certificate(s) for a list of hostnames.
* `set_expired`_ - Helper function  to check (at runtime) if a cert is expired or not.

.. _ssl: https://docs.python.org/3/library/ssl.html
.. _asn1crypto: https://pypi.org/project/asn1crypto
.. _pyOpenSSL: https://pypi.org/project/pyOpenSSL/
..  _source: https://stackoverflow.com/a/74349032/10237506
.. _self-signed certificate: https://stackoverflow.com/a/68889470/10237506
.. _`cert_please`: https://cert-hero.readthedocs.io/en/latest/cert_hero.html#cert_hero.cert_please
.. _`certs_please`: https://cert-hero.readthedocs.io/en/latest/cert_hero.html#cert_hero.certs_please
.. _`set_expired`: https://cert-hero.readthedocs.io/en/latest/cert_hero.html#cert_hero.set_expired

Install
-------

.. code-block:: console

    $ pip install cert-hero

Usage
-----

Fetch the SSL certificate for a **host** with ``cert_please()``:

.. code:: python3

    import cert_hero

    cert = cert_hero.cert_please('google.com')

    print('Cert is Valid Till:', cert.not_after_date.isoformat())

    # To get the output as a JSON string, use `str(cert)` or remove `!r` from below
    print(f'Cert -> \n{cert!r}')

    cert_hero.set_expired(cert)
    print(f'Validity ->\n{cert["Validity"]}')

*Output (Sample)*

.. code::

    Cert is Valid Till: 2023-10-28
    Cert ->
    CertHero(
      {
        "Cert Status": "SUCCESS",
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
    Validity ->
    {'Not After': '2023-10-28', 'Not Before': '2023-10-14', 'Expired': False}

Fetch (concurrently) the SSL certificates for **multiple hosts** with ``certs_please()``:

.. code:: python3

    import cert_hero

    host_to_cert = cert_hero.certs_please(['google.com', 'cnn.com', 'www.yahoo.co.in', 'youtu.be'])
    cert_hero.set_expired(host_to_cert)

    for host, cert in host_to_cert.items():
        print(f'=== {host.center(17)} ===')
        # To get the output as a JSON string, use `str(cert)` or remove `!r` from below
        print(f'{cert!r}')
        print()

*Output (Sample)*

.. code::

    ===     google.com    ===
    CertHero(
      {
        "Cert Status": "SUCCESS",
        "Serial": "753DD6FF20CB1B4510CB4C1EA27DA2EB",
        "Subject Name": {
          "Common Name": "*.google.com"
        },
        ...
      }
    )

    ===      cnn.com      ===
    CertHero(
      {
        "Cert Status": "SUCCESS",
        "Serial": "7F2F3E5C350554D71A6784CCFE6E8315",
        "Subject Name": {
          "Common Name": "cnn.com"
        },
        ...
      }
    )

    ===  www.yahoo.co.in  ===
    CertHero(
      {
        "Cert Status": "SUCCESS",
        "Serial": "7D7FD7B7C2EE7146B4D4E43E36908B72",
        "Subject Name": {
          "Common Name": "src1.yahoo.com"
        },
        ...
      }
    )

    ===      youtu.be     ===
    CertHero(
      {
        "Cert Status": "SUCCESS",
        "Serial": "753DD6FF20CB1B4510CB4C1EA27DA2EB",
        "Subject Name": {
          "Common Name": "*.google.com"
        },
        ...
      }
    )

Usage as a CLI
--------------

After the installation step you can use cert-hero just typing ``ch`` in your terminal window.

The ``ch`` command allows you to retrieve the SSL certificate(s) for one or more given host.

For example::

    ch google.com cnn.com

You can get help about the main command using::

    ch --help

Rationale
---------

The builtin Python module ``ssl`` can be used to retrieve a certificate from a server via ``getpeercert``,
but it'll work only if the certificate of interest can be successfully verified (source_).

If, for any reason, verification fails, like, for example, with expired or a `self-signed certificate`_,
we'll get ``ssl.SSLCertVerificationError`` instead of the requested info.

We can work around this by asking for the certificate in the binary form:

.. code-block:: python3

    getpeercert(binary_form=True)

But now we have to convert it, and thus we can use a third party ``asn1crypto`` module, instead of
the (bulkier) ``cryptography`` module.

Credits
-------

This package was created with Cookiecutter_ and the `rnag/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _`rnag/cookiecutter-pypackage`: https://github.com/rnag/cookiecutter-pypackage
