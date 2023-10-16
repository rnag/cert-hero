"""
Cert Hero
~~~~~~~~~

Python Stand-alone Library to Download SSL Certs for Any Host

Sample Usage:

    >>> import cert_hero

For full documentation and more advanced usage, please see
<https://cert-hero.readthedocs.io>.

:copyright: (c) 2023 by Ritvik Nag.
:license:MIT, see LICENSE for more details.
"""

__all__ = [

]

import logging


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger('cert_hero').addHandler(logging.NullHandler())
