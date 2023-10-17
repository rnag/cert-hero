import json

from cert_hero import cert_please, certs_please, set_expired


def test_cert_please():
    cert = cert_please('google.com')

    print('Cert is Valid Till:', cert.not_after_date.isoformat())

    # To get the output as a JSON string, use `str(cert)` or remove `!r` from below
    print(f'Cert -> \n{cert!r}')

    assert cert['Subject Name']['Common Name'] == '*.google.com'

    set_expired(cert)
    print(f'Validity ->\n{cert["Validity"]}')

    # assert the cert is still valid!
    assert not cert['Validity']['Expired']


def test_certs_please():
    host_to_cert = certs_please(['google.com', 'cnn.com', 'www.yahoo.co.in', 'youtu.be'])
    set_expired(host_to_cert)

    for host, cert in host_to_cert.items():
        print(f'=== {host.center(17)} ===')
        print(f'{cert!r}')
        print()


def test_set_expired_with_cert_please_response_serialized():
    cert = cert_please('google.com')

    cert_reloaded = json.loads(str(cert))

    set_expired(cert_reloaded)
    assert not cert_reloaded['Validity']['Expired']

    # print(f'Cert -> \n{cert_reloaded!r}')


def test_set_expired_with_certs_please_response_serialized():
    host_to_cert = certs_please(['google.com', 'cnn.com', 'www.yahoo.co.in', 'youtu.be'])

    host_to_cert_reloaded = json.loads(json.dumps(host_to_cert))

    set_expired(host_to_cert_reloaded)

    for host, cert in host_to_cert_reloaded.items():
        assert not cert['Validity']['Expired']

    # print(f'Cert -> \n{host_to_cert_reloaded!r}')
