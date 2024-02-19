# k3p4

K3P4 - 4 node Raspberry Pi 4 Cluster using k3s

List of hostnames for each board

- k3p4m = master k3s node
- k3p4w1 = worker k3s node #1
- k3p4w2 ...
- k3p4w3 ...

## Setting up Raspberry Pis

All pis in my build are 'Raspberry Pi 4 Model B 8gb arm64' boards, with 32gb sandisk cards.

I'm still figuring out k3s and networking and everything else.

### Needed software

`sudo apt update && sudo apt install curl vim python3-pip -y && sudo apt full-upgrade -y && sudo reboot`

### Patch Configs for k3s

```sh
# Add cgroups
sudo vim /boot/firmware/cmdline.txt

# Add this to the existing oneliner
cgroup_memory=1 cgroup_enable=memory
```

### Turn off / remove bluetooth

```sh
# sudo vim /boot/firmware/config.txt`
# disable bluetooth
dtoverlay=disable-bt
# disable wifi
dtoverlay=disable-wifi

# close and save file
```

```sh
sudo systemctl disable hciuart.service
sudo systemctl disable bluetooth.service
sudo apt purge bluez
sudo apt autoremove
sudo reboot
```

### Setting Static IPs

macos `arp -a` shows devices on network ?

pis `ip r | grep default` for dns server ip

<!-- # This didn't work because Raspberry Pi OS Bookworm uses Network Manager instead of dhcp
```sh
# sudo vim /etc/dhcpcd.conf

interface eth0
metric 300
static ip_address=192.168.0.40/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1

interface wlan0
metric 200
``` -->

Raspberry Pi OS Bookworm uses Network Manager instead of dhcpcd.service, use `sudo nmtui` to set static ip's.

Or this

```sh
# for static wifi ip with imager configed wifi
# sudo vim /etc/NetworkManager/system-connections/preconfigured.nmconnection
[ipv4]
address1=<static ip>/24,192.168.0.1
dns=192.168.0.1;1.1.1.1;8.8.8.8;
dns-search=ht.home;
may-fail=false
method=manual

# for static ethernet
# sudo vim /etc/NetworkManager/system-connections/Wired\ connection\ 1.nmconnection
[ipv4]
address1=<other static ip>/24,192.168.0.1
dns=192.168.0.1;1.1.1.1;8.8.8.8;
dns-search=ht.home;
may-fail=false
method=manual
```

## Install k3s on master node

`curl -sfl https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -s`

get your k3s token `sudo cat /var/lib/rancher/k3s/server/node-token`

## Install k3s on worker / agent nodes

`curl -sfL https://get.k3s.io | K3S_URL=https://<master static ip addr>:6443 K3S_TOKEN=<master k3s token> sh -`

### Manage / build containers

[nerdctl](https://github.com/containerd/nerdctl) might help?

```sh
curl -L https://github.com/containerd/nerdctl/releases/download/v1.7.3/nerdctl-1.7.3-linux-amd64.tar.gz > nerdctl.tar.gz
tar xzf nerdctl.tar.gz
```

## Deployment idea #1

Put my Deno Fresh Blog in to k3s.

[How to Dockerize Fresh app](https://fresh.deno.dev/docs/concepts/deployment)

Github docker build job?

https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry

How do ingress? Do I need an nginx ingress thingy pointed to fresh site?
