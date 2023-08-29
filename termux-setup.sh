pkg update
pkg upgrade -y
pkg install proot-distro
proot-distro install debian
termux-setup-storage
mkdir ~/storage/repos
cd ~/storage/repos
proot-distro login debian
apt update
apt upgrade
apt install sl
sl
