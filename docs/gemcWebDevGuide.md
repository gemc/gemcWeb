# gemcWeb Development Guide

## Introduction

This guide is meant as a quick start guide for developers wanting to con-
tribute to a web based nuclear physics simulation software.
As the name would suggest, the Geant4 based simulation software gemc is
used on the back-end. gemc was developed by Maurizio Ungaro, Ph.D, at
Thomas Jefferson National Accelerator Facility in Newport News, Virginia.
More information about gemc can be found here: [gemc](https://gemc.jlab.org/gemc/html/index.html)

This guide will cover setting up your development environment, technologies
used to develop gemcWeb, and an overview of the software design

## Setting Up Development Environment

### Installing gemc

The first thing that is necessary is to install gemc on your machine. This
can be done using the documentation available on the gemc website, linked
in the introduction section of this document. For developers attempting to
install gemc on an Ubuntu based machine, I have written a more in-depth
and user-friendly guide that will be included in the same location as this
documentation. It should be noted that the Jana and Root packages are
not used for gemcWeb and are there is no need to install them.

### Cloning the project 

Once gemc is set up, the project can be cloned from GitHub into your desired
working directory. To do this open a terminal and run:

```bash
git clone htttps://github.com/gemc/gemcWeb.git
```

### Installing Dependencies 

The necessary dependencies to develop gemcWeb are the Flask micro-framework,
the Jinja2 template engine, and virtualenv. These can all be installed using
pip. You will need to install pip fits if it is not already installed. It should be
noted that this documentation assumes you are using apt as your package
manager.

```bash
sudo apt-get install python-pip

sudo pip install Flask

sudo pip install jinja2

sudo pip install virtualenv
```

## Utlized Technologies

The technologies used to develop gemcWeb are considered rather standard.
The following will be a walk-through of them. At the end of this section is a
list of links, linking to all necessary documentation. The websites ’w3schools’
and ’tutorialspoint’ are also very useful for beginning web developers.

### Front End Technologies

In terms of design the Twitter developed Bootstrap web framework is be-
ing used. Bootstrap contains html and css based templates that provide
a consistent front end experience across all platforms. jQuery, the famous
JavaScript library , is being utilized for client-side scripting purposes.

There is no need to setup Bootstrap or jQuery in your local dev environment as they areeither being fetched from a CDN or will be included in the project cloned from GitHub.

### Back End Technologies

Flask, a Python based micro web framework is being used solely on the
back-end. It is rather easy to learn and implement. It utilizes the Jinja2
template engine. It is being used as it is powerful without being restrictive, in the sense the developer has almost unlimited design-choice freedom.

Currently, there is no database in place, however in future updates one may
be utilized to better maintain individual user’s accounts and project

### Documentation Links

* [Bootstrap](http://getbootstrap.com/)
* [jQuery](https://jquery.com/)
* [Flask](http://flask.pocoo.org/)
* [Jinja2] (http://jinja.pocoo.org/docs/2.9/)

## Software Design

### Directory Structure

The following is the directory structure of gemcWeb, highlighting important files:

```
~/gemcWeb
|-- run.py
|-- scripts.py
|__ /components
		|__ /example_experiment
		|__ /expjson
|__ /static
	|__ /css
	|__ /fonts
	|__ /images
	|__ /js
		|-- sam.js
|__ /templates
|__ /upload
|__ /users
		|__ /example_user
				|__ /projects
				|-- pwd.txt
```

#### run.py

This file is the back end. It contains a Flask configuration seciton, and handles the back end tasks. This includes URL routing, handling user data, and calling scripts that run gemc and such.

#### scripts.py

This file contatins all of the back end scripting. Included is account handling, data handling and creation, running gemc, handling results, and more.

--------

#### components

This directory contains components needed to run specfic experiments with gemc. 

##### example_experiment

This directory contains files for a gemc experiment. This includes CAD files and other such configuration files that gemc recognizes. More can be found about this on the aformentioned gemc website.

Every experiment groups needs to have a seperate directory.

##### expjson

This directory contains the .json files which store very important information
about specific experiments that is both served to the client, and used to
construct a gcard based on the user’s selection.

The naming scheme for these files is (Do not include the ’<>’):
```
<full_experiment_name>.json
```

The proper and necessary syntax for such a file is:
```
{
	"experiment": "experiment name",
	"description": "This is the experiment description.",
	"detectors": [{
						"name": "first detector name",
						"tag": "<detector name=’/directory/pointing/to/detector’ factory=’fac’ variation=’var’/>",
						"variation": "var",
						"present": "yes/no"
		},
						{ Add as many detectors as required...
		}
	]
}
```

--------

#### static

This directory is standard for any Flask application and contains all of the static files needed for the website.

##### css

This directory contains no custom css, just that required for bootstrap.

##### fonts

This directory contains bootstrap font files.

##### images

The directory contains all the images and GIFs that are served to ther website.

##### js

This directory contains not only the necessary and included JavaScript for
bootstrap, but also all the custom scripting for the site in a file called sam.js.

All the custom script is  jQuery. It should be noted that jQuery
is not locally stored on the server, but rather delivered via a CDN.

--------

#### templates

This directory is standard for a Flask application, and contains all of the
html pages for the site.

--------

#### upload

This directory is where all files uploaded by the user are stored. Currently, this is just generator library files.

--------

#### users

This directory contains all of the files for all of the users on the specfic instance of gemcWeb you are maintaining.

##### example_user

This is the directory of an example user.

###### projects

This directory conains all of the projects created by the example user. Projects are sperated into uniquely named subdirectories.

##### pwd.txt

This text file contains a hased version of the password of the user for authetication purposes.

### Getting Familiar with the Code

Read it!

Seriously, by the time any other soul, besides myself, is attempting to work
on gemcWeb it should have good in-code documentation.

Even for developer’s not familiar with Flask the code base should be rather
easy to learn, as Flask is a rather easy to use and understand micro-framework.
For completely new developers wanting to work on a project, gemcWeb is a
good option. In the original implementation I attempted to design the soft-
ware with as much straight forward code as possible, although as greater
amounts of abstraction become the norm, this gets exponentially less easy
to do.

### Client Server Model

To ease the process of getting familar with the code, appeneded to this section is a diagram of the client server model for gemcWeb:

![Client Server Model gemcWeb](gemcWeb/docs/gemcWebFlow.png  "Client Server gemcWeb")

### Testing

To test any updates you make simply run the application on the local de-
velopment server.

To do this open a terminal emulator, change to you working development
directory, and call the run.py file like any other python executable.
```
cd ~/working/development/directory

python run.py
```

To view the application as a user would, open your browser of choice and
point it to:

```
localhost:5000
```

#### Reporting Bugs and Pushing Updates

If you would like to become a main developer on the project please send me an email and you can be added to the GitHub repository.

My email address is: sam ~dot~ markelon ~at~ uconn ~dot~ edu.

There is currently not a really good system of reporting bugs, so again just
send me an email (especially if you want to implement bug reporting!).

For bugs and development inquiries pertaining directly to gemc itself please
contact Maurizio Ungaro.

His email is: ungaro ~at~ jlab ~dot~ org.

Futher inquiry of any subject can be directed to advisor Markus Diefenthaler.

His email is mdiefent ~at~ jlab ~dot~ org.
