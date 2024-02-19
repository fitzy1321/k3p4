# k3p4

K3P4 - 4 node Raspberry Pi Cluster using k3s

Goal of this project:

I want to learn k8s deployments and hosting various apps on it, and I want to mess around with raspberry pis.

K3s will work on a pi cluster, and it's easy to get started.

## Deployment idea #1

Put my Deno Fresh Blog in to k3s.

[How to Dockerize Fresh app](https://fresh.deno.dev/docs/concepts/deployment)

[Github docker build job](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) ?

How do ingress? Do I need an nginx ingress thingy pointed to fresh site?

## Setting up Raspberry Pis

All pis in my build are 'Raspberry Pi 4 Model B 8gb arm64' boards, with 32gb sandisk cards.

OS: Raspberry Pi OS Bookworm (~Debian 12)

I'm still figuring out k3s and networking and everything else.

### Needed software

`sudo apt update && sudo apt install curl vim python3-pip -y && sudo apt full-upgrade -y && sudo reboot`

### Patch Configs for k3s

```sh
# Add cgroups
sudo vim /boot/firmware/cmdline.txt

# Add this to the existing oneliner
cgroup_memory=1 cgroup_enable=memory

# close file

# Turn off / remove bluetooth
sudo vim /boot/firmware/config.txt`

# Disable bluetooth
dtoverlay=disable-bt
# Disable wifi
#dtoverlay=disable-wifi

# close file

sudo systemctl disable hciuart.service
sudo systemctl disable bluetooth.service
sudo apt purge bluez
sudo apt autoremove
sudo reboot
```

### Setting Static IPs

`ip r | grep default` for dns server ip

`ifconfig` to see device interaces

For Raspberry Pi OS Bulleyes or lower, change dhcpcd settings

```sh
sudo vim /etc/dhcpcd.conf

interface eth0
metric 300
static ip_address=<your static ip>/24
static routers=<your router ip>
static domain_name_servers=<your dns ip>

interface wlan0
metric 200
static ip_address=<other static ip>/24
static routers=<your router ip>
static domain_name_servers=<your dns ip>
# close file

sudo reboot
```

Raspberry Pi OS Bookworm uses Network Manager instead of dhcpcd.service, use `sudo nmtui` to set static ip's.

Or this

```sh
# for static wifi ip with imager configed wifi
sudo vim /etc/NetworkManager/system-connections/preconfigured.nmconnection

[ipv4]
address1=<your static ip>/24,<your router ip>
dns=<your dns ip>;1.1.1.1;8.8.8.8;
dns-search=ht.home;
may-fail=false
method=manual
# close file

# for static ethernet
sudo vim /etc/NetworkManager/system-connections/Wired\ connection\ 1.nmconnection

[ipv4]
address1=<other static ip>/24,<router ip>
dns=<dns ip>;1.1.1.1;8.8.8.8;
dns-search=ht.home;
may-fail=false
method=manual
# close file

sudo reboot
```

### Install k3s on master node

`curl -sfl https://get.k3s.io | K3S_KUBECONFIG_MODE="644" sh -s`

get your k3s token `sudo cat /var/lib/rancher/k3s/server/node-token`

### Install k3s on worker / agent nodes

`curl -sfL https://get.k3s.io | K3S_URL=https://<master static ip addr>:6443 K3S_TOKEN=<master k3s token> sh -`

### References

- https://www.pragmaticlinux.com/2021/08/raspberry-pi-headless-setup-with-the-raspberry-pi-imager/
- https://docs.k3s.io/quick-start
- https://docs.k3s.io/installation/requirements?os=pi
- https://docs.k3s.io/related-projects
- https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address-on-raspbian-raspberry-pi-os
- https://fresh.deno.dev/docs/concepts/deployment
- https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry
