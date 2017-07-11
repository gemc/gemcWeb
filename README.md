# gemcWeb Quick Start

## Install gemc

**This is an Ubuntu install guide for gemc**

Other install options are avaible on the [gemc website] (http://gemc.jlab.org/gemc/html/index.html)

### Install dependencies 

```bash
sudo apt-get -y install g++ mysql-client libmysqlclient-dev libx11-dev libxext-dev libglu1-mesa-dev libext-dev libxmu-dev libxrender-dev libexpat1-dev tcsh cmake libadterimage-dev scons
```

### Creating a working directory and get install package

```bash
sudo chown <username> /opt

mkdir /opt/jlab_software

cd /opt/jlab_software

mkdir -p devel

wget http://www.jlab.org/12gev_phys/packages/sources/ceInstall_devel.tar.gz

tar -zxpvf ceInstall_devel.tar.gz
```

### Change the csh config file to set environment variables for gemc

```bash
nano ~/.cshrc
```

Append the following lines to the document:

```
setenv JLAB_ROOT /opt/jlab_software
source $JLAB_ROOT/devel/ce/jlab.csh
```

If you are unfamiliar with nano, hit ctrl+o to write-out, and ctrl+x to exit.

### Run gemc install scripts

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

There is a seperate qt installer that needs to be run. Follow the instructions displayed by the terminal.

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

Jana and Root are not necessary for gemcWeb development.

## Cloning the Project

Create a working directory, change to it, and clone the GitHub project.

```bash
git clone https://github.com/gemc/gemcWeb.git
```

## Install Dependencies

All the dependencies can be installed via pip; which needs to be installed if it is not already.

```bash
sudo apt-get install python-pip

sudo pip install Flask

sudo pip install jinja2

sudo pip install virtualenv
```

**You are now fully equipped to develop gemcWeb**
