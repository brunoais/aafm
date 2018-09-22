aafm
====

# Android ADB File Manager #

A command line + GUI (GTK based) Android ADB-based file manager

![Screenshot](https://raw.githubusercontent.com/zymos/aafm/master/screenshot.png)

Android uses of MTP (Massive Transfer Protocol) for file transfers. Unfortunately this is still very buggy and doesn't work well: system slowing down to a halt when transferring large number of files, files which are there but cannot be seen by the computer... etc.

So **aafm** uses Android Debug protocal.  Using ADB (one of the command line tools provided with the official Android SDK) for communicating with the Android device.  Making it a simple file manager to transfer files.

## Installing ##

### Requirements ###
* Python 2.x
* PyGTK
* git (optional)
* adb (version > 1.0.36)
	* Install via Android Studio https://developer.android.com/studio/ (Very large download)
	* or SDK tools https://developer.android.com/studio (Also a large download)
	* or Android Platform-Tools https://developer.android.com/studio/releases/platform-tools (recomended)
	* or minimal requirement, adb binary (Version > 1.0.36) 

### Install ###
* Download adb and install
	* Only adb is required, but can be aquired via
	* Android Studio https://developer.android.com/studio/ (Very large download)
	* or SDK tools https://developer.android.com/studio (Also a large download)
	* or Android Platform-Tools https://developer.android.com/studio/releases/platform-tools (recomended)
	* or minimal requirement, adb binary (Version > 1.0.36) 
* Clone or Download aafm package
	* Git: git clone https://github.com/zymos/aafm.git
	* Download [ZIP file](https://github.com/zymos/aafm/archive/master.zip)
* Change directory to package location
	* cd aafm/
* Install: 
	* python setup.py install
	* or just run it from the directory

### Enable Android Debug on Phone ###
* https://developer.android.com/studio/debug/dev-options

### Uninstall ###
* Change directory to package location
* python setup.py install --record files.txt
* cat files.txt | xargs rm -rf

### Using it ###

* Execute: aafm
	* Should be that simple

## License ##

Copyright (C) 2011-2012 Soledad Penades (http://soledadpenades.com).

This software is licensed under a GPL V3 license. Please read the accompanying LICENSE.txt file for more details, but basically, if you modify this software and distribute it, you must make your changes public too, so that everyone can benefit from your work--just as you're doing with mine. 

You can also make your changes public even if you don't plan on redistributing this application, okay? Sharing is good! :-)

## Change log ##
2018 09 22
* Supports versions of adb > 1.0.36
* Supports direcories with special chars
* Displays hidden files (optional)
* Better executable
* Update screenshot

2012 09 25 - **r5**

Several bug fixes and refactoring, plus a nice addition for those using desktop systems in Linux!

* New .desktop file and icon allows users to launch aafm from GNOME/KDE/etc menus/shells/launchers ([Huulivoide](http://github.com/Huulivoide)). Fixes #35.
* New setup.py script for making aafm available system-wide ([Huulivoide](http://github.com/Huulivoide)). Fixes #35.
* Fix/refactor copying files between host and device ([sole](http://github.com/sole), [xisberto](http://github.com/xisberto)). Fixes #33 and #37.
* Gracefully handle unknown uids and gids ([sole](http://github.com/sole) and [muflone](http://github.com/muflone)). Fixes #8 and #39.

2012 03 14 - **r4**

Many interesting bug fixes and new features thanks to the work of Norman Rasmussen and Michał Kowalczuk. Thanks!

* Add BusyBox support (by [sammael](http://github.com/sammael)). Fixes #11.
* Handle device drops when there's no row present (by [normanr](http://github.com/normanr)). Fixes #9.
* Handle symlinks on the device correctly (by [normanr](http://github.com/normanr)). Fixes #12.
* Quote/Unquote special characters in drag&drop messages (by [normanr](http://github.com/normanr)). Fixes #10. 
* Slightly improve the README. Clarify how to find out the device Id, add link to PyGTK binary for Mac users.
* Move the TO DO list items that were on this README file over to the issue tracker in the project's page.

2011 11 06 - **r3**

* Fix issue #4: use correct path separator in device when running under Windows
* Fix issue #5: support for finding out ownership in Windows
* Python 3 compatibility
* Start using REVISION file
* README.md revised

2011 09 30 - **r2**

* Fix issue #3: ls -la fails in some devices

2011 07 18 - **r1**

* First initial release; basic functionality is here!


## Attributions ##

- Written by [Sole](http://soledadpenades.com)
- Nice usability ideas from [Mr.doob](http://mrdoob.com/)
- [FamFamFam icons](http://www.famfamfam.com/lab/icons/)
- XDS with PyGTK [tutorial](http://rodney.id.au/dev/gnome/an-xds-example)
- Issues and patches from [Toby Collett](https://github.com/thjc), [Peter Sinnott](https://github.com/psinnott) and [Alexalex89](https://github.com/Alexalex89).
- Updates Xerus2000, zymos

## Hacking ##

I'm by no means a GTK/Python/ADB/Android expert. I'm just learning so this project will surely contain many things that can be improved or that are plain wrong, so feel free to clone the repository and submit pull requests :-)

In order to make your life a bit easier I'll roughly show what each file does:

* **aafm** - shell script to execute aafm-gui.py
* **Aafm.py** - a class that communicates with an Android device, using ADB via shell commands. Takes care of copying and reading files, listing and parsing directories, etc.
* **aafm-gui.py** - this is the GTK front-end. Takes care of building the window with the host and device panels, and issuing instructions to Aafm when the user requests something to be done.
* **TreeViewFile.py** - a utility class that encapsulates a GTKTreeView and some more things in order to show file listings.
* **MultiDragTreeView.py** - an awesome class developed by the guys of Quod Libet, that allows more than one element of a TreeView to be selected and dragged around.

As you can see, an **aafm-cli.py** GUI counterpart is missing. There was one at the beginning but I didn't redo it when I rewrote most of the code from scratch. Feel free to... you know what, if you're interested in having a CLI version.


## Tested On ##
This was initially developed in an Ubuntu Linux 10.10 system. I thought it wouldn't work on other systems, but it seems people are using it in a lot of places though. Some environments where it's known to work:

- Debian 7.0, 8.9
- Ubuntu 10.10, 11.04, 11.10
- Arch Linux
- Windows (!!!)


## TO DO ##

I'm now using Github's issue tracker to keep track of issues, bugs and wished-for features.

If you'd like to have a certain feature or think you've found a bug that is not in the list, please add it to the issue tracker at https://github.com/sole/aafm/issues



