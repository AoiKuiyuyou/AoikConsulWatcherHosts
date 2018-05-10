# coding: utf-8
from __future__ import absolute_import

from collections import OrderedDict
import os
import os.path
import sys


CONSUL_HOST = os.environ.get('CONSUL_HOST', '127.0.0.1')

CONSUL_PORT = int(os.environ.get('CONSUL_PORT', '8500'))

DOMAIN_IP = os.environ.get('DOMAIN_IP', '127.0.0.1')


_HOSTS_FILE_PATH = 'C:/Windows/System32/drivers/etc/hosts' \
    if sys.platform.startswith('win32') else '/etc/hosts'

_EXISTING_MAP_NAME_TO_IP = None


def handle_service_infos(service_infos):
    global _EXISTING_MAP_NAME_TO_IP

    if _EXISTING_MAP_NAME_TO_IP is None:

        _EXISTING_MAP_NAME_TO_IP = OrderedDict()

        if os.path.isfile(_HOSTS_FILE_PATH):
            existing_hosts_text = open(_HOSTS_FILE_PATH).read()

            for line in existing_hosts_text.split('\n'):
                line = line.strip()

                if not line:
                    continue

                if line.startswith('#'):
                    continue

                line_parts = line.split(None, 1)

                if len(line_parts) == 2:
                    domain_ip = line_parts[0]
                    domain_name = line_parts[1]
                    _EXISTING_MAP_NAME_TO_IP[domain_name] = domain_ip

    map_name_to_ip = OrderedDict(_EXISTING_MAP_NAME_TO_IP)

    filtered_service_infos = dict(
        (service_name, service_info)
        for service_name, service_info in service_infos.items()
        if filter_service(service_name, service_info)
    )

    for service_name, service_info in filtered_service_infos.items():
        map_name_to_ip[service_info['domain_name']] = service_info['domain_ip']

    dns_items = [
        '{0} {1}'.format(domain_ip, domain_name)
        for domain_name, domain_ip in map_name_to_ip.items()
    ]

    hosts_text = '\n'.join(dns_items) + '\n'

    with open(_HOSTS_FILE_PATH, mode='w') as hosts_file:
        hosts_file.write(hosts_text)

    msg = 'Updated `{0}`.'.format(_HOSTS_FILE_PATH)

    print(msg)


def filter_service(service_name, service_info):
    nodes = service_info.get('nodes', None)

    if not nodes:
        return False

    node = nodes[0]

    if not node.get('ServiceAddress', None):
        return False

    if not node.get('ServicePort', None):
        return False

    service_info['domain_ip'] = DOMAIN_IP

    if service_name == 'consul-8500':
        service_info['domain_name'] = 'consul.local'
    else:
        service_info['domain_name'] = service_name + '.local'

    return True
