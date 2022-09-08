#!/bin/sh
cd /home/pi/photobooth
#sudo mount /dev/sda1 /home/pi/photobooth/mounted_datas
#sudo /etc/init.d/samba restart
#v="`cat /sys/class/net/wlan0/operstate`"
#v1="up"

#echo $v
#echo $v1

#if [ "$v" = "$v1" ];
#  then echo "wlan0 up : starting samba"
#  sudo /etc/init.d/samba restart
#fi
sudo filebrowser -r /home/pi -a "" -p 80 &
while [ 1 ]; do sudo python3 photobooth.py -photobooth 1; test $? -gt 128 && break; done
