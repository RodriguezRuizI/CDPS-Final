#!/bin/sh

sudo dpkg --configure -a
sudo apt-get update -y
sudo apt-get install python -y
wget http://idefix.dit.upm.es/cdps/pfinal/pfinal.tgz
sudo vnx --unpack pfinal.tgz
./pfinal/bin/prepare-pfinal-vm
sudo chmod a+rx Confi_Inicial.py
sudo ./Confi_Inicial.py ayuda
