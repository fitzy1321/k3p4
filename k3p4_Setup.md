# K3P4 Setup

Goal of this project:

I want to learn k8s deployments and hosting various apps on it, and I want to mess around with raspberry pis.

K3s will work on a pi cluster, and it's easy to get started.

## Deployment idea #1

Put my Deno Fresh Blog in to k3s.

[How to Dockerize Fresh app](https://fresh.deno.dev/docs/concepts/deployment)

[Github docker build job](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) ?

How do ingress? Do I need an nginx ingress thingy pointed to fresh site?

## Setting up Raspberry Pis

### Configure OS + SD Card

I could buy 3 - 4 more Raspberry PI 5 8gb, but that requires 3 - 4 more coolers, PoE+ M.2 Hats, Active Coolers, and idk if a usb hub can power RPI 5's well enough?

USB-C might? I need to look at usb-c hub actually power delivery ...

...

Anyway, the SD Cards and OS need some setup before running k3s and ansible.

User, Hostname, Wifi, ssh enabled

Master Node Hostname ~ k3p4m
Worker Nodes Hostnames ~ k3p4w[n-1] i.e. k3p4w1

All pis in my build are 'Raspberry Pi 4 Model B 8gb arm64' boards, with 32gb sandisk cards.

OS: Raspberry Pi OS Bookworm (~Debian 12)

I'm still figuring out k3s and networking and everything else.

M.2 Hat / PCIE / Check firmware / bootware updates:

Use raspi-config to change PCIE mode

Get latest boot / firm ware

```sh
sudo rpi-eeprom-update -a
```

### Needed software

System update, and install necessary software
`sudo apt update && sudo apt install git vim curl python3-pip python3-venv -y && sudo apt full-upgrade -y && sudo reboot`

install docker, after system update:

```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh   
```

install rust

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

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

`curl -sfL https://get.k3s.io | K3S_URL=https://k3p4m.ht.home:6443 K3S_TOKEN=<master k3s token> sh -`

### ssh key

Copy the ssh key you want to use with ansible

```sh
# this should be on your main machine
ssh-copy-id -i ~/.ssh/id_rsa.pub pi@<k3p4 hostname here>
```

Turn off Password Auth after copying key

```sh
sudo vim /etc/ssh/sshd_config

# Scroll down to Authentication
PasswordAuthentication no
```

### References

- <https://www.pragmaticlinux.com/2021/08/raspberry-pi-headless-setup-with-the-raspberry-pi-imager/>
- <https://docs.k3s.io/quick-start>
- <https://docs.k3s.io/installation/requirements?os=pi>
- <https://docs.k3s.io/related-projects>
- <https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address-on-raspbian-raspberry-pi-os>
- <https://fresh.deno.dev/docs/concepts/deployment>
- <https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry>
