Graveyard Ghoul
===============

Graveyard Ghoul runs Three D Radio graveyard timeslots.

It provides a continuous stream of music taken from Three D's music catalogue,
selected at random, but meeting Three D's play quotas.

Released under the MIT licence on the off chance someone else will find it
useful.


# Installation

Here's how to install the Graveyard Ghoul onto a new computer.

## Obtain the code

The GraveyardGhoul source code is up on [github](https://github.com/ThreeDRadio/GraveyardGhoul), and you need to check it out. Make sure you have git installed on the computer you intend to use.

In this case, we'll install GraveyardGhoul to `/usr/local/bin/GraveyardGhoul`, but it doesn't really matter. Wherever you want will work.

```
cd /usr/local/bin
git clone https://github.com/ThreeDRadio/GraveyardGhoul.git
```


You'll now have a copy of the code ready to run.

## Setup virtualenv

Virtualenv is a Python environment manager that lets you keep separate python installations, with different installed packages, for each piece of software. We will use virtualenv to make sure the Ghoul can run without interfering with other python software that may be on the system.

### Install virtualenv (if necessary)

    sudo pip install virtualenv

### Create a virtual environment

```
cd GraveyardGhoul
virtualenv --system-site-packages env
```
Note: `--system-site-packages` is usually frowned upon as bad practice. However, we need it because pygtk2 cannot be installed inside a virtualenv container! :angry:

### Non-pip dependencies

Because Python and its software ecosystem is garbage, there are a few more libraries that need to be installed system wide:

 * Postgresql development files
 * python-gtk2
 * python-glade2
 * python-gst0.10
 * python-gst-1.0

### Install the python packages

Use pip to install all the required python libraries from the requirements.txt file.

    source env/bin/activate 
    pip install -r  requirements.txt

## Edit the config file

First, copy the example config file into place

    cp config.yaml.example config.yaml

Open it up in your favourite editor, and update

* Database connection settings for the music catalogue
* Database connection settings for the message database (wtf are these not the same database!?)
* The filesystem paths for where The Ghoul can find the music and message audio files

If you're @imoore, then I assume you know the answers here :wink:  

## Create a desktop shortcut

The Ghoul code includes a bash script `Ghoul.bash` which can be used to start the software. Just create a desktop shortcut to `/usr/local/bin/GraveyardGhoul/Ghoul.bash`

**Note: If you don't install in `/usr/local/bin` you will need to edit this script to point to the correct directory!**

