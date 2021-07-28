These scripts are written by Patcha Saheb, to facilitate the transfer of a single frame animation "pose" between Maya and 3D Equalizer.
[patchasaheb@gmail.com]

http://michaelkarp.net//patchaPose.zip

Typically the position of a camera at a particular frame is imported/exported from Maya/3DE as an ASCII file with the extension .pose.

Usually the pose will be of a camera line-up for Matchmoving, but it might be possible to also transfer object poses. The parent hierarchy for objects in 3DE is slightly confusing, as far as importing Object poses.

This .pose file is similar to a Houdini/Nuke .chan file, but only has one line. It is also similar to a Kuper file, but Kuper contains a header with the axes names and also has a modified Right Hand space, with some of the channel polarities reversed.
http://lowrez.marklowne.com/exportchan.html
http://michaelkarp.net/Kuper_ASCII_file-struct.HTML

The .pose file will contain a single line of six numerical values, tx, ty, tz, rx, ry,rz, in Right Hand space.
Example:

      348.502754729999992 157.132706366000008 55.355262352399997 -24.028901663800003 97.891429775700004 0.322090098239999

*Copy the 3D Equalizer python scripts to the user's 3DE python directory.
 3DE_ExportPose.py
 3DE_ImportPose.py

*For the Maya Pose script, Load the Maya Pose Saver script to the Maya script Editor and then save the contents of that script window to the Maya shelf, using the script editor Save To Shelf command.
 Maya_PoseSaver.py
