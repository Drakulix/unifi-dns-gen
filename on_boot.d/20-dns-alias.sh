#!/bin/sh

CONTAINER=dns-gen
HOSTS_DIR=/mnt/data/hosts

UNIFI_BASEURL="https://127.0.0.1"
UNIFI_USERNAME="REDACTED"
UNIFI_PASSWORD="REDACTED"

if ! grep -qxF hostsdir=${HOSTS_DIR} /run/dnsmasq.conf.d/custom.conf; then
    echo hostsdir=${HOSTS_DIR} >> /run/dnsmasq.conf.d/custom.conf
    kill -9 `cat /run/dnsmasq.pid`
fi

if podman container exists ${CONTAINER}; then
  podman start ${CONTAINER}
else
  podman run --name ${CONTAINER} -d \
    --net host \
    -e UNIFI_BASEURL=${UNIFI_BASEURL} \
    -e UNIFI_USERNAME=${UNIFI_USERNAME} \
    -e UNIFI_PASSWORD=${UNIFI_PASSWORD} \
    -v "${HOSTS_DIR}:/hosts" \
    ghcr.io/drakulix/unifi-dns-gen:latest
fi
