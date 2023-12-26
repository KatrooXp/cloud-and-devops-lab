#!/bin/bash

#install dhcp server
sudo apt update -y
sudo apt install isc-dhcp-server -y

#configure dhcp server
sudo sed -i 's/INTERFACESv4=""/INTERFACESv4="enp0s8"/' /etc/default/isc-dhcp-server

sudo sed -i 's/#authoritative;/authoritative;/' /etc/dhcp/dhcpd.conf

sudo tee -a /etc/dhcp/dhcpd.conf << END
subnet 192.168.56.0 netmask 255.255.255.0 {
 range 192.168.56.10 192.168.56.20;
 option routers 192.168.56.254;
 option domain-name-servers 8.8.8.8, 8.8.4.4;
}
END

#start dhcp server
sudo systemctl start isc-dhcp-server.service



