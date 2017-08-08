# gemc Ubuntu Install Guide

***

## Install dependencies

```bash
sudo apt-get -y install g++ mysql-client libmysqlclient-dev libx11-dev libxext-dev libglu1-mesa-dev libxt-dev libxmu-dev libxrender-dev libexpat1-dev tcsh cmake libafterimage-dev scons
```

## Creating a working directory and get the install package

```bash
mkdir /opt/jlab_software

sudo chown <username> /opt/jlab_software

cd /opt/jlab_software

mkdir -p devel

wget http://www.jlab.org/12gev_phys/packages/sources/ceInstall_devel.tar.gz

tar -zxpvf ceInstall_devel.tar.gz
```

## Change the csh config file to set environment variables for gemc

```bash
nano ~/.cshrc
```

Append the following lines to the document:

```
setenv JLAB_ROOT /opt/jlab_software
source $JLAB_ROOT/devel/ce/jlab.csh
```

If you are unfamiliar with nano, hit ctrl+o to write-out, and ctrl+x to exit.

## Run the gemc install scripts

Open a new terminal window and enter a c shell

```bash
tcsh
```

```shell
cd $JLAB_ROOT/devel/install

./go_clhep

./go_xercesc

./go_qt
```

There is a separate qt installer that needs to be run. Follow the instructions displayed by the terminal.

```shell
./go_geant4

./go_sconsscript

./go_evio

./go_mysql

./go_ccdb

./go_mlibrary

./go_gemc

./go_fields

./go_banks
```

Jana and Root are not necessary for gemcWeb development. They however can be installed if desired. Root is a rather large package.

```shell
./go_root

./go_jana
```
