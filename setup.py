"""The setup script."""
import pathlib

from pkg_resources import parse_requirements
from setuptools import setup, find_packages


here = pathlib.Path(__file__).parent

package_name = 'cert_hero'

packages = find_packages(include=[package_name, f'{package_name}.*'])

requires = [
    'asn1crypto>=1.5.1,<2',
]

test_requires = [
    'pytest==7.4.2',
    'pytest-cov==4.1.0',
    'pytest-runner==6.0.0',
]

if (requires_dev_file := here / 'requirements-dev.txt').exists():
    with requires_dev_file.open() as requires_dev_txt:
        dev_requires = [str(req) for req in parse_requirements(requires_dev_txt)]
else:   # Running on CI
    dev_requires = []

about = {}
exec((here / package_name / '__version__.py').read_text(), about)

readme = (here / 'README.rst').read_text()
history = (here / 'HISTORY.rst').read_text()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    include_package_data=True,
    install_requires=requires,
    project_urls={
        'Documentation': 'https://cert-hero.readthedocs.io',
        'Source': 'https://github.com/rnag/cert-hero',
    },
    license=about['__license__'],
    # TODO add more relevant keywords as needed
    keywords=['cert-hero', 'cert', 'ssl', 'certificate', 'host cert'],
    classifiers=[
        # Ref: https://pypi.org/classifiers/
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ch=cert_hero.cli:main',
        ],
    },
    extras_require={
        'dev': dev_requires,
    },
    test_suite='tests',
    tests_require=test_requires,
    zip_safe=False
)
