#!/bin/sh
hosts_dir=/hosts
unifi_hosts=$hosts_dir/unifi.hosts

while true; do
    ./get_unifi_reservations.py > $unifi_hosts
    sleep ${UNIFI_POLL_INTERVAL:-600}
done

