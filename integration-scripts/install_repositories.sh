#!/bin/sh

sudo apt update
sudo apt install software-properties-common python-software-properties

echo "Adding R cran repositories"
version=`lsb_release -r | awk '{ print $2;}'`

case ${version} in
    "14.04")
	echo "deb http://cran.rstudio.com/bin/linux/ubuntu trusty/" | sudo tee -a /etc/apt/sources.list
	;;
    "16.04")
	echo "deb http://cran.rstudio.com/bin/linux/ubuntu xenial/" | sudo tee -a /etc/apt/sources.list
	;;
    *) echo "Unsupported version of Ubuntu detected, aborting"
       exit 1;;
esac

sudo apt update
