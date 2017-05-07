yelt
====

# Yetl File Manager #

A  GTK-based file manager with vim key bidings

![Screenshot](http://sole.github.com/aafm/screenshot.png)

Recent Android releases (Honeycomb / 3.0+) replace the older USB mount protocol with the use of MTP (Massive Transfer Protocol). Unfortunately this is still very buggy and doesn't work as it should in any machine I have tested (and heard of): system slowing down to a halt when transferring large number of files, files which are there but cannot be seen by the computer... etc.

So I decided to go ahead and build a little utility that would if not fix, at least alleviate the pain of using Honeycomb devices. **aafm** uses ADB (one of the command line tools provided with the official Android SDK) for communicating with the Android device. This is the same method that IDEs implement.

### Dependencies ###

Python with PyGTK bindings, GTK, git.

### Executing ###

To execute it, cd to the place where it's been cloned:

    cd ~/Applications/aafm/src/

And simply execute it:

    ./aafm-gui.py

If for some odd reason it has lost the executable permission, you can add it:

    chmod +x ./aafm-gui.py

Or simply execute it using Python:

    python ./aafm-gui.py

Once you're satisfied it's working, you can also make a launcher or add it to your Gnome menu, of course!

## Using it ##

If everything works (and why shouldn't it?) you should get a window divided in two panels. The left side represents your host computer, and initially should show the files of the aafm directory, since you launched it from there. The right side represents your Android device's files --so it needs to be connected to the computer, and _USB debugging_ must be enabled in the device.
You can navigate just as you would do with your favourite file explorer. Files can be dragged from one to another panel, directories created, and files renamed (hint: right click and explore the options the contextual menu offers you!). You can also drag from Nautilus (in GNOME) into the device panel, to copy files to the device, or drag _to_ Nautilus, for copying files from the device.

Be warned that currently the progress reporting is a bit hackish and with large files it will appear as if the window has got frozen. It hasn't--it's just waiting for the ADB transfer to finish. In the future this should be fixed, but I haven't come up with the best solution yet.


## License ##

Copyright (C) 2011-2012 Soledad Penades (http://soledadpenades.com).

This software is licensed under a GPL V3 license. Please read the accompanying LICENSE.txt file for more details, but basically, if you modify this software and distribute it, you must make your changes public too, so that everyone can benefit from your work--just as you're doing with mine. 

You can also make your changes public even if you don't plan on redistributing this application, okay? Sharing is good! :-)
