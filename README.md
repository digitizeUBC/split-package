# split_package.py

For use when a prepped Archivematica package is too large to run through the pipeline. Allows the user to set a maximum number of objects per package, and creates a series of smaller packages based on that limit. (See Archivematica training docs for guidance on determining package size.)

Make sure you have enough server/desktop space before running. Script does *not* alter or delete the original package when it creates new packages (in case of error), so you'll need double the original space.

## Getting Started

Copy to your desktop:
* split_package.py
* your prepped transfer package

### The Transfer Package

The source transfer package should be structured according to the Digitization Centre's standard (see example below).

```
UL_1088
	/metadata
		metadata.csv
		/submissionDocumentation
			UL_1088_md.xlsx
	/objects
		/edited
			/UL_1088_0001
			/UL_1088_0002
			/UL_1088_0003
		/unedited
			/UL_1088_0001
			/UL_1088_0002
			/UL_1088_0003
```

## Running the script

Open up Terminal and navigate to your Desktop 
(use the 'cd' command, as in the example below)

```
LBRY-DIG_176:~ coolestDPA$ cd Desktop
LBRY-DIG_176:Desktop coolestDPA$ 
```

Use the following command syntax to run the script:

```
python split_package.py \
[SOURCE FOLDER PATH FOR ORIGINAL PACKAGE] \
[DESTINATION FOLDER PATH FOR SPLIT PACKAGES] \
--max_objects=[MAX PER PACKAGE] \
--prefix="[YOUR PREFIX]"
```

Example:
```
python split_package.py \
/Users/coolestDPA/Desktop/UL_1624_01 \
/Users/coolestDPA/Desktop/UL_1624_01_split \
--max_objects=50 \
--prefix="UL_1624_01_"
```
- Two easy ways to add folder paths in Terminal on Mac:
	1. Navigate to the folder in Finder. Click/drag it into the Terminal window. Done!
	2. Navigate to the folder in Finder. Hold the 'alt/option' key, right click the folder, and select 'Copy ... as Pathname'. Paste (Command+V) into the Terminal window.
- The prefix is used to name the new packages. It should usually be the digital identifier associated with the objects. E.g., the prefix "RBSC_ARC_FISH_" will result in a series of packages named "RBSC_ARC_FISH_01", "RBSC_ARC_FISH_02", and so on.

Terminal output will look something like this when the script is running correctly:
```
Transfer will be split into 7.0 packages:
('make', '/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01')
('make', '/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/metadata/submissionDocumentation/')
Copying objects... [src=/Users/coolestDPA/Desktop/UL_1624_01/metadata/submissionDocumentation/] [dst=/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/metadata/submissionDocumentation/]
submissionDocumentation should be available at: /Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/metadata/submissionDocumentation/

- UL_1624_01_0001
('make', '/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/objects/edited/UL_1624_01_0001/')
('make', '/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/objects/unedited/UL_1624_01_0001/')
Copying objects... [src=/Users/coolestDPA/Desktop/UL_1624_01/objects/edited/UL_1624_01_0001/] [dst=/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/objects/edited/UL_1624_01_0001/]
Copying objects... [src=/Users/coolestDPA/Desktop/UL_1624_01/objects/unedited/UL_1624_01_0001/] [dst=/Users/coolestDPA/Desktop/UL_1624_01_split/UL_1624_01_01/objects/unedited/UL_1624_01_0001/]
Writing metadata...

```

... amd the new folder structure will look something like this:
```
UL_1624_01_split
	UL_1624_01_01
		/metadata
			metadata.csv
			/submissionDocumentation
				langmann_basic_md_UL_1624_01.xlsx
		/objects
			/edited
				UL_1624_01_0001
				UL_1624_01_0002
				UL_1624_01_0003
				[...]
				UL_1624_01_0050
			/unedited
				UL_1624_01_0001
				UL_1624_01_0002
				UL_1624_01_0003
				[...]
				UL_1624_01_0050
	UL_1624_01_02
	UL_1624_01_03
	UL_1624_01_04
	UL_1624_01_05
	UL_1624_01_06
	UL_1624_01_07
```

## Authors

* Based very heavily on 'split_sip.py' by [sevein](https://github.com/sevein), downloaded by someone many moons ago
* Adapted for the UBC Library Digitization Centre 2018-06 by [rebeckson](https://github.com/rebeckson)
