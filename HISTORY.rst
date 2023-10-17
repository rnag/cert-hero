=======
History
=======

0.2.0 (2023-10-17)
------------------

**Features and Improvements**

* Add exported function :func:`certs_please` to concurrently retrieve SSL certificate(s) for a list
  of hostnames.
* Rename :class:`CertDict` to :class:`CertHero`.
* Add field ``Cert Status`` (default value: *SUCCESS*) to :class:`CertHero` response.
* :meth:`CertHero.__str__()` just calls :func:`json.dumps` internally, and
  no longer returns a *prettified* JSON string.
* Update docs

0.1.0 (2023-10-16)
------------------

* First release on PyPI.
