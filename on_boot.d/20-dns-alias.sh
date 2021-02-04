#!/bin/sh

CONTAINER=dns-gen
HOSTS_DIR=/mnt/data/hosts

UNIFI_BASEURL="https://setup.ui.com"
UNIFI_USERNAME="REDACTED"
UNIFI_PASSWORD="REDACTED"

if ! grep -qxF hostsdir=${HOSTS_DIR} /run/dnsmasq.conf.d/custom.conf; then
    echo hostsdir=${HOSTS_DIR} >> /run/dnsmasq.conf.d/custom.conf
    kill -9 `cat /run/dnsmasq.pid`
fi

if podman container exists ${CONTAINER}; then
  podman start ${CONTAINER}
else
  podman run --name ${CONTAINER} \
    -e UNIFI_BASEURL=${UNIFI_BASEURL} \
    -e UNIFI_USERNAME=${UNIFI_USERNAME} \
    -e UNIFI_PASSWORD=${UNIFI_PASSWORD} \
    -v "${HOSTS_DIR}:/etc/dnsmasq.d" \
    docker.pkg.github.com/drakulix/unifi-dns-gen/unifi-dns-gen:latest
fi
