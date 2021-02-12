#!/usr/bin/env python3
import os
import re
import time
import sys

import requests

baseurl = os.environ.get('UNIFI_BASEURL', 'https://udm')
username = os.environ.get('UNIFI_USERNAME')
password = os.environ.get('UNIFI_PASSWORD')
site = os.environ.get('UNIFI_SITE', 'default')
fixed_only = os.environ.get('FIXED_ONLY', False)
interval = os.environ.get('INTERVAL', 60)
hostsfile = os.environ.get("HOSTS_FILE")

clients = {}

def get_configured_clients(session):
    # Get configured clients
    r = session.get(f'{baseurl}/proxy/network/api/s/{site}/list/user', verify=False)
    r.raise_for_status()
    return r.json()['data']


def get_active_clients(session):
    # Get active clients
    r = session.get(f'{baseurl}/proxy/network/api/s/{site}/stat/sta', verify=False)
    r.raise_for_status()
    return r.json()['data']

def get_networks(session):
    # Get network configurations
    r = session.get(f'{baseurl}/proxy/network/api/s/{site}/rest/networkconf/', verify=False)
    r.raise_for_status()
    return r.json()['data']


def get_clients(session):
    # Add clients with alias and reserved IP
    for c in get_configured_clients(s):
        if 'name' in c and 'fixed_ip' in c:
            clients[c['fixed_ip']] = {'names': [c['name']], 'ip': c['fixed_ip']}
            if 'network_id' in c:
                clients[c['fixed_ip']]['network'] = c['network_id']
    if fixed_only is False:
        # Add active clients with alias
        # Active client IP overrides the reserved one (the actual IP is what matters most)
        for c in get_active_clients(s):
            if 'name' in c and 'ip' in c:
                clients[c['ip']] = {'names': [c['name']], 'ip': c['ip']}
                if 'network_id' in c:
                    clients[c['ip']]['network'] = c['network_id']
                if 'hostname' in c:
                    if re.search('^[a-zA-Z0-9-]+$', c['hostname']):
                        clients[c['ip']]['names'].append(c['hostname'])

    # Return a list of clients filtered on dns-friendly names and sorted by IP
    friendly_clients = [c for c in clients.values() if re.search('^[a-zA-Z0-9-]+$', c['names'][0])]
    return sorted(friendly_clients, key=lambda i: i['names'][0])


if __name__ == '__main__':
    while True:
        try:
            with open(hostsfile, 'w') as f:
                s = requests.Session()

                # Log in to controller
                r = s.post(f'{baseurl}/api/auth/login', json={'username': username, 'password': password}, verify=False)
                r.raise_for_status()

                networks = {net['_id']: net['domain_name'] for net in get_networks(s) if 'domain_name' in net}
                for c in get_clients(s):
                    if 'network' in c and c['network'] in networks:
                        print(c['ip'], ' '.join(name + ' ' + name+"."+networks[c['network']] for name in c['names']), file=f)
                    else:
                        print(c['ip'], ' '.join(name for name in c['names']), file=f)
        except requests.exceptions.ConnectionError as e:
            print(f'Could not connect to unifi controller at {baseurl}', file=sys.stderr)
            print(e, file=sys.stderr)
        except OSError as e:
            print(f'Could not open file {hostsfile}', file=sys.stderr)
            print(e, file=sys.stderr)
            exit(1)
        time.sleep(interval)


