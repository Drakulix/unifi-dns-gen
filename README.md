# What it is

A hosts-file generator by aliases made in a UniFi controller to be run on a UDM.

# But why?

To make up for the fact that UniFi USG doesn't have hostname alias/override for clients.

# How it works

It polls a UniFi controller and writes client aliases and IP addresses to a file being picked up by UDM's dnsmasq. Clients with DNS-incompatible names will be skipped.

## Build

* Run `podman build -t unifi-dns-gen .`
* *Note*: If you are not doing this on your UDM, you need qemu-user-static-aarch64 to build this image 

## Run

* SSH into your Dream Machine
* Make a folder to hold your host files: `mkdir /mnt/data/hosts`
* Run: `podman run --name unifi-dns-gen -e UNIFI_BASEURL=https://192.168.1.1 -e UNIFI_USERNAME='REDACTED' -e UNIFI_PASSWORD='REDACTED' -e HOSTS_FILE="/hosts/unifi.hosts -v "/mnt/data/hosts:/hosts" -it --rm ghcr.io/drakulix/unifi-dns-gen:latest`
* Add a file with `hostsdir=/mnt/data/hosts` as contents to `/run/dnsmasq.d`
* Restart dnsmasq: `pkill dnsmasq`

| Env variable     | Description                                        | Required | Default |
| ---------------- | -------------------------------------------------- | -------- | ------- |
| `UNIFI_BASEURL`  | Url of the Unifi Controller @ you UDM              |      yes |         |
| `UNIFI_USERNAME` | Username to log into your controller               |      yes |         |
| `UNIFI_PASSWORD` | Password to log into your controller               |      yes |         |
| `UNIFI_SITE`     | Site to enumerate                                  |       no | default |
| `HOSTS_FILE`     | File to write host entries into                    |      yes |         |
| `FIXED_ONLY`     | Only write out clients with fixed ip addresses     |       no | `False` |
| `INTERVAL`       | Interval at which to poll controller (in seconds)  |       no |     60  |

## Persist

To avoid doing this again after each restart check out the awesome [`udm-utilities`](https://github.com/boostchicken/udm-utilities/) repository and setup on-boot-scripts.

You can then download and copy [`on_boot.d/20-dns-alias.sh`](https://github.com/drakulix/unifi-dns-gen/raw/master/on_boot.d/20-dns-alias.sh) into `/mnt/data/on_boot.d`.


# Credits

To [`unifi-dns`](https://github.com/wicol/unifi-dns) and [`UDM-DNS-Fix`](https://github.com/cdchris12/UDM-DNS-Fix)
