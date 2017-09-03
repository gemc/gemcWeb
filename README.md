# gemcWeb

## About

gemcWeb: a cloud based nuclear physics simulation software. The original main-net version is privately hosted at Jefferson National Lab. However, obviously, this is an open source project and can be easily modified, and subsequently hosted at any instituion. Those interested in doing this, or gemcWeb development should check out the docs for a full developer's guide.

## Quick Installation for development/hosting

Install gemc on dev machine. Instructions on how to do this are avaialable on the [gemc Website](https://gemc.jlab.org/gemc/html/downloads.html). A detailed Ubuntu installation guide is available in the docs.

Clone the project:
```bash
git clone https://github.com/gemc/gemcWeb.git
```

Install dependencies (pip needs to be installed, if it is not already):
```bash
sudo apt-get install python-pip

sudo pip install Flask

sudo pip install jinja2

sudo pip install virtualenv
```

You are now fully equipped to develop or host an iteration of gemcWeb.
